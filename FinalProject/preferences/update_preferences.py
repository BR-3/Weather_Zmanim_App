from flask import jsonify
from db.add_and_update import add_preferences_to_db


def update_user_preferences(data):
    default_location = data.get("defaultLocation")
    default_date = data.get("defaultDate")
    show_weather = data.get("showWeather")
    language = data.get("language")
    notifications = data.get("notifications")

    result = add_preferences_to_db(default_location=default_location, default_date=default_date,show_weather=show_weather, language=language, notifications=notifications)

    if result.upserted_id:  # If an insert happened
        return jsonify({"message": "Preferences saved successfully (new user)!"}), 200
    elif result.modified_count > 0:  # If an update happened
        return jsonify({"message": "Preferences updated successfully!"}), 200
    else:
        return jsonify({"error": "No changes were made to preferences"}), 400