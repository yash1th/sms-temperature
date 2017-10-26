from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from get_weather import get_current_weather_by_location

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Welcome to text me weather'

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    location = request.form.get('Body')
    temp, temp_max, temp_min = get_current_weather_by_location(location)
    # Start our TwiML response
    resp = MessagingResponse()
    print(resp)
    # Add a message
    resp.message('The temperature in {location} is {temp} F'.format(location=location, temp=temp))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)