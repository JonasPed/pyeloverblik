'''
Primary public module for eloverblik.dk API wrapper.
'''
from datetime import datetime
from datetime import timedelta
from requests.exceptions import HTTPError
import requests
from .models import RawResponse
from .models import TimeSeries
import json

class Eloverblik:
    '''
    Primary exported interface for eloverblik.dk API wrapper.
    '''
    def __init__(self, refreshToken):
        self._refresh_token = refreshToken
        self._base_url = 'https://api.eloverblik.dk/CustomerApi/'

    def get_time_series(self,
                        meetering_point,
                        from_date=datetime.now()-timedelta(days=1),
                        to_date=datetime.now(),
                        aggregation='Hour'):
        '''
        Call time series API on eloverblik.dk. Defaults to yester days data.
        '''
        url = self._base_url + 'api/Token'
        headers = {'Authorization': 'Bearer ' + self._refresh_token}
        token_response = requests.get(url, headers=headers)
        token_response.raise_for_status()

        tokenJson = token_response.json()

        short_token = tokenJson['result']

        dateFormat = '%Y-%m-%d'
        parsed_from_date = from_date.strftime(dateFormat)
        parsed_to_date = to_date.strftime(dateFormat)
        body = "{\"meteringPoints\": {\"meteringPoint\": [\"" + meetering_point + "\"]}}"

        headers = {'Authorization': 'Bearer ' + short_token,
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        response = requests.post(self._base_url + f'/api/MeterData/GetTimeSeries/{parsed_from_date}/{parsed_to_date}/{aggregation}',
                                 data=body,
                                 headers=headers)

        raw_response = RawResponse()
        raw_response.status = response.status_code
        raw_response.body = response.text

        return raw_response

    def get_yesterday_parsed(self, metering_point):
        raw_data = self.get_time_series(metering_point)

        if raw_data.status == 200:
            json_response = json.loads(raw_data.body)

            result = self._parse_result(datetime.now()-timedelta(days=1), json_response)
        else:
            result = TimeSeries(raw_response.status, None, None, raw_response.body)

        return result

    def _parse_result(self, date, result):
        metering_data = []

        if 'result' in result and len(result['result'])  > 0:
            market_document = result['result'][0]['MyEnergyData_MarketDocument']

            if 'TimeSeries' in market_document and len(market_document['TimeSeries']) > 0:
                time_series = market_document['TimeSeries'][0]

                if 'Period' in time_series and len(time_series['Period']) > 0:
                    point = time_series['Period'][0]['Point']
                    for i in point:
                        metering_data.append(float(i['out_Quantity.quantity']))

                    result = TimeSeries(200, date, metering_data)

                    return result
                else:
                    return TimeSeries(404, None, None, f"Data most likely not available yet: {result}")
            else:
                return TimeSeries(404, None, None, f"Data most likely not available yet: {result}")
        else:
            return TimeSeries(404, None, None, f"Data most likely not available yet: {result}")
