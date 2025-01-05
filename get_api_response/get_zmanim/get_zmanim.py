from flask import g
from get_api_response.get_zmanim.zmanim_format_methods import format_zmanim_result_date, format_date_for_zmanim_api, get_day_of_week, format_zmanim_response
import requests
from db.connection import notifications_collection


def get_zmanim_info(date, zip_code):
    """
    This method connects to the OU's zmanim api and returns zmanim based on inputted date and zip code
    Args:
        date: date entered by user
        zip_code: zip code entered by user
    Returns:
        JSON object with zmanim results or empty JSON object
    """
    date = format_date_for_zmanim_api(date)

    url = f"https://db.ou.org/zmanim/getCalendarData.php?mode=day&dateBegin={date}&zipCode={zip_code}"

    try: 
        response = requests.get(url)
        response.raise_for_status()

        zmanim_info = format_zmanim_response(response.json())
        return zmanim_info
    except:
        print(f"Error fetching zmanim data")
        return {}