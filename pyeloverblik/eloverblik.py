'''
Primary public module for eloverblik.dk API wrapper.
'''
from datetime import datetime
from datetime import timedelta
import requests

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

        response.raise_for_status()

        return response.json()

    def get_yesterday_parsed(self, metering_point):
        raw_result = self.get_time_series(metering_point)

        response = dict()

        for k in raw_result['result'][0]['MyEnergyData_MarketDocument'] \
            ['TimeSeries'][0]['Period'][0]['Point']:
            response[k['position']] = k['out_Quantity.quantity']

        return response
