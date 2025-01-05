from datetime import datetime
import re
from flask import jsonify

from get_api_response.get_location.get_location import get_location_info
from get_api_response.get_weather.get_weather import check_if_get_weather
from get_api_response.get_zmanim.get_zmanim import get_zmanim_info

def get_api_response(date, zip_code):
    """ This method receives the user inputted date and zip code, validates them, and gets the different api results
    Args:
        date: date entered from user
        zip_code: zip code entered from user
    Returns:
        A json object containing location, zmanim, and weather information"""
    input_validation = validate_args(date, zip_code)
    if input_validation is not None:
        return input_validation

    location_info = get_location_info(zip_code = zip_code)
    zmanim_info = get_zmanim_info(date, zip_code)
    weather_info = check_if_get_weather(location_info['location_key'], date)
    
    return jsonify({
        'location':location_info, 
        'zmanim':zmanim_info, 
        'weather':weather_info
        })


def validate_args(date, zip_code):
    """ validates the date and zip code
    Returns:
        error message if invalid """
    
    # Check if date or zip_code is missing
    if not date or not zip_code:
        return jsonify({'error': 'Missing zip_code or date'}), 400
    
    # Validate zip code (5 digits)
    if not re.match(r'^\d{5}?$', zip_code):
        return jsonify({'error': 'Invalid zip code format. Must be 5 digits (e.g., 12345 or 12345-6789).'}), 400

    # Validate date format (yyyy-mm-dd)
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Must be yyyy-mm-dd.'}), 400