from flask import Flask, jsonify, render_template, request, session, redirect, url_for, g
import os

import requests

from db.add_and_update import add_user_to_db, log_user_visit
from db.connection import user_preferences
from get_location.get_location import get_location_info
from get_weather.get_weather import get_weather_info
from get_zmanim.get_zmanim import get_zmanim_info
from login.oauth_login import get_authorization_url, handle_oauth_callback, logout_user

aw_api_key = os.getenv('aw_api_key')


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# flask global user and preferences to load before each route
@app.before_request
def load_user():
    g.user = session.get("user")
    if g.user:
        g.preferences = user_preferences.find_one({"google_id": g.user['id']})
    else:
        g.preferences = None

@app.route('/')
def home():
    if g.user:
        log_user_visit("/")
        return render_template('index.html', user = g.user, preferences=g.preferences) 
    return  render_template('index.html', user = None, preferences=None)


@app.route("/login")
def login():
    return redirect(get_authorization_url())


@app.route("/callback")
def callback():
    user_info = handle_oauth_callback()
    session["user"] = user_info # set session
    add_user_to_db(user_info)
    log_user_visit('/login')
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
def account():
    if not g.user:
        return redirect(url_for('login'))
    log_user_visit("/account")
    return render_template('account.html', user=g.user)


@app.route("/preferences")
def preferences():
    if not g.user:
        return redirect(url_for('login'))
    log_user_visit("/preferences")
    return render_template('preferences.html', user=g.user, preferences=g.preferences)


@app.route("/update_preferences", methods=["POST"])
def update_preferences():
    if not g.user:
        return jsonify({"error": "User not logged in"}), 400
    
    data = request.get_json()

    default_location = data.get("defaultLocation")
    default_date = data.get("defaultDate")
    show_weather = data.get("showWeather")
    language = data.get("language")
    notifications = data.get("notifications")

    print(f"Location: {default_location}, date: {default_date}, Show Weather: {show_weather}, Language: {language}, Notifications: {notifications}")
    result = user_preferences.update_one(
        {"google_id": g.user['id']},  
        {"$set": {
            "default_location": default_location,
            "default_date": default_date,
            "show_weather": show_weather,
            "language": language,
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

    if g.preferences['show_weather']== True:
       weather_info = get_weather_info(location_info['location_key'], date)
    else:
        weather_info = {}

    return jsonify({
        'location':location_info, 
        'zmanim':zmanim_info, 
        'weather':weather_info
        })


from requests.auth import HTTPBasicAuth
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
scheduler = BackgroundScheduler()
@app.route("/twilio")
def twilio():
    print("received request to schedule message")
    send_time = datetime(2024, 12, 9, 12, 20)  # Example: December 8, 2024, at 4 pm
    scheduler.add_job(send_message, 'date', run_date=send_time)
    print("message scheduled for ", send_time)
    scheduler.start()

    return "success!"

    

def send_message():
    print("executing message send")
    X_RAPID_API_KEY = '6d2caefdfe96c5737a7b5b8e9f3f75f9'
    TWILIO_PHONE_NUMBER = '+19177465798'
    TO_NUMBER = '+19296097511'
    SID = 'AC2971234654291b575ae9c6c249759e49'
    MESSAGE_BODY = 'This is a one time scheduled message.'

    url = "https://api.twilio.com/2010-04-01/Accounts/" + SID + "/Messages.json"

    params = {
        "From":TWILIO_PHONE_NUMBER,
        "Body":MESSAGE_BODY,
        "To":TO_NUMBER
    }
    basic = HTTPBasicAuth(SID,X_RAPID_API_KEY)
    print(f"Sending request to {url} with params: {params}")
    response = requests.post(url, auth=basic, data=params)

    if response.status_code == 201:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")