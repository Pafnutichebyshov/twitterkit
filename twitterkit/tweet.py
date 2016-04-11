import datetime
import os

import tweepy
from tweepy.streaming import StreamListener
import pandas as pd
import psycopg2
import psycopg2.extras
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
        return True


    def on_timeout(self, status_code):
        return True

class StdoutStreamer(TweetStreamer):

    def on_data(self, data):
        print(data)
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
            print(self.num / elapsed_time)
        utils.process_tweet(data._json, self.func_file)
        return True


class PostgresStreamer(TweetStreamer):
    """Stream Twitter data to a postgres table."""
    query = """INSERT INTO {tablename}
        (id_str, created_at, user_id, source, text)
        values (%(id_str)s, %(created_at)s, %(user_id)s, %(source)s, %(text)s)"""

    def __init__(self, *args, **kwargs):
        self.conn = kwargs.pop('conn')
        self.tablename = kwargs.pop('tablename')
        self.query = self.query.format(tablename=self.tablename)
        TweetStreamer.__init__(self, *args, **kwargs)

    def on_status(self, data):
        args = utils.extract_text(data._json)
        try:
            utils.insert_query(self.conn, self.query, args)
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            self.conn.commit()
        return True
