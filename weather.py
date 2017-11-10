class Weather:
    def __init__(self, city):
        self._city = city
        self._country = None
        self._current = dict.fromkeys(('description', 'temp', 'high', 'low', 'wind'))
        self._forecast = dict.fromkeys(('description', 'temp', 'high', 'low'))
        self._error = ''
    
    def get_city(self):
        return self._city

    def get_country(self):
        return self._country

    def get_current_weather_object(self):
        return self._current

    def get_forecast_weather_object(self):
        return self._forecast

    def get_error(self):
        return self._error