__author__ = 'mcherkassky'
from flask import url_for, request, redirect, render_template, session
import tweepy
import requests

from settings import *
from chirp.auth import *
from chirp import app

import json
from chirp.models import *

from oauth2client.client import OAuth2WebServerFlow
flow = OAuth2WebServerFlow(
        client_id=OAUTH2_CLIENT_ID,
        client_secret=OAUTH2_CLIENT_SECRET,
        # The scope is unique per product. We use the AdWords scope here for example.
        # scope='https://adwords.google.com/api/adwords',
        scope='https://www.googleapis.com/auth/urlshortener',
        redirect_uri='http://127.0.0.1:5000/auth_return')


@app.route('/google')
def google_auth():

    auth_uri = flow.step1_get_authorize_url()
    # flow.step2_exchange('4/GqzC8017jROcP1T4bK5ZGnjP1SsA.Qk2PJZW4y6EUshQV0ieZDAr8qVkRhQI')
    return redirect(auth_uri)

@app.route('/auth_return')
def aut_return():
    code = request.args.get('code')

    credentials = flow.step2_exchange(code)
    import pdb; pdb.set_trace()

@app.route('/ly/<url_id>')
def shorten_url(url_id):
    url = Url.objects.get(id=url_id)
    url.record_ip(request.remote_addr)

    return redirect(url.url)

@app.route("/twitter")
def send_token():
    redirect_url = send_twitter_token()

    #this is twitter's url for authentication
    return redirect(redirect_url)

@app.route("/verify")
def get_verification():
    api = get_twitter_verification()

    return redirect(url_for('authenticated'))

@app.route("/authenticated")
def authenticated():
    return render_template('authenticated.html')



@app.route('/offers')
def offers():
    offers = Ad.objects.all()
    return json.dumps([offer.serialize() for offer in offers])

@app.route('/campaigns', methods=['POST'])
def campaigns():
    data = request.json
    import pdb; pdb.set_trace()
    Ad.build_from_json(data)


@app.route('/offers/<offer_id>', methods=['POST'])
def offer_id(offer_id):
    offer = Ad.objects.get(id=offer_id)

    offer.claimed = True
    offer.save()
    return json.dumps(offer.serialize())

@app.route('/offers/<offer_id>/url', methods=['GET'])
def offer_url(offer_id):
    offer = Ad.objects.get(id=offer_id)

    url = Url.create(offer.url)
    shortened = url.shortUrl

    return json.dumps({'url': shortened})
