
import json, requests
import os


def get_location_info(zip_code):
    """
    this method gets the location info based on the zip code 
    from accuweather's postal code api
    Args:
        zip_code: an integer 5 digit zip code
    Returns: 
        location_info: formatted json that gives the location info of the zip code
    """
    aw_api_key = os.getenv('aw_api_key')

    url = f"http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey={aw_api_key}&q={zip_code}"
    location_search = requests.get(url)
    location_search.raise_for_status()

    location_info = process_location_info(json.loads(location_search.content))

    return location_info

def process_location_info(raw_location_info):
    location_data = raw_location_info[0]
    
    final_location_info = {
        "city": location_data["LocalizedName"],
        "state": location_data["AdministrativeArea"]["LocalizedName"],
        "country": location_data["AdministrativeArea"]["CountryID"],
        "zip_code": location_data['PrimaryPostalCode'],
        "location_key": location_data["Key"],
        "time_zone": location_data["TimeZone"]["Name"],
        "time_zone_code": location_data["TimeZone"]["Code"]
    }

    return final_location_info