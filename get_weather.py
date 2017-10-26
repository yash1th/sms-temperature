import requests
import sys
import json
from pprint import pprint as pp

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
#https://api.openweathermap.org/data/2.5/weather?q=London&APPID=535a0b9cdae68e503b65c22508e3661a
APP_ID = '535a0b9cdae68e503b65c22508e3661a'

def get_response(url, parameters):
    r = requests.get(url, params = parameters)
    return r

def get_current_weather_by_location(location):
    PAYLOAD = {'q':location.lower()+',us', 'appid' : APP_ID, 'units':'imperial'}
    r = get_response(BASE_URL, PAYLOAD)
    if r.status_code == 200:
        data = json.loads(r.content.decode('utf-8'))
        return data['main']['temp']

if __name__ == '__main__':
    get_current_weather_by_location(sys.argv[1])
