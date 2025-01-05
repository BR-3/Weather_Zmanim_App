from flask import jsonify
from db.add_and_update import add_preferences_to_db


def update_user_preferences(data):
    """
    receives updated user preferences to add them to the database
    Args:
        data: preferences sent through a get request
    Returns: 
        json message of success or error"""
    default_location = data.get("defaultLocation")
    default_date = data.get("defaultDate")
    show_weather = data.get("showWeather")
    language = data.get("language")
    notifications = data.get("notifications")
    notification_number = data.get("notificationNumber")

    result = add_preferences_to_db(default_location=default_location, default_date=default_date,show_weather=show_weather, language=language, notifications=notifications, notification_number=notification_number)

    if result.upserted_id:
        return jsonify({"message": "Preferences saved successfully (new user)!"}), 200
    elif result.modified_count > 0:
        return jsonify({"message": "Preferences updated successfully!"}), 200
    else:
        return jsonify({"message": "No changes were made to preferences"}), 304