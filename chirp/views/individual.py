__author__ = 'mcherkassky'

from flask import render_template

from chirp import app

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')

@app.route('/')
def index():
    return render_template('index/index.html')

@app.route('/home')
def home():
    return render_template('home/home.html')


@app.route('/create')
def create():
    return render_template('create/create.html')
