from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from get_weather import get_weather_by_location

app = Flask(__name__)

import redis
r = redis.from_url(os.environ.get("REDIS_URL"))
print('redis url', r)

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
        resp.message(get_weather_by_location(location.strip().title()))
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)