__author__ = 'mcherkassky'

from flask import request

from chirp import app
from flask.ext.login import current_user

import json
from chirp.models import *

@app.route('/offers')
def offers():
    offers = current_user.offers
    return offers.to_json()

@app.route('/campaigns', methods=['POST'])
def campaigns():
    data = request.json
    ad = Ad.build_from_json(data)
    ad.save()

    return ad.to_json()

@app.route('/offers/<offer_id>', methods=['POST'])
def offer_id(offer_id):
    offer = Offer.objects.get(id=offer_id)
    offer.claim()
    return offer.to_json()

@app.route('/offers/<offer_id>/url', methods=['GET'])
def offer_url(offer_id):
    offer = Offer.objects.get(id=offer_id)

    url = Url.create(offer.ad.url)
    shortened = url.shortUrl

    return json.dumps({'url': shortened})