import pdb
import twitter
import tweetstream
import json
import tweepy

consumer_key='13wjAb9GLLP3O9onQuM1Ew'
consumer_secret='agpSyJzyMnvIBEkfaCdGv2EoIKWVNo0qYkjuGoMbjjg'
access_key='1552105075-fDyEqGl2qTOgFzdfJZAOAkZwlXdq7AXRxs2OZm4'
access_secret='hbEZp3o075kvf7DS2v3RGhE9CGAzjzIVnqLI16w5kDGvK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

    def on_data(self, tweet):
        tweet = json.loads(tweet)
        if tweet['geo'] is not None:
            print tweet['text']


    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
import pdb; pdb.set_trace()
sapi.filter(track=['coca cola', 'pepsi', 'nike', 'adidas', "mcdonald's",
                   'burger king', 'mercedes', 'bmw', 'audi', 'gilette',
                   'microsoft', 'visa', 'walmart', 'mastercard', 'disney',
                   'samsung', 'louis vuitton', 'zara', 'hermes', 'starbucks',
                   'h&m', 'siemens', 'ikea', 'target', 'red bull', 'nissan',
                   'prada', 'abercrombie', 'j crew', 'lululemon', 'ugg'
                   'armani', 'chipotle', 'the north face', 'real madrid',
                   'godiva', "macy's", 'nordstrom', 'sears', 'sephora',
                   'urban outfitters', 'vans', "victoria's secret",
                   'victorinox', 'oakley', 'ray ban', 'madewell', 'lacoste',
                   'lego', 'lenscrafters', "levi's", 'lindt', 'puma'])
# sapi.filter(track=['Gandolfini'])


# stream = tweetstream.SampleStream("mcherkassky@gmail.com", "mAbel1127")
# import pdb; pdb.set_trace()
# for tweet in stream:
#     print tweet
#
# pdb.set_trace()
