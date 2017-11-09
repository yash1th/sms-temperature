import requests
import json
import configparser
import sys
import os


config = configparser.ConfigParser()
config.read('settings.ini')
CURRENT_WEATHER_URL = config['openweathermap']['CURRENT_WEATHER_URL']
FORECAST_WEATHER_URL = config['openweathermap']['FORECAST_WEATHER_URL']
APP_ID = config['openweathermap']['APP_ID']


def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r

def get_temperature_summary(temperature_details):
    current_temperature = 'now: '+str(temperature_details['temp'])
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
    s['windspeed'] = 'wind speed : '+ str(data['wind']['speed']) + ' miles/hour'
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
    s['header'] = '\nforecast for the next 3 hours'
    s['temperature'] = get_temperature_summary(data['main'])
    s['description'] = data['weather'][0]['description']
    s['windspeed'] = 'windspeed: '+str(data['wind']['speed'])
    return '\n'.join([s['header'], s['description'], s['temperature'], s['windspeed']])

def get_forecast_weather_by_location(message):
    PAYLOAD = {'q': message.title(), 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(FORECAST_WEATHER_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))['list'][0]
        return get_forecast_string(data)
    else:
        return 'Sorry the location you sent is either not valid or forecast is not available for that area'


if __name__ == '__main__':
    # print(len(get_current_weather_by_location('charlotte')))
    # print(len(get_current_weather_by_location('vijayawada')))
    import time
    s = time.time()
    print(len(get_current_weather_by_location('charlotte')+get_forecast_weather('charlotte')))
    print('total time = ',time.time()-s)