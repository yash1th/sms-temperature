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
        return 'metrics'
    else:
        return 'imperial'

def get_current_weather_by_location(incoming_message):
    PAYLOAD = {'q': incoming_message.lower()+',us', 'appid' : APP_ID, 'units':'imperials'}
    r = get_response(BASE_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return data['main']['temp'], data['main']['temp_max'], data['main']['temp_min']

if __name__ == '__main__':
    get_current_weather_by_location('charlotte')
