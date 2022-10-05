'''
Primary public module for eloverblik.dk API wrapper.
'''
from datetime import datetime
from datetime import timedelta
import json
from os import access
import re
import requests
import logging
from .models import RawResponse
from .models import TimeSeries
from .models import Charges
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

_LOGGER = logging.getLogger(__name__)

retry_strategy = Retry(
    total=3,
    status_forcelist=[400, 429, 500, 502, 503, 504],
    method_whitelist=["GET", "POST"],
    backoff_factor=60
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)


class Eloverblik:
    '''
    Primary exported interface for eloverblik.dk API wrapper.
    '''

    _access_token_cache = (None, None)

    def __init__(self, refresh_token):
        self._refresh_token = refresh_token
        self._base_url = 'https://api.eloverblik.dk/CustomerApi/'

    def get_time_series(self,
                        meetering_point,
                        from_date=None,  # Will be set to yesterday
                        to_date=None,  # Will be set to today
                        aggregation='Hour'):
        '''
        Call time series API on eloverblik.dk. Defaults to yester days data.
        '''
        if from_date is None:
            from_date = datetime.now()-timedelta(days=1)
        if to_date is None:
            to_date = datetime.now()

        access_token = self._get_access_token()

        date_format = '%Y-%m-%d'
        parsed_from_date = from_date.strftime(date_format)
        parsed_to_date = to_date.strftime(date_format)
        body = "{\"meteringPoints\": {\"meteringPoint\": [\"" + \
            meetering_point + "\"]}}"

        headers = self._create_headers(access_token)

        url = self._base_url + \
            f'/api/MeterData/GetTimeSeries/{parsed_from_date}/{parsed_to_date}/{aggregation}'
        response = http.post(url,
                                 data=body,
                                 headers=headers,
                                 timeout=5
                                 )

        _LOGGER.debug(
            f"Response from API. Status: {response.status_code}, Body: {response.text}")

        raw_response = RawResponse()
        raw_response.status = response.status_code
        raw_response.body = response.text

        return raw_response

    def get_tariffs(self,
                    metering_point):
        '''
        Call charges API on eloverblik.dk and extract tariffs. Note that this does not include subscriptions or fees.
        '''

        access_token = self._get_access_token()
        headers = self._create_headers(access_token)
        body = '{"meteringPoints": {"meteringPoint": ["' + metering_point + '"]}}'
        url = self._base_url + '/api/meteringpoints/meteringpoint/getcharges'
       
        response = requests.post(url,
                                 data=body,
                                 headers=headers,
                                 timeout=5
                                 )

        _LOGGER.debug(
            f"Response from API. Status: {response.status_code}, Body: {response.text}")

        if response.status_code == 200:
            return self._parse_tariffs_from_charges_result(json.loads(response.text))
        else:
            return Charges(response.status_code, None, response.text)

    def _get_access_token(self):
        cache_datetime, short_token = Eloverblik._access_token_cache

        if cache_datetime is not None and datetime.today() - cache_datetime < timedelta(hours = 12):
            _LOGGER.debug("Found valid token in cache.")
            return short_token

        url = self._base_url + 'api/Token'
        headers = {'Authorization': 'Bearer ' + self._refresh_token}

        token_response = http.get(url, headers=headers, timeout=5)
        token_response.raise_for_status()

        token_json = token_response.json()
        short_token = token_json['result']

        Eloverblik._access_token_cache = (datetime.today(), short_token)

        _LOGGER.debug(f"Got short lived token: {short_token}")
        return short_token

    def _create_headers(self, access_token):
        return {'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'}

    def get_yesterday_parsed(self, metering_point):
        '''
        Get data for yesterday and parse it.
        '''
        raw_data = self.get_time_series(metering_point)

        if raw_data.status == 200:
            json_response = json.loads(raw_data.body)

            result_dict = self._parse_result(json_response)
            (key, value) = result_dict.popitem()
            result = value
        else:
            result = TimeSeries(raw_data.status, None, None, raw_data.body)

        return result

    def get_latest(self, metering_point):
        '''
        Get latest data. Will look for one week.
        '''
        raw_data = self.get_time_series(metering_point,
                                        from_date=datetime.now()-timedelta(days=8),
                                        to_date=datetime.now())

        if raw_data.status == 200:
            json_response = json.loads(raw_data.body)

            r = self._parse_result(json_response)

            keys = list(r.keys())

            keys.sort()
            keys.reverse()

            result = r[keys[0]]
        else:
            result = TimeSeries(raw_data.status, None, None, raw_data.body)

        return result

    def get_per_month(self, metering_point, year=None):
        '''
        Get total consumption for each month in the given year, as well as the total for the year.
        '''
        if year is None:
            year = datetime.today().year

        if not re.match('\d{4}', str(year)):
            raise ValueError("Year must be a four digit number.")

        raw_data = self.get_time_series(metering_point,
                                        from_date=datetime(year, 1, 1),
                                        to_date=datetime(year, 12, 31) if year < datetime.today().year else datetime.today(),
                                        aggregation='Month')
        
        if raw_data.status == 200:
            json_response = json.loads(raw_data.body)

            r = self._parse_result(json_response)
            keys = list(r.keys())
            keys.sort()

            result = TimeSeries(raw_data.status, keys[-1], [r[k].get_total_metering_data() for k in keys])
        else:
            result = TimeSeries(raw_data.status, None, None, raw_data.body)

        return result


    def _parse_result(self, result):
        '''
        Parse result from API call.
        '''
        parsed_result = {}

        if 'result' in result and len(result['result']) > 0:
            market_document = result['result'][0]['MyEnergyData_MarketDocument']
            if 'TimeSeries' in market_document and len(market_document['TimeSeries']) > 0:
                time_series = market_document['TimeSeries'][0]

                if 'Period' in time_series and len(time_series['Period']) > 0:
                    for period in time_series['Period']:
                        metering_data = []

                        point = period['Point']
                        for i in point:
                            metering_data.append(
                                float(i['out_Quantity.quantity']))

                        date = datetime.strptime(
                            period['timeInterval']['end'], '%Y-%m-%dT%H:%M:%SZ')

                        time_series = TimeSeries(200, date, metering_data)

                        parsed_result[date] = time_series
                else:
                    parsed_result['none'] = TimeSeries(404,
                                                       None,
                                                       None,
                                                       f"Data most likely not available yet-1: {result}")
            else:
                parsed_result['none'] = TimeSeries(404,
                                                   None,
                                                   None,
                                                   f"Data most likely not available yet-2: {result}")
        else:
            parsed_result['none'] = TimeSeries(404,
                                               None,
                                               None,
                                               f"Data most likely not available yet-3: {result}")

        return parsed_result

    def _parse_tariffs_from_charges_result(self, result):
        ''' 
        Parse charges result from API call
        '''

        if 'result' in result and len(result['result']) > 0 and 'result' in result['result'][0] and 'tariffs' in result['result'][0]['result']:
            charges = {}

            for tariff in result['result'][0]['result']['tariffs']:
                name = tariff['name'].lower().replace(' ', '_')

                if tariff['periodType'] == 'P1D':
                    charges[name] = tariff['prices'][0]['price']
                elif tariff['periodType'] == 'PT1H':
                    sorted_prices = [p['price'] for p in sorted(tariff['prices'], key=lambda d: int(d['position']))]
                    charges[name] = sorted_prices
                else:
                    raise NotImplementedError(f"Unsupported periodType for tariff '{tariff['periodType']}")

            return Charges(200, charges)

        else:
            return Charges(400, None);