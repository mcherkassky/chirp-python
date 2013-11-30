__author__ = 'mcherkassky'

from flask import Flask

import db

import settings


app = Flask(__name__)

app.debug = True
app.secret_key = 'zefr'
app.config.from_object(settings)

from views.individual import *
from views.views import *