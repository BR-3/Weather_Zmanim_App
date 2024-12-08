from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os

from db.add_and_update import add_user_to_db, log_user_visit
from db.connection import user_preferences
from get_location.get_location import get_location_info
from get_weather.get_weather import get_weather_info
from get_zmanim.get_zmanim import get_zmanim_info
from oauth_login.oauth_login import get_authorization_url, handle_oauth_callback, logout_user

aw_api_key = os.getenv('aw_api_key')


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")



@app.route('/')
def home():
    user = session.get("user")
    if user:
        log_user_visit("/")
        preferences = user_preferences.find_one({"google_id": user['id']})
        print('preferences: ', preferences)
        return render_template('index.html', user = user, preferences=preferences) 
    return  render_template('index.html', user = None)


@app.route("/login")
def login():
    return redirect(get_authorization_url())


@app.route("/callback")
def callback():
    user_info = handle_oauth_callback()
    session["user"] = user_info
    add_user_to_db(user_info) #add user to db
    log_user_visit('/login')
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
def account():
    user = session.get("user")
    if not user:
        return redirect(url_for('login'))
    log_user_visit("/account")
    return render_template('account.html', user=user)


@app.route("/preferences")
def preferences():
    user = session.get("user")
    if not user:
        return redirect(url_for('login'))
    log_user_visit("/preferences")
    return render_template('preferences.html', user=user)


@app.route("/update_preferences", methods=["POST"])
def update_preferences():
    user = session.get("user")
    if not user:
        return jsonify({"error": "User not logged in"}), 400
    
    data = request.get_json()

    default_location = data.get("defaultLocation")
    show_weather = data.get("showWeather")
    language = data.get("language")
    reminders = data.get("reminders")
    notifications = data.get("notifications")

    print(f"Location: {default_location}, Show Weather: {show_weather}, Language: {language}, Reminders: {reminders}, Notifications: {notifications}")

    result = user_preferences.update_one(
        {"google_id":session['user']['id']},  
        {"$set": {
            "default_location": default_location,
            "show_weather": show_weather,
            "language": language,  # Save the language preference
            "reminders": reminders,  # Save the reminder preference
            "notifications": notifications
        }},
        upsert=True
    )

    if result.upserted_id:  # If an insert happened
        return jsonify({"message": "Preferences saved successfully (new user)!"}), 200
    elif result.modified_count > 0:  # If an update happened
        return jsonify({"message": "Preferences updated successfully!"}), 200
    else:
        return jsonify({"error": "No changes were made to preferences"}), 400

@app.route('/get_weather_and_zmanim') 
def get_weather_and_zmanim():
    date = request.args.get('date')
    zip_code = request.args.get('zipCode')

    if not date or not zip_code:
       return jsonify({'error': 'Missing zip_code or date'}), 400

    location_info =  get_location_info(zip_code = zip_code)
    zmanim_info = get_zmanim_info(date, zip_code)
    weather_info = get_weather_info(location_info['location_key'], date)

    return jsonify({
        'location':location_info, 
        'zmanim':zmanim_info, 
        'weather':weather_info
        })


