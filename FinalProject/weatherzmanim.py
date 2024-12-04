from flask import Flask, jsonify, render_template, request, session,redirect, url_for
from google_auth_oauthlib.flow import InstalledAppFlow 
from googleapiclient.discovery import build
import requests, os

from db.add_and_update import add_user_to_db, log_user_visit
from get_location.get_location import get_location_info
from get_weather.get_weather import check_if_within_4_days, get_weather_info
from get_zmanim.get_zmanim import format_date_string, get_zmanim_info
from oauth_login.oauth_login import GOOGLE_CLIENT_SECRETS_FILE, SCOPES, credentials_to_dict

aw_api_key = os.getenv('aw_api_key')

# these will eventually be gotten from front end/user

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")



@app.route('/')
def home():
    user = session.get("user")
    if user:
        log_user_visit("/")
        return render_template('index.html', user = user) 
    return  render_template('index.html', user = None)


@app.route("/login")
def login():
    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for("callback", _external=True)
    authorization_url, state = flow.authorization_url(prompt="consent")

    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    state = session["state"]
    flow =  InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = url_for("callback", _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    session["user"] = user_info
    add_user_to_db(user_info) #add user to db
    log_user_visit('/login')
    return redirect(url_for("home"))



@app.route("/logout")
def logout():
    session.pop("credentials", None)
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/get_weather_and_zmanim') 
def get_weather_and_zmanim():
    # get the data sent from front end
    date = request.args.get('date')
    zip_code = request.args.get('zipCode')
    # print(f"date {date} zip {zip_code}")

    if not date or not zip_code:
       return jsonify({'error': 'Missing zip_code or date'}), 400

    location_info =  get_location_info(zip_code = zip_code)
    zmanim_info = get_zmanim_info(date, zip_code)
    weather_info = get_weather_info(location_info['location_key'], date)
    print(f"weather: {weather_info}")


    return jsonify({
        'location':location_info, 
        'zmanim':zmanim_info, 
        'weather':weather_info
        })




# @app.route('/get_zmanim', methods=['GET'])
# def get_zmanim():
#     print("Request args:", request.args)
#     print(f"the zip code received: {request.args.get('zipCode')}")
#     print(f"the date received: {request.args.get('date')}")
#     try:
#         raw_date = request.args.get('date')
#         zip_code = request.args.get('zipCode')
#         print(f"date {raw_date} and zip {zip_code} in zmanim")

#         if not raw_date or not zip_code:
#             return jsonify({'error': 'Missing zip_code or date'}), 400

#         date = format_date_string(raw_date)
#         zresponse = get_zmanim_info(date, zip_code)
            
#         return zresponse

#     except (requests.exceptions.RequestException, ValueError) as e:
#         return {'error': f"Error retrieving Zmanim data: {str(e)}"}




# @app.route('/get_weather', methods=['GET'])
# def get_weather():
#     date = request.args.get('date')
#     zip_code = request.args.get('zipCode')
#     print(f"date {date} and zip {zip_code} from weather")

#     if not date or not zip_code:
#         return jsonify({'error': 'Missing zip_code or date'}), 400
    
#     # print("Request URL:", request.url)  # Debug: Full URL
#     # print("Request args:", request.args)  # Debug: All query parameters

#     # if not zip_code or not date:
#     #     return jsonify({'error': 'Missing zip_code or date'}), 400

#     within_4_days = check_if_within_4_days(date)
#     if(within_4_days is not None):
#         location_info = get_location_info(zip_code)
#         location_key = location_info['location_key']

#         weather_info = get_weather_info(location_key, within_4_days)

#         return weather_info
#     else:
#         return jsonify({})
    

# @app.route('/process_location', methods=['GET'])
# def process_location():   
#     print(f"zip in locatoin {request.args.get('zipCode')}")  
#     zip_code = request.args.get('zipCode')
#     location_info =  get_location_info(zip_code = zip_code)

#     #return the location info - TODO format it
#     return location_info


