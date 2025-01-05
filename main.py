from flask import Flask, render_template, request, session, redirect, url_for, g

import os

from db.add_and_update import add_user_to_db
from get_api_response.get_weather_and_zmanim import get_api_response
from login.oauth_login import get_authorization_url, handle_oauth_callback, logout_user
from preferences.update_preferences import update_user_preferences
from preferences.notifications.send_notifications import start_scheduler
from setup_app import check_authentication, load_user


aw_api_key = os.getenv('aw_api_key')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")
app.initialized = False


@app.before_request
def setup_app():
    if not app.initialized: 
        app.initialized = True 
        start_scheduler()
    load_user()
    check_authentication()


@app.route('/')
def home():
    return render_template('index.html', user = g.user, preferences=g.preferences) 


@app.route('/get_weather_and_zmanim') 
def get_weather_and_zmanim():
    date = request.args.get('date')
    zip_code = request.args.get('zipCode')
    response = get_api_response(date, zip_code)
    return response


@app.route("/login")
def login():
    return redirect(get_authorization_url())


@app.route("/callback")
def callback():
    user_info = handle_oauth_callback()
    session["user"] = user_info
    add_user_to_db(user_info)
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
def account():
    return render_template('account.html', user=g.user)


@app.route("/preferences")
def preferences():
    return render_template('preferences.html', user=g.user, preferences=g.preferences)


@app.route("/update_preferences", methods=["POST"])
def update_preferences():    
    data = request.get_json()
    return update_user_preferences(data)

    
