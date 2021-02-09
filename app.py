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
    print(result)

    split_up = [s.strip() for s in text.split("*")]
    print(split_up)
    
    if len(split_up) == 4 :
        user_name = split_up[3]
    elif len(split_up) >= 2:
        user_name = "Name"
        phone = split_up[1]
    else:
        user_name = "Name"
        phone = "0000"


    if text == '' :
        response  = "CON What would you want to check \n"
        response += "1. My Phone Book \n"
        response  = "2. Add Contact \n" 
    
    elif text == '1':
        for x in result.values():
            name = x["fullName"]
            email = x["email"]
            phoneNumber = x["phoneNumber"]
            print(name,email,phoneNumber)
            
            response += f"CON Name:{name} No:{phoneNumber} Email:{email}\n"
            response  = "END."

    elif text == '2':
        response  = "CON Kindly type your number\n"

    elif text == f'2*{phone}':
        response  = "CON Do you want to continue? \n"
        response += "1. Yes \n"
        response  = "2. No"

    elif text == f'2*{phone}*1':
        # time to save the values we have gotten
        response = "CON Kindly type your name\n"

    elif text == f'2*{phone}*2':
        # time to save the values we have gotten
        response = "END Contact not saved \n"

    
    elif text == f'2*{phone}*1*{name}':
        phone_no = split_up[1]
        name = split_up[3]

        üser = {
                'fullName': name,
                'phoneNumber': phone_no
               }

        new_user = firebase.post('/contacts',üser)  
        print(new_user)
        response = f"END {new_user} added successfully  \n"
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