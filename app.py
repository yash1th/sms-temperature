from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from get_weather import get_weather_by_location

app = Flask(__name__)


from rq import Queue
from worker import conn

q = Queue(connection=conn)
from utils import jilebi

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
        result = q.enqueue(jilebi, str(resp))
        print(result)
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)