import json
import os

import attrdict
import tweepy
from tweepy.streaming import StreamListener
import unicodecsv as csv

from twitterkit import utils


def getSession(auth_keys=None):
    access_token_key = os.environ['ACCESS_TOKEN_KEY']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    api_session = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api_session.set_access_token(access_token_key, access_token_secret)
    return api_session


class TweetStreamer(StreamListener):

    def on_error(self, status_code):
        return False


class StdoutStreamer(TweetStreamer):

    def on_data(self, data):
        print data
        return True


class TsvStreamer(TweetStreamer):
    def __init__(self, *args, **kwargs):
        self.filename = kwargs.pop('filename')
        TweetStreamer.__init__(self, *args, **kwargs)

    def on_data(self, data):
        data = attrdict.AttrDict(json.loads(data))
        if not hasattr(data, 'text'):
            return True
        with open(self.filename, 'a') as f:
            if data.text.startswith('RT @'):
                return True
            csv_writer = csv.writer(f, delimiter='\t')
            csv_writer.writerows(self._getAttributes(data))
        return True

    def on_status(self, data):
        with open(self.filename, 'a') as f:
            if data.text.startswith('RT @'):
                return True
            csv_writer = csv.writer(f, delimiter='\t')
            csv_writer.writerow(self.getAttributes(data))
        return True

    def _getAttributes(self, data):
        created_at = data.created_at
        _id = data.id
        user = data.user.screen_name
        text = data.text.lower()
        return _id, created_at, user, text


class JsonStreamer(TweetStreamer):
    def __init__(self, *args, **kwargs):
        self.filename = kwargs.pop('filename')
        TweetStreamer.__init__(self, *args, **kwargs)

    def on_status(self, data):
        with open(self.filename, 'a') as f:
            utils.write_json(data._json, f)
        return True
