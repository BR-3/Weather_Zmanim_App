
from flask import g, json, jsonify, session
from db.connection import users_collection, user_preferences
from datetime import datetime


def add_user_to_db(user_info):
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
    # current_preferences = user_preferences.find_one({"google_id": g.user['id']})

    new_data = {
        "default_location": default_location,
        "default_date": default_date,
        "show_weather": show_weather,
        "language": language,
        "notifications": notifications,
        "notification_number": notification_number
    }

    # if current_preferences and all(current_preferences.get(key) == value for key, value in new_data.items()):
    #     print("no changes detected")
    #     return {"message": "No changes detected", "modified_count": 0}
    
    result = user_preferences.update_one(
            {"google_id": g.user['id']},  
            {"$set": new_data },
            upsert=True
        )
    return result