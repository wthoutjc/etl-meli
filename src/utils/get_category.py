import requests

def get_category(API_URL: str, CATEGORY_ID: str):
  search_url = f"{API_URL}/categories/{CATEGORY_ID}"
  search_response = requests.get(search_url)
  categories = search_response.json()
  return categories