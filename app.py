# Your code goes here
from flask import Flask, request
import requests
import json


app = Flask(__name__)

response = ""

@app.route('/', methods=['POST','GET'])
def ussd_callback():

    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    contact_list = requests.get("https://us-central1-add-backend-fst4enter5.cloudfunctions.net/contact/").json()


    if text == '':
        response  = "CON What would you want to check \n"
        response += "1. My Phone Book \n"
        response += "2. Add Contact" 
    
    elif text == '1':
        response = "END  \n" + contact_list

    elif text == '2':
        response  = "CON Please type the phone number \n"
        response += "END This is the added phone number. \n" + text

    # elif text == '2':
    #     response = "END This is your phone number " + phone_number 

    return response

# A welcome message to test our server
@app.route('/message')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
        # app.run(host="0.0.0.0", port=os.environ.get('PORT'))
        app.run(threaded=True, port=5000)