import requests
import json
import configparser
import sys
import os


config = configparser.ConfigParser()
config.read('settings.ini')
BASE_URL = config['openweathermap']['BASE_URL']
APP_ID = config['openweathermap']['APP_ID']


def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r

def get_temperature_summary(temperature_details):
    current_temperature = 'current : '+str(temperature_details['temp'])
    maximum_temperature = 'high : '+str(temperature_details['temp_max'])
    minimum_temperature = 'low : '+str(temperature_details['temp_min'])
    if temperature_details['temp_max'] == temperature_details['temp_min']:
        temperature_summary = current_temperature
    else:
        temperature_summary = ' \xb0F\n'.join([current_temperature, maximum_temperature, minimum_temperature])
    return temperature_summary+' \xb0F'
    

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
        return 'Sorry the location you sent is either not valid or unavailable'

if __name__ == '__main__':
    print(get_current_weather_by_location('charlotte'))
    print(get_current_weather_by_location('vijayawada'))
