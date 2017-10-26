import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
BASE_URL = config['openweathermap']['BASE_URL']
APP_ID = config['openweathermap']['APP_ID']

def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r

def get_current_weather_by_location(location):
    PAYLOAD = {'q': location.lower()+',us', 'appid' : APP_ID, 'units':'imperial'}
    r = get_response(BASE_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return data['main']['temp']

if __name__ == '__main__':
    get_current_weather_by_location(sys.argv[1])
