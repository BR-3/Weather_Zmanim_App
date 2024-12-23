from flask import g
from get_api_response.get_zmanim.zmanim_format_methods import format_date, format_date_string, get_day_of_week, format_zmanim_response
import requests
from db.connection import notifications_collection


def get_zmanim_info(date, zip_code):
    date = format_date_string(date)

    url = f"https://db.ou.org/zmanim/getCalendarData.php?mode=day&dateBegin={date}&zipCode={zip_code}"

    try: 
        response = requests.get(url)
        response.raise_for_status()

        zmanim_info = format_zmanim_response(response.json())
        add_notifications_to_db(zmanim_info)
        return zmanim_info
    except:
        print(f"Error fetching zmanim data")
        return {}

def add_notifications_to_db(zmanim_info):
    if g.preferences:
        notifications = g.preferences.get('notifications')
        if notifications is not None:
            if('shkia' in notifications):
                notification_info = {
                    'notification_type': 'shkia',
                    'notification_time': zmanim_info['zmanim']['sunset'],
                    'notification_number': g.preferences.get('notification_number'),
                    'notification_message': 'It\'s almost shkia!'
                }
                result = notifications_collection.update_one(
                    {'google_id': g.user['id']},
                    { '$set': notification_info },
                    upsert=True
                )
                print(result)
            print(zmanim_info)
        else:
            print("no notifications, its null")
    else:
        print("no preferences")

