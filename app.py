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
    split_up = [s.strip() for s in text.split("*")]
    print(split_up)
    number = 0
    user_name = "name"
    phone = "000"
    email = "email"
    if len(split_up) >= 4 :
        email = split_up[3]
        phone = split_up[2]
        user_name = split_up[1] 
    elif len(split_up) >= 3:
        phone = split_up[2]
        user_name = split_up[1]
    elif len(split_up) >= 2:
        user_name = split_up[1]

    print(text)   

    if text == '' :
        response  = "CON What would you want to check \n"
        response += "1. My Phone Book \n"
        response += "2. Add Contact \n" 
    
    elif text == '1':
        response = "END "
        for x in result.values():
            name = x["fullName"]
            email = x["email"]
            phoneNumber = x["phoneNumber"]
            number += 1
            print(number,name,email,phoneNumber)
            
            response += f"{number}: Full Name: {name},\n Phone number: {phoneNumber},\n Email: {email}\n"

    elif text == '2':
        response  = "CON Kindly type the name\n"

    elif text == f"2*{user_name}":
        # time to save the values we have gotten
        response = f"CON Kindly type the number to save {user_name}\n"

    elif text == f"2*{user_name}*{phone}":
        # time to save the values we have gotten
        response = f"CON Enter the email to save {user_name}\n"

    elif text == f"2*{user_name}*{phone}*{email}":
        response  = f"CON Do you want to continue to save {user_name}\n with phone number:{phone} and email:{email}? \n"
        response += "1. Yes \n"
        response += "2. No"

    elif text == f"2*{user_name}*{phone}*{email}*1":
        #save with email
        üser = {
                'email': email,
                'fullName': user_name,
                'phoneNumber': phone
               }

        new_user = firedb.post('/contacts',üser)  
        print(new_user)
        response = f"END {user_name} added successfully to contact list  \n"

    elif text == f"2*{user_name}*{phone}*{email}*2":
    # time to save the values we have gotten
        response = "END Contact not saved \n"
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