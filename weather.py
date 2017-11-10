class Weather:
    def __init__(self, city):
        self._city = city
        self._country = None
        self._current = dict.fromkeys(('description', 'temp', 'high', 'low', 'wind'))
        self._forecast = dict.fromkeys(('description', 'temp', 'high', 'low'))
        self._error = ''

# def get_forecast_string(data):
#     s = {}
#     s['header'] = '3 hour forecast-'
#     s['temperature'] = get_temperature_summary(data['main'])
#     s['description'] = data['weather'][0]['description']
#     return '\n'.join([s['header'], s['description'], s['temperature']])