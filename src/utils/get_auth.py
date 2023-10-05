import requests

def get_auth(APP_ID: str, CLIENT_SECRET: str, API_URL: str):
  auth_params = {
      'grant_type': 'client_credentials',
      'client_id': APP_ID,
      'client_secret': CLIENT_SECRET
  }
  auth_response = requests.post(f"{API_URL}/oauth/token", params=auth_params)
  access_token = auth_response.json().get('access_token')
  return access_token