
from flask import g, json, session
from db.connection import users_collection, user_preferences
from datetime import datetime


def add_user_to_db(user_info):
    """ Adds the user to the database (or updates if the user exists)"""
    user_info['last_login'] = datetime.now()
    
    users_collection.update_one(
        {'google_id': user_info['id']},
        {'$set': user_info},
        upsert=True
    )


def log_user_visit(page):
    """
    Logs a user visit to the specified page.

    Args:
        page (str): The page visited by the user.
    """

    visit_time = datetime.now()
    id = session['user']['id']

    users_collection.update_one(
        {"google_id": id},
        {"$push": {"user_event_log": {"vist_time": visit_time, "page": page}}}
    )


def add_preferences_to_db(default_location, default_date, show_weather, language, notifications, notification_number):
    """Adds the user's preferences from the preference form into the preferences database"""
    new_data = {
        "default_location": default_location,
        "default_date": default_date,
        "show_weather": show_weather,
        "language": language,
        "notifications": notifications,
        "notification_number": notification_number
    }

    result = user_preferences.update_one(
            {"google_id": g.user['id']},  
            {"$set": new_data },
            upsert=True
        )
    return result


def add_notification_to_db(id, type, time, number, message, notifications_collection):
    """ Adds the notification information for any given notification into the notifications database """
    notification_info = {
        'google_id': id,
        'notification_type': type,
        'notification_time': time,
        'notification_number': number,
        'notification_message': message
    }
    result = notifications_collection.insert_one({
        **notification_info
    })
    return result