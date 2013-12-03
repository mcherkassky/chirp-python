__author__ = 'mcherkassky'

from flask import render_template
from flask.ext.login import login_required

from chirp import app


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')


@app.route('/')
def index():
    return render_template('index/index.html')


@app.route('/home')
@login_required
def home():
    return render_template('base/base.html')


@app.route('/create')
@login_required
def create():
    return render_template('create/create.html')
