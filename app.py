# Your code goes here
from flask import Flask, request
import requests
import json

from firebase import firebase


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
    my_contact_list = str(contact_list)

    firedb = firebase.FirebaseApplication("https://add-backend-fst4enter5-default-rtdb.firebaseio.com/", None)
    result = firedb.get('/contacts', None)
    for x in result.values():
        print(x)

    if text == '' :
        response  = "CON What would you want to check \n"
        response += "1. My Phone Book \n"
        response += "2. Add Contact" 
    
    elif text == '1':
        response = "END  \n" + x

    elif text == '2':
        response  = "CON Kindly type your number\n"

    elif text == f'2*{text[2:]}':
        response  = "CON Kindly type your name\n"
        # response += "0. Back"
        # response += "END This is the added phone number. \n" + text

    elif f'2*{text[2:]}*' in text:
        # time to save the values we have gotten
        response = "CON Please confirm your details \n"
        response += "1. Yes"
        response += "2. No"
        
    elif f'2*{text[1:]}*1*' in text:
        response = "END Let us save  \n"

    else:
        response = "END Invalid Option"
    return response

# A welcome message to test our server
@app.route('/message')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
        # app.run(host="0.0.0.0", port=os.environ.get('PORT'))
        app.run(threaded=True, port=5000)