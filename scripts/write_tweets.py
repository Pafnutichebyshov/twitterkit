import logging
import os
import sys
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from twitterkit import tweet_access

ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
FILENAME = '/Users/ng/data/2016_election_tweets.tsv'
LANGUAGES = ['en']

TAGS = [
    'jeb',
    'bush',
    'jebbush',
    'jeb2016',
    'bush2016',
    'jebbush2016',
    'donald',
    'trump',
    'donaldtrump',
    'donald2016',
    'trump2016',
    'donaldtrump2016',
    'ben',
    'carson',
    'bencarson',
    'ben2016',
    'carson2016',
    'bencarson2016',
    'ted',
    'cruz',
    'tedcruz',
    'ted2016',
    'cruz2016',
    'tedcruz2016',
    'bernie',
    'sanders',
    'berniesanders',
    'bernie2016',
    'sanders2016',
    'berniesanders2016',
    'hillary',
    'clinton',
    'hillaryclinton',
    'hillary2016',
    'clinton2016',
    'hillaryclinton2016',
]


def main():
    while True:
        try:
            data_streamer = tweet_access.TsvStreamer()
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
            stream = Stream(auth, data_streamer)
            stream.filter(languages=LANGUAGES, track=TAGS, async=True)
        except Exception, e:
            print e.message
            stream.disconnect()


if __name__ == '__main__':
    sys.exit(main())
