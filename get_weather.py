import requests
import json
import configparser
import sys

config = configparser.ConfigParser()
config.read('settings.ini')
BASE_URL = config['openweathermap']['BASE_URL']
APP_ID = config['openweathermap']['APP_ID']
metrics = config['units']['metrics'].split(',')

def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r

def get_units(message):
    if any(_ in message.lower().split(' ') for _ in metrics):
        return 'metric'
    else:
        return 'imperial'


def to_celcius(temperature):
    pass


def get_temperature_summary(temperature_details):
    current_temperature = 'current : '+str(temperature_details['temp'])
    max_temperature = 'high : '+str(temperature_details['temp_max'])
    min_temperature = 'low : '+str(temperature_details['temp_min'])
    if max_temperature == min_temperature:
        temperature_summary = current_temperature
    else:
        temperature_summary = ' \xb0F\n'.join([current_temperature, max_temperature, min_temperature])
    return temperature_summary
    

def get_message_string(data):
    s = {}
    s['header'] = 'weather for '+data['name']+', '+data['sys']['country']+' -'
    s['summary'] = 'description : '+data['weather'][0]['description']
    s['temperature'] = get_temperature_summary(data['main'])
    s['windspeed'] = 'wind speed : '+ str(data['wind']['speed']) + ' miles/hour'
    message= '\n'.join((s['header'], s['summary'], s['temperature'], s['windspeed']))
    return message

def get_current_weather_by_location(message):
    PAYLOAD = {'q': message.title(), 'type':'accurate','appid' : APP_ID, 'units':'imperial'}
    r = get_response(BASE_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return get_message_string(data)
    else:
        return 'Sorry the current location is unavailable'

if __name__ == '__main__':
    get_current_weather_by_location('charlotte')
