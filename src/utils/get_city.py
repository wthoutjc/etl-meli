import requests

def get_city(API_URL: str, USER_ID: str):
    search_url = f"{API_URL}/users/{USER_ID}"
    search_response = requests.get(search_url)
    city = search_response.json()
    if 'address' in city.keys() and 'city' in city['address'].keys(): 
        return city['address']['city']
    return None