from mongoengine import *
from flask_login import UserMixin

from settings import *
from url import *

class Url(Document):
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

class User(Document, UserMixin):
    name = StringField()
    screen_name = StringField()
    access_token_key = StringField()
    access_token_secret = StringField()

    followers = ListField(StringField())

    @classmethod
    def get(cls, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except:
            return None

class Ad(Document):
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
        response.bid = float(json['cpc'])
        response.budget = float(json['budget'])
        response.start_date = json['start_date']
        response.end_date = json['end_date']
        response.img = json['img']

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

class Offer(Document):
    ad_id = ObjectIdField()
    claimed = BooleanField(default=False)