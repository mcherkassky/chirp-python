__author__ = 'mcherkassky'

from flask import Flask, url_for, request, session, redirect, render_template, g

import db

import settings


app = Flask(__name__)

app.debug = True
app.secret_key = 'zefr'
app.config.from_object(settings)

from chirp import views