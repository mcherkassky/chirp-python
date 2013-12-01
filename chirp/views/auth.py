__author__ = 'mcherkassky'

import tweepy
from flask import url_for, request, redirect, render_template, session, g
from flask.ext.login import current_user, login_user
from settings import *
from chirp import app, login_manager
from chirp.models import *

def send_twitter_token():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    try:
        #get the request tokens
        redirect_url = auth.get_authorization_url()
        session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    except tweepy.TweepError:
        print 'Error! Failed to get request token'

    return redirect_url

def get_twitter_verification():
    #get the verifier key from the request url
    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = session['request_token']
    del session['request_token']

    auth.set_request_token(token[0], token[1])

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'

    #now you have access!
    api = tweepy.API(auth)

    #store in a db
    from chirp.models import User

    tweepy_user = api.me()
    followers = [follower.name for follower in api.followers()]
    user = User(name=tweepy_user.name,
                screen_name=tweepy_user.screen_name,
                followers=followers,
                access_token_key=auth.access_token.key,
                access_token_secret=auth.access_token.secret)
    import pdb; pdb.set_trace()
    login_user(user, remember=True)
    user.save()

    return api

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.before_request
def before_request():
    g.user = current_user

from oauth2client.client import OAuth2WebServerFlow
flow = OAuth2WebServerFlow(
        client_id=OAUTH2_CLIENT_ID,
        client_secret=OAUTH2_CLIENT_SECRET,
        # The scope is unique per product. We use the AdWords scope here for example.
        # scope='https://adwords.google.com/api/adwords',
        scope='https://www.googleapis.com/auth/urlshortener',
        redirect_uri='http://127.0.0.1:5000/auth_return')


# @app.route('/google')
# def google_auth():
#
#     auth_uri = flow.step1_get_authorize_url()
#     # flow.step2_exchange('4/GqzC8017jROcP1T4bK5ZGnjP1SsA.Qk2PJZW4y6EUshQV0ieZDAr8qVkRhQI')
#     return redirect(auth_uri)
#
# @app.route('/auth_return')
# def aut_return():
#     code = request.args.get('code')
#
#     credentials = flow.step2_exchange(code)

@app.route('/ly/<url_id>')
def shorten_url(url_id):
    url = Url.objects.get(id=url_id)
    url.record_ip(request.remote_addr)

    return redirect(url.url)

@app.route("/twitter")
def send_token():
    import pdb; pdb.set_trace()
    if g.user is not None and g.user.is_authenticated():

        return redirect(url_for('authenticated'))
    else:
        redirect_url = send_twitter_token()

        #this is twitter's url for authentication
        return redirect(redirect_url)

@app.route("/verify")
def get_verification():
    api = get_twitter_verification()

    return redirect(url_for('authenticated'))

@app.route("/authenticated")
def authenticated():
    return render_template('authenticated.html')
