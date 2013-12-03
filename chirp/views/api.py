__author__ = 'mcherkassky'

from flask import request

from chirp import app
from flask.ext.login import current_user

import json
from chirp.models import *

@app.route('/offers')
def offers():
    offers = current_user.offers
    ads = Ad.objects.filter(id__in=[offer.ad_id for offer in offers])
    return ads.to_json()

@app.route('/campaigns', methods=['POST'])
def campaigns():
    data = request.json
    ad = Ad.build_from_json(data)
    ad.save()

    return ad.to_json()

@app.route('/offers/<ad_id>', methods=['POST'])
def offer_id(ad_id):
    ad = Ad.objects.get(id=ad_id)
    offer = Offer.objects.get(ad_id=ad.id, user_id=current_user.id)
    offer.claim()
    return ad.to_json()

@app.route('/offers/<offer_id>/url', methods=['GET'])
def offer_url(offer_id):
    offer = Ad.objects.get(id=offer_id)

    url = Url.create(offer.url)
    shortened = url.shortUrl

    return json.dumps({'url': shortened})