
from flask import session
from db.connection import users_collection
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