from mongoengine import *
from flask_login import UserMixin
import json

from bs4 import *
from bson import json_util

from settings import *
from url import *

from datetime import datetime

def url_image(url):
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data)

    img = soup.find('meta', attrs={'property': 'og:image'})['content']

    return img

def serialize(dict):
    dict['id'] = str(dict['_id'])
    dict.pop('_id')
    return dict

class CustomQuerySet(QuerySet):
    def to_json(self, *args, **kwargs):
        return json_util.dumps([serialize(obj) for obj in self.as_pymongo()], *args, **kwargs)

class Base(object):
    meta = {'allow_inheritance': True,
            'queryset_class': CustomQuerySet}

    def to_json(self, *args, **kwargs):
        return json_util.dumps(serialize(self.to_mongo()),  *args, **kwargs)

    @classmethod
    def build_from_json(cls):
        pass

class Url(Document, Base):
    # id = SequenceField(primary_key=True)
    url = URLField()
    clicks = IntField(default=0)
    short = URLField()
    ip = DictField()

    def record_ip(self, ip):
        dict_ip = ip.replace('.', '-')
        try:
            self.ip[dict_ip] += 1
        except:
            self.ip[dict_ip] = 0
        self.save()

    @classmethod
    def create(cls, longUrl):
        if not longUrl.startswith('http'):
            longUrl = '%s%s' % ('http://', longUrl)

        url = cls(url=longUrl)
        url.save()
        return url

    @property
    def shortUrl(self):
        if self.short:
            return self.short
        else:
            self.short = shorten(self)
            self.save()
            return self.short

    @property
    def redirect(self):
        return HOST + '/ly/' + str(self.id)
    # @property
    # def hex(self):
    #     return base64.urlsafe_b64encode(str(self.id))

class User(Document, UserMixin, Base):
    name = StringField()
    screen_name = StringField()
    access_token_key = StringField()
    access_token_secret = StringField()

    followers = ListField(StringField())

    @classmethod
    def get(cls, user_id):
        try:
            user = cls.objects.get(id=user_id)
            return user
        except:
            return None

    def create_offers(self):
        ads = Ad.objects()
        for ad in ads:
            Offer.create(self, ad)

    @property
    def offers(self):
        return Offer.objects.filter(user_id=self.id, claimed=False)

    @property
    def claimed_offers(self):
        return Offer.objects.filter(user_id=self.id, claimed=True)

class Ad(Document, Base):
    url = StringField()
    img = StringField()

    bid = FloatField()
    budget = FloatField()

    title = StringField()

    start_date = DateTimeField()
    end_date = DateTimeField()

    owner = ObjectIdField()

    claimed = BooleanField(default=False)

    @classmethod
    def build_from_json(cls, json):
        response = cls()
        response.url = json['url']

        response.img = url_image(json['url'])
        response.bid = float(json['cpc'])
        response.budget = float(json['budget'])
        response.title = json['title']
        response.start_date = datetime.strptime(json['start_date'].split('T')[0], '%Y-%m-%d')
        response.end_date = datetime.strptime(json['end_date'].split('T')[0], '%Y-%m-%d')

        return response

    def serialize(self):
        response = dict()
        response['url'] = self.url
        response['img'] = self.img
        response['bid'] = self.bid
        response['title'] = self.title
        response['id'] = str(self.id)
        response['claimed'] = self.claimed

        return response

class Offer(Document, Base):
    ad_id = ObjectIdField()
    user_id = ObjectIdField()
    claimed = BooleanField(default=False)

    @classmethod
    def create(cls, user, ad):
        offer = cls(user_id=user.id, ad_id=ad.id)
        offer.save()

    def claim(self):
        self.claimed = True
        self.save()
