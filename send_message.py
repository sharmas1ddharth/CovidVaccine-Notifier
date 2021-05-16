

import requests

TWILIO_SID = "TWILIO_SID" # enter twilio sid here
TWILIO_AUTHTOKEN = "TWILIO_AUTHTOKEN" # enter twilio auth key here
TWILIO_MESSAGE_ENDPOINT = "https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json".format(TWILIO_SID=TWILIO_SID)

TWILIO_NUMBER = "twilio number" # enter twilio  number here

def send_whatsapp_message(to, message):
    message_data = {
        "To": to,
        "From": TWILIO_NUMBER,
        "Body": message,
    }
    response = requests.post(TWILIO_MESSAGE_ENDPOINT, data=message_data, auth=(TWILIO_SID, TWILIO_AUTHTOKEN))
    
    response_json = response.json()
    
    
