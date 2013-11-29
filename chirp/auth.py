import tweepy
from flask import session, request
from settings import *

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
    from models import User

    tweepy_user = api.me()
    followers = [follower.name for follower in api.followers()]
    user = User(name=tweepy_user.name,
                screen_name=tweepy_user.screen_name,
                followers=followers,
                access_token_key=auth.access_token.key,
                access_token_secret=auth.access_token.secret)
    user.save()

    return api