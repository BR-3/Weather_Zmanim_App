import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

scheduler = BackgroundScheduler()
scheduler.start()

def setup_notifications(notifications_collection):
    notifications_cursor = notifications_collection.find()

    for notification in notifications_cursor:
        notification_type = notification.get('notification_type')
        notification_time_str = notification.get('notification_time')
        notification_number = notification.get('notification_number')
        notification_message = notification.get('notification_message')
        google_id = notification.get('google_id')

        print("tpy:", notification_type, " time: " , notification_time_str, " number ", notification_number, "googleid", google_id)

        if not notification_time_str:
            continue  

        today = datetime.today()

        try:
            send_time = datetime.strptime(f"{today.strftime('%Y-%m-%d')} {notification_time_str}", '%Y-%m-%d %H:%M:%S')
        except:
            print(f"Skipping invalid time format for {google_id}: {notification_time_str}")
            continue

        if send_time < today:
            send_time = send_time.replace(day=today.day + 1)

        job = scheduler.add_job(send_message, 'date', run_date=send_time, args=[notification_number, notification_message, google_id])
        print(f"Scheduled job {job.id} for {send_time} (google_id: {google_id})")

    return "messages set up!"

    

def send_message(notification_number, notification_message, google_id):
    """Send a notification via Twilio."""
    print(f"Sending message for {google_id}...")

    X_RAPID_API_KEY = os.getenv('X_RAPID_API_KEY')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    SID = os.getenv('SID')

    url = "https://api.twilio.com/2010-04-01/Accounts/" + SID + "/Messages.json"

    params = {
        "From":TWILIO_PHONE_NUMBER,
        "Body": notification_message,
        "To":notification_number
    }

    basic = HTTPBasicAuth(SID,X_RAPID_API_KEY)

    response = requests.post(url, auth=basic, data=params)

    if response.status_code == 201:
        print(f"Message sent successfully to {google_id}!")
    else:
        print(f"Failed to send message to {google_id}: {response.status_code} - {response.text}")

