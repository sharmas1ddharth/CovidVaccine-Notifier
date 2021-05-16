"""
TODO: Send notification according to the registered date to the registered number
"""

import requests

from datetime import datetime, timedelta
import time

import json

from twilio.rest.api.v2010.account import message

import send_message

age = int(input("Enter age :"))
pin = input("Enter pincode : ")
pinCodes = [pin]
num_days = 2

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
print(actual_dates)
message_to_send = """ """

while True:

    counter = 0

    for pinCode in pinCodes:
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pinCode, given_date)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()

                flag = False
                if response_json["centers"]:
                    if (print_flag.lower() == 'y'):

                        for center in response_json["centers"]:

                            for session in center["sessions"]:
                                if session["min_age_limit"] <= age and session["available_capacity"] > 0:
                                    message = f"""\n\nPincode: {pinCode}
Available on: {given_date}
{center["name"]}
{center["block_name"]}
Price:  {center["fee_type"]}
Availablity :  {session["available_capacity"]}\n"""

                                    if session["vaccine"] != '':
                                        message = message + f"Vaccine type: {session['vaccine']}\n"

                                        message_to_send += message

                                    counter = counter + 1

                                else:
                                    pass
                else:
                    pass

            else:
                print("No Response!")

    if counter == 0:

        message_to_send_when_no = "No Vaccination slot avaliable!"
        to_number = "to number" # number to which we have to send the notification
        send_message.send_whatsapp_message(to_number, message_to_send_when_no)

    else:
        to_number = "to number" # number to which we have to send the notification

        with open("center.txt", "r") as f:
            count = 0
            ten_center = ""
            for text in f:
                if count == 10:
                    break
                if "Vaccine" in text:
                    count += 1
                ten_center += text
            send_message.send_whatsapp_message(to_number, ten_center)

        break

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
