from datetime import datetime
import os
import requests
from requests.auth import HTTPBasicAuth
from db.add_and_update import add_notification_to_db


def get_send_time(notification_time_str):
    """gets the send time based on today's date for notification messages"""
    today = datetime.today()

    try:
        send_time = datetime.strptime(f"{today.strftime('%Y-%m-%d')} {notification_time_str}", '%Y-%m-%d %H:%M:%S')
    except:
        print(f"Skipping invalid time format for: {notification_time_str}")

    if send_time < today:
        send_time = send_time.replace(day=today.day + 1)

    return send_time

       
def add_zmanim_notifications_to_db(id, zmanim, number, notifications, notifications_collection):
    """Adds notifications to the notification database for each type of notification in notification preferences"""
    if 'shkia' in notifications:
        add_notification_to_db(id, type="shkia", time=zmanim['zmanim']['sunset'], number= number, message="It's almost shkia!", notifications_collection=notifications_collection)
    if 'sunrise' in notifications:
        add_notification_to_db(id, type="sunrise", time=zmanim['zmanim']['sunrise'], number= number, message="It's almost sunrise!", notifications_collection=notifications_collection)
    if 'szsMA' in notifications:
        add_notification_to_db(id, type="szsMA", time=zmanim['zmanim']['sof_zman_shema_ma'], number= number, message="It's almost sof zman shema according to the M\"A!", notifications_collection=notifications_collection)
    if 'szsGRA' in notifications:
        add_notification_to_db(id, type="szsGRA", time=zmanim['zmanim']['sof_zman_shema_gra'], number= number, message="It's almost sof zman shema according to the Gra!", notifications_collection=notifications_collection)
    if 'sztMA' in notifications:
        add_notification_to_db(id, type="sztMA", time=zmanim['zmanim']['sof_zman_tefila_ma'], number= number, message="It's almost sof zman tefila according to the M\"A!", notifications_collection=notifications_collection)
    if 'sztGRA' in notifications:
        add_notification_to_db(id, type="sztGRA", time=zmanim['zmanim']['sof_zman_tefila_gra'], number= number, message="It's almost sof zman tefila according to the GRA!", notifications_collection=notifications_collection)
    if 'alos' in notifications:
        add_notification_to_db(id, type="alos", time=zmanim['zmanim']['alos_ma'], number= number, message="It's almost alos!", notifications_collection=notifications_collection)
    if 'talis' in notifications:
        add_notification_to_db(id, type="talis", time=zmanim['zmanim']['talis_ma'], number= number, message="It's time for talis!", notifications_collection=notifications_collection)
    if 'chatzos' in notifications:
        add_notification_to_db(id, type="chatzos", time=zmanim['zmanim']['chatzos'], number= number, message="It's almost chatzos!", notifications_collection=notifications_collection)
    if 'minchaGedola' in notifications:
        add_notification_to_db(id, type="mincha_gedola", time=zmanim['zmanim']['mincha_gedola_ma'], number= number, message="It's almost mincha gedola!", notifications_collection=notifications_collection)
    if 'minchaKetana' in notifications:
        add_notification_to_db(id, type="mincha_ketana", time=zmanim['zmanim']['mincha_ketana_gra'], number= number, message="It's almost mincha ketana!", notifications_collection=notifications_collection)
    if 'plagHamincha' in notifications:
        add_notification_to_db(id, type="plag_hamincha", time=zmanim['zmanim']['plag_mincha_ma'], number= number, message="It's almost plag hamincha!", notifications_collection=notifications_collection)
    if 'degreees595' in notifications:
        add_notification_to_db(id, type="degrees595", time=zmanim['zmanim']['tzeis_595_degrees'], number= number, message="It's tzeis 595 degrees!", notifications_collection=notifications_collection)
    if 'min42' in notifications:
        add_notification_to_db(id, type="min42", time=zmanim['zmanim']['tzeis_42_minutes'], number= number, message="It's tzeis 42 minutes!", notifications_collection=notifications_collection)
    if 'degreees850' in notifications:
        add_notification_to_db(id, type="degrees850", time=zmanim['zmanim']['tzeis_850_degrees'], number= number, message="It's tzeis 850 degrees!", notifications_collection=notifications_collection)
    if 'min72' in notifications:
        add_notification_to_db(id, type="min72", time=zmanim['zmanim']['tzeis_72_minutes'], number= number, message="It's tzeis 72 minutes!", notifications_collection=notifications_collection)
    if 'dafYomi' in notifications:
        masechta = zmanim['dafYomi']['masechta']
        daf = zmanim['dafYomi']['daf']
        daf_yomi = f"Maseches {masechta} daf {daf}"
        add_notification_to_db(id, type="daf_yomi", time="14:28:30", number= number, message=f"Today's daf is {daf_yomi}", notifications_collection=notifications_collection)



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

