import datetime
import os

import tweepy
from tweepy.streaming import StreamListener
import pandas as pd
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


class JsonStreamer(TweetStreamer):
    def __init__(self, *args, **kwargs):
        self.filename = kwargs.pop('filename')
        TweetStreamer.__init__(self, *args, **kwargs)

    def on_status(self, data):
        with open(self.filename, 'a') as f:
            utils.write_json(data._json, f)
        return True


class TsvStreamer(TweetStreamer):
    def __init__(self, *args, **kwargs):
        self.output = kwargs.pop('output')
        self.func = kwargs.pop('func')
        self.monitor = kwargs.pop('monitor')
        TweetStreamer.__init__(self, *args, **kwargs)
        self.func_file = {}
        self.num = 0.0
        self.start = datetime.datetime.utcnow()
        for table, func in self.func.items():
            output_file = '{}_{}.tsv'.format(self.output, table)
            f = open(output_file, 'a')
            fieldnames = func({})
            csv_writer = csv.DictWriter(f, fieldnames, delimiter='\t')
            if not os.path.getsize(output_file):
                csv_writer.writeheader()
            self.func_file[table] = (func, csv_writer)


    def on_status(self, data):
        if self.monitor:
            now = datetime.datetime.utcnow()
            _diff = (now - pd.to_datetime(data._json['created_at'])).total_seconds()
            elapsed_time = (now - self.start).total_seconds()
            self.num += 1
            print('lag: {}'.format(_diff))
            print self.num / elapsed_time
        utils.process_tweet_2(data._json, self.func_file)
        return True
