from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from get_weather import get_current_weather_by_location

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
        twi_form = request.form.to_dict()
        print(twi_form)
        current_temp, max_temp, min_temp = get_current_weather_by_location(location)
        resp = MessagingResponse()
        resp.message('Temperatures in {location} -\n Current: {temp}F\n Maximum: {max_temp}F\n Minimum: {min_temp}F'.format(location=location, temp=current_temp, max_temp=max_temp, min_temp=min_temp))
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)