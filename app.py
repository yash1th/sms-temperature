from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from get_weather import get_current_weather_by_location

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Welcome to text me weather'

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

    location = request.form.get('Body')
    current_temp, max_temp, min_temp = get_current_weather_by_location(location)
    resp = MessagingResponse()
    resp.message('The temperature in {location} is {temp}F. Maximum would be {temp_ma} and Minimum would be {temp_mi}'.format(location=location, temp=current_temp, temp_ma=max_temp, temp_mi=temp_mi))
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)