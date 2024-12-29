from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from dotenv import load_dotenv

from get_api_response.get_zmanim.get_zmanim import get_zmanim_info
from preferences.notifications.notifications_helper_methods import add_zmanim_notifications_to_db, get_send_time, send_message
from db.connection import user_preferences, notifications_collection

load_dotenv()

scheduler = BackgroundScheduler()

def setup_daily_notifications():
    today = datetime.now()
    setup_notifications(user_preferences, notifications_collection)

# Schedule to run every day at midnight
scheduler.add_job(setup_daily_notifications, CronTrigger(hour=0, minute=0, second=0))


def setup_notifications(user_preferences, notifications_collection):
    # clear previous day's notifications
    notifications_collection.delete_many({})

    # load notification requests from all user preferences
    get_notification_requests(user_preferences, notifications_collection)

    # set up sending notifications from the notifications collection
    set_notification_send(notifications_collection)
    



def get_notification_requests(user_preferences, notifications_collection):
    preferences_cursor = user_preferences.find()
    today = datetime.now()
    date = today.strftime('%Y-%m-%d')


    for preference in preferences_cursor:
        id = preference.get('google_id')
        notifications = preference.get('notifications')
        zip_code = preference.get('default_location')
        number = preference.get('notification_number')
        if notifications is not None and zip_code is not None and number is not None and zip_code != '' and number != '' and notifications != []:
            zmanim = get_zmanim_info(date, zip_code)
            add_zmanim_notifications_to_db(id, zmanim, number, notifications, notifications_collection)
            print("about the preference: ", notifications, zip_code, zmanim)


def set_notification_send(notifications_collection):  
    notifications_cursor = notifications_collection.find()
    for notification in notifications_cursor:
        google_id = notification.get('google_id')
        notification_type = notification.get('notification_type')
        notification_time_str = notification.get('notification_time')
        notification_number = notification.get('notification_number')
        notification_message = notification.get('notification_message')

        send_time = get_send_time(notification_time_str)

        job = scheduler.add_job(send_message, 'date', run_date=send_time, args=[notification_number, notification_message, google_id])
        print(f"Scheduled job {job.id} for {send_time} (google_id: {google_id})")

 
def start_scheduler():
    scheduler.start()