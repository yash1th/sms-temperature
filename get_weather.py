import requests
import json
import configparser
import os
from weather import Weather


config = configparser.ConfigParser()
config.read('settings.ini')
CURRENT_WEATHER_URL = config['openweathermap']['CURRENT_WEATHER_URL']
FORECAST_WEATHER_URL = config['openweathermap']['FORECAST_WEATHER_URL']
APP_ID = config['openweathermap']['APP_ID']


def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r
    
def get_message_string(data):
    s = {}
    s['header'] = data['name']+', '+data['sys']['country']+'-'
    s['summary'] = data['weather'][0]['description']
    s['temperature'] = get_temperature_summary(data['main'])
    s['windspeed'] = 'wind: '+ str(data['wind']['speed']) + ' m/h'
    message= '\n'.join((s['header'], s['summary'], s['temperature'], s['windspeed']))
    return message

def get_current_weather_by_location(message):
    PAYLOAD = {'q': message, 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(CURRENT_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return get_message_string(data)
    else:
        return 'Sorry the location you sent is either not valid or unavailable'

def get_forecast_string(data):
    s = {}
    s['header'] = '3 hour forecast-'
    s['temperature'] = get_temperature_summary(data['main'])
    s['description'] = data['weather'][0]['description']
    return '\n'.join([s['header'], s['description'], s['temperature']])

def get_forecast_weather_by_location(message):
    PAYLOAD = {'q': message, 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(FORECAST_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))['list'][0]
        return get_forecast_string(data)
    else:
        return ''

def construct_current_weather_string(details):
    header = ', '.join([details._city, details._country])
    temperature = get_temperature_summary(details._current)
    return '\n'.join([header, details._current['description'], temperature, 'wind: '+details._current['wind']])

def get_temperature_summary(temperature_details):
    current_temperature = 'temp: '+str(temperature_details['temp'])
    maximum_temperature = 'high: '+str(temperature_details['high'])
    minimum_temperature = 'low: '+str(temperature_details['low'])
    if temperature_details['high'] == temperature_details['low']:
        return current_temperature+' \xb0F'
    else:
        return ' \xb0F\n'.join([current_temperature, maximum_temperature, minimum_temperature])+' \xb0F'

def get_current_weather_by_location_2(details):
    PAYLOAD = {'q': details._city, 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(CURRENT_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        details._country = data['sys']['country']
        details._current['description'] = data['weather'][0]['description']
        details._current['temp'] = str(data['main']['temp'])
        details._current['high'] = str(data['main']['temp_max'])
        details._current['low'] = str(data['main']['temp_min'])
        details._current['wind'] = str(data['wind']['speed']) + ' m/h'
    else:
        details._error = 'Sorry the location you sent is either not valid or unavailable'

def construct_forecast_weather_string(details):
    header = '3 hour forecast-'
    temperature = get_temperature_summary(details._forecast)
    return '\n'.join([header, details._forecast['description'], temperature])


def get_forecast_weather_by_location_2(details):
    PAYLOAD = {'q': details._city, 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(FORECAST_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))['list'][0]
        details._forecast['description'] = data['weather'][0]['description']
        details._forecast['temp'] = str(data['main']['temp'])
        details._forecast['high'] = str(data['main']['temp_max'])
        details._forecast['low'] = str(data['main']['temp_min'])
    else:
        details._error = 'Sorry the location you sent is either not valid or unavailable'

def get_weather_by_location_2(location):
    details = Weather(location)
    get_current_weather_by_location_2(details)
    if details._error:
        return details._error
    get_forecast_weather_by_location_2(details)
    if details._error:
        return '\n'.join([construct_current_weather_string(details), details._error])
    return '\n\n'.join([construct_current_weather_string(details), construct_forecast_weather_string(details)])



def get_weather_by_location(location):
    return '\n\n'.join([get_current_weather_by_location(message), get_forecast_weather_by_location(message)])


if __name__ == '__main__':
    # print(get_weather_by_location('asdjlkahdsjkasd'))
    # print(get_weather_by_location('vijayawada'))
    print(get_weather_by_location_2('charlotte'))
    print(get_weather_by_location_2('vijayawada'))