from apiclient.discovery import build
from settings import *

import requests
import json
from models import *

service = build('urlshortener', 'v1', developerKey=API_KEY)
api = service.url()

def google_token():
    payload = {'client_id': OAUTH2_CLIENT_ID,
               'client_secret': OAUTH2_CLIENT_SECRET,
               'refresh_token': REFRESH_TOKEN,
               'grant_type': 'refresh_token'}
    response = requests.post('https://accounts.google.com/o/oauth2/token', data=payload)
    return response.json()['access_token']

def shorten(url):
    auth_token = google_token()

    # local_url = Url.create(url)

    payload = {'longUrl': url.redirect}

    response = requests.post('https://www.googleapis.com/urlshortener/v1/url',
                             headers={'Content-Type': 'application/json', 'Authorization': "OAuth {}".format(auth_token)},
                             data=json.dumps(payload))

    return response.json()['id']
