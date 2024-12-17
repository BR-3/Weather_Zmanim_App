from flask import jsonify

from get_api_response.get_location.get_location import get_location_info
from get_api_response.get_weather.get_weather import check_if_get_weather
from get_api_response.get_zmanim.get_zmanim import get_zmanim_info

def get_api_response(date, zip_code):
    input_validation = validate_args(date, zip_code)
    if input_validation is not None:
        return input_validation

    location_info =  get_location_info(zip_code = zip_code)
    zmanim_info = get_zmanim_info(date, zip_code)
    weather_info = check_if_get_weather(location_info['location_key'], date)
    

    return jsonify({
        'location':location_info, 
        'zmanim':zmanim_info, 
        'weather':weather_info
        })


def validate_args(date, zip_code):
    if not date or not zip_code:
       return jsonify({'error': 'Missing zip_code or date'}), 400