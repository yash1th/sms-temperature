from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from get_weather import get_weather_by_location
from get_weather import get_weather_by_location_2

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Welcome to text me weather'

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    if request.method == 'GET':
        return 'You reached the sms page'
    else:
        location = request.form.get('Body')
        resp = MessagingResponse()
        resp.message(get_weather_by_location_2(location.strip().title()))
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)