import requests
from requests.auth import HTTPBasicAuth
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
scheduler = BackgroundScheduler()
def twilio():
    send_time = datetime(2024, 12, 9, 12, 20)  # Example: December 8, 2024, at 4 pm
    scheduler.add_job(send_message, 'date', run_date=send_time)
    print("message scheduled for ", send_time)
    scheduler.start()

    return "success!"

    

def send_message():
    print("executing message send")
    X_RAPID_API_KEY = '6d2caefdfe96c5737a7b5b8e9f3f75f9'
    TWILIO_PHONE_NUMBER = '+19177465798'
    TO_NUMBER = '+19296097511'
    SID = 'AC2971234654291b575ae9c6c249759e49'
    MESSAGE_BODY = 'This is a one time scheduled message.'

    url = "https://api.twilio.com/2010-04-01/Accounts/" + SID + "/Messages.json"

    params = {
        "From":TWILIO_PHONE_NUMBER,
        "Body":MESSAGE_BODY,
        "To":TO_NUMBER
    }
    basic = HTTPBasicAuth(SID,X_RAPID_API_KEY)
    print(f"Sending request to {url} with params: {params}")
    response = requests.post(url, auth=basic, data=params)

    if response.status_code == 201:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")