from flask import Flask, jsonify, render_template, request, session, redirect, url_for, g

import os

from db.add_and_update import add_user_to_db, log_user_visit
from db.connection import user_preferences
from get_location.get_location import get_location_info
from get_weather.get_weather import get_weather_info
from get_zmanim.get_zmanim import get_zmanim_info
from login.oauth_login import get_authorization_url, handle_oauth_callback, logout_user
from preferences.update_preferences import update_user_preferences

aw_api_key = os.getenv('aw_api_key')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

protected_paths = ['/account', '/preferences']

# flask global user and preferences to load before each route
@app.before_request
def load_user():
    g.user = session.get("user")
    g.route = request.path
    if g.user:
        log_user_visit(g.route)
        g.preferences = user_preferences.find_one({"google_id": g.user['id']})
    else:
        g.preferences = None
        g.user = None


@app.before_request 
def check_authentication(): 
    if request.path in protected_paths: 
        if not g.user: 
            return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('index.html', user = g.user, preferences=g.preferences) 


@app.route("/login")
def login():
    return redirect(get_authorization_url())


@app.route("/callback")
def callback():
    user_info = handle_oauth_callback()
    session["user"] = user_info # set session
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


@app.route("/update_preferences", methods=["POST"])
def update_preferences():    
    data = request.get_json()
    return update_user_preferences(data)

    
