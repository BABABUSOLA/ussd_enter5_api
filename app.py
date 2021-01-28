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
    my_contact_list = str(contact_list)


    if text == '' :
        response  = "CON What would you want to check \n"
        response += "1. My Phone Book \n"
        response += "2. Add Contact" 
    
    elif text == '1':
        response = "END  \n" + my_contact_list

    elif text == '2':
        response  = "CON Kindly \n"
        response += "1. Type your number \n"
        # response += "0. Back"
        # response += "END This is the added phone number. \n" + text
    
    elif '*2*' in text:
        response = "CON Kindly \n"
        response = "1. Type your name to save this number" + text 

    # elif text == '2':
    #     response = "END This is your phone number " + phone_number 
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