__author__ = 'mcherkassky'

from flask import request

from chirp import app

import json
from chirp.models import *

@app.route('/offers')
def offers():
    offers = Ad.objects.all()
    return json.dumps([offer.serialize() for offer in offers])

@app.route('/campaigns', methods=['POST'])
def campaigns():
    data = request.json
    ad = Ad.build_from_json(data)
    ad.save()

    return ad.to_json()

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