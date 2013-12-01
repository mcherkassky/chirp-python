__author__ = 'mcherkassky'

from flask import Flask
from flask.ext.login import LoginManager

import db

import settings

app = Flask(__name__)

app.debug = True
app.secret_key = 'zefr'
app.config.from_object(settings)

login_manager = LoginManager()
login_manager.init_app(app)

#import views
from views.auth import *
from views.individual import *
from views.api import *