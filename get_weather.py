import requests
import json
import configparser
import sys
import os
from pprint import pprint as pp

config = configparser.ConfigParser()
config.read('settings.ini')
CURRENT_WEATHER_URL = config['openweathermap']['CURRENT_WEATHER_URL']
FORECAST_WEATHER_URL = config['openweathermap']['FORECAST_WEATHER_URL']
APP_ID = config['openweathermap']['APP_ID']


def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r

def get_temperature_summary(temperature_details):
    current_temperature = 'temp: '+str(temperature_details['temp'])
    maximum_temperature = 'high: '+str(temperature_details['temp_max'])
    minimum_temperature = 'low: '+str(temperature_details['temp_min'])
    if temperature_details['temp_max'] == temperature_details['temp_min']:
        return current_temperature+' \xb0F'
    else:
        return ' \xb0F\n'.join([current_temperature, maximum_temperature, minimum_temperature])+' \xb0F'
    
def get_message_string(data):
    s = {}
    s['header'] = data['name']+', '+data['sys']['country']+'-'
    s['summary'] = data['weather'][0]['description']
    s['temperature'] = get_temperature_summary(data['main'])
    s['windspeed'] = 'wind: '+ str(data['wind']['speed']) + ' m/h'
    message= '\n'.join((s['header'], s['summary'], s['temperature'], s['windspeed']))
    return message

def get_current_weather_by_location(message):
    PAYLOAD = {'q': message.title(), 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(CURRENT_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return get_message_string(data)
    else:
        return 'Sorry the location you sent is either not valid or available'

def get_forecast_string(data):
    s = {}
    s['header'] = '3 hour forecast-'
    s['temperature'] = get_temperature_summary(data['main'])
    s['description'] = data['weather'][0]['description']
    return '\n'.join([s['header'], s['description'], s['temperature']])

def get_forecast_weather_by_location(message):
    PAYLOAD = {'q': message.title(), 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(FORECAST_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))['list'][0]
        return get_forecast_string(data)
    else:
        return ''

def get_weather_by_location(message):
    return '\n\n'.join([get_current_weather_by_location(message), get_forecast_weather_by_location(message)])


if __name__ == '__main__':
    print(get_weather_by_location('asdjlkahdsjkasd'))
    #print(get_weather_by_location('vijayawada'))