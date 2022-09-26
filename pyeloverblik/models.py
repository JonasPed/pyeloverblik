'''
All model classes for pyeloverblik
'''

class RawResponse:
    '''
    Class representing a raw response by http status code and http body.
    '''
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, response):
        self._body = response

class TimeSeries:
    '''
    Class representing a parsed time series data for a single day.
    '''
    def __init__(self, status, data_date, metering_data, detailed_status=None):
        self._status = status
        self._data_date = data_date
        self._metering_data = metering_data
        self._detailed_status = detailed_status

    @property
    def status(self):
        return self._status

    @property
    def detailed_status(self):
        return self._detailed_status
    
    @property
    def data_date(self):
        return self._data_date
    
    def get_metering_data(self, index):
        '''
        Get metering data for a single hour or month.
        index=1: data between 00.00 and 01.00 if TimeSeries contains day data, or January if TimeSeries contains month data.
        index=4: data between 03.00 and 04.00 if TimeSeries contains day data, or April if TimeSeries contains month data.
        '''
        return self._metering_data[index-1]

    def get_total_metering_data(self):
        total = 0
        for v in self._metering_data:
            total += v

        return total

class Charges:
    '''
    Class representing parsed charges data.
    '''
    def __init__(self, status, charges, detailed_status=None):
        self._status = status
        self._charges = charges
        self._detailed_status = detailed_status

    @property
    def status(self):
        return self._status

    @property
    def detailed_status(self):
        return self._detailed_status
    
    @property
    def charges(self):
        return self._charges
    