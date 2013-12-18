from mongoengine import *
from flask_login import UserMixin
import json

from bs4 import *
from bson import json_util, ObjectId, DBRef
from mongoengine.dereference import DeReference

from settings import *
from url import *

from datetime import datetime
from json import JSONEncoder

def mongoencode(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, DBRef):
        obj_db = DeReference()({'data': obj})['data']
        return obj_db._data
    else:
        return obj._data

def url_image(url):
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data)

    img = soup.find('meta', attrs={'property': 'og:image'})['content']

    return img

class CustomQuerySet(QuerySet):
    # def to_json(self, *args, **kwargs):
    #     import pdb; pdb.set_trace()
    #     return json_util.dumps([serialize(obj) for obj in self.as_pymongo()], *args, **kwargs)
    def json(self):
        return '[' + ','.join([obj.json() for obj in self]) + ']'

class Base(object):
    meta = {'allow_inheritance': True,
            'queryset_class': CustomQuerySet}

    # def serialize(self, *args, **kwargs):
    #     import pdb; pdb.set_trace()
        # return json_util.dumps(serialize(self.to_mongo()),  *args, **kwargs)

    def json(self):
        return json.dumps(self, default=mongoencode)

    @classmethod
    def build_from_json(cls):
        print 'poop'

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

    def create_offer(self, ad):
        Offer.create(self, ad)

    @property
    def offers(self):
        return Offer.objects.filter(user_id=self.id)

    # @property
    # def claimed_offers(self):
    #     return Offer.objects.filter(user_id=self.id, claimed=True)

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

    def create_offers(self):
        users = self.eligible_users()
        for user in users:
            user.create_offer(self)

    def eligible_users(self):
        return User.objects.all()

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
    ad = ReferenceField('Ad')

    user_id = ObjectIdField()

    claimed = BooleanField(default=False)

    @classmethod
    def create(cls, user, ad):
        offer = cls(user_id=user.id,
                    ad=ad)
        offer.save()

    # @property
    # def ad(self):
    #     return Ad.objects.get(id=self.ad_id)

    def claim(self):
        self.claimed = True
        self.save()
