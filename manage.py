from datetime import date, timedelta
from random import randint, choice
from logging import info

from flask import url_for
from flask.ext.script import Manager, Shell

from chirp import app

from mongoengine import *

from chirp import models
from chirp.models import *

manager = Manager(app)

def _make_context():
    return {'app': app, 'models': models}

@manager.command
def delete_and_bootstrap():
    Url.objects.delete()
    User.objects.delete()
    Ad.objects.delete()
    Offer.objects.delete()

    drose = Ad(url="http://www.youtube.com/watch?v=GOtxJrzp6ls",
               img="http://img.youtube.com/vi/GOtxJrzp6ls/0.jpg",
               title="Derrick Rose Adidas D Rose 4.0",
               bid=.75)
    drose.save()

    usa = Ad(url="http://www.youtube.com/watch?v=GBPDnUil75c",
             img="http://img.youtube.com/vi/GBPDnUil75c/0.jpg",
             title="USMNT World Cup Campaign",
             bid=1.10)
    usa.save()

    beyonce = Ad(url="http://www.youtube.com/watch?v=Ob7vObnFUJc",
                 img="http://img.youtube.com/vi/Ob7vObnFUJc/0.jpg",
                 title="Beyonce Love On Top Music Video",
                 bid=.75)
    beyonce.save()

    print('done')


if __name__ == "__main__":
    manager.add_command('shell', Shell(make_context=_make_context))
    manager.run()



