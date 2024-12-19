import os
import requests
from requests.auth import HTTPBasicAuth
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()
scheduler.start()

def twilio():
    send_time = datetime(2024, 12, 16, 21, 49)  # Example: December 8, 2024, at 4 pm
    scheduler.add_job(send_message, 'date', run_date=send_time)
    print("message scheduled for ", send_time)
    return "success!"

    

def send_message():
    print("executing message send")

    X_RAPID_API_KEY = os.getenv('X_RAPID_API_KEY')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    TO_NUMBER = '+19296097511'
    SID = os.getenv('SID')
    MESSAGE_BODY = 'This is a one time scheduled message.'

    url = "https://api.twilio.com/2010-04-01/Accounts/" + SID + "/Messages.json"
    print(url)
    params = {
        "From":TWILIO_PHONE_NUMBER,
        "Body":MESSAGE_BODY,
        "To":TO_NUMBER
    }

    basic = HTTPBasicAuth(SID,X_RAPID_API_KEY)
    print(f"Sending request to {url} with params: {params}")

    response = requests.post(url, auth=basic, data=params)
    print(response.status_code)

    if response.status_code == 201:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Starting scheduler...")
    twilio()
    try:
        # Wait for all jobs to complete
        scheduler._thread.join()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
        scheduler.shutdown(wait=True)
