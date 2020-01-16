from datetime import datetime
from datetime import timedelta
import requests

class Eloverblik:
    def __init__(self, refreshToken):
        self._refresh_token = refreshToken
        self._base_url = 'https://api.eloverblik.dk/CustomerApi/'
        pass

    def getTimeSeries(self, meetering_point, fromDate=datetime.now()-timedelta(days=1), toDate=datetime.now(), aggregation='Hour'):
        url = self._base_url + 'api/Token'
        print(url)
        headers = {'Authorization': 'Bearer ' + self._refresh_token}
        token_response = requests.get(url, headers=headers)
        token_response.raise_for_status()
                
        tokenJson = token_response.json()

        short_token = tokenJson['result']

        dateFormat = '%Y-%m-%d'
        f = fromDate.strftime(dateFormat)
        t = toDate.strftime(dateFormat)
        body = "{\"meteringPoints\": {\"meteringPoint\": [\"" + meetering_point + "\"]}}"
        headers = {'Authorization': 'Bearer ' + short_token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(self._base_url + f'/api/MeterData/GetTimeSeries/{f}/{t}/Hour', data=body, headers=headers)
        
        response.raise_for_status()

        print(response.json())

        return response.json()





