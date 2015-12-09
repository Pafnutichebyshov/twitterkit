import logging
import os
import sys
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#TODO: make these functions. as is, just importing module will fail if these aren't set.
ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
FILENAME = '/Users/ng/data/2016_election_tweets.tsv'
LANGUAGES = ['en']


class TweetStreamer(StreamListener):

    def on_error(self, status_code):
        print status_code
        return False


class StdoutStreamer(TweetStreamer):

    def on_data(self, data):
        print data
        return True


class TsvStreamer(TweetStreamer):

    def on_data(self, data):
        with open(FILENAME, 'a') as f:
            f.write(data)
        return True


def main():
    while True:
        try:
            stdout_streamer = TsvStreamer()
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
            stream = Stream(auth, stdout_streamer)
            stream.filter(languages=LANGUAGES, track=tags, async=True, )
        except Exception, e:
            print e.message
            stream.disconnect()


if __name__ == '__main__':
   # sys.exit(main())
    #while True:
    try:
        stdout_streamer = TsvStreamer()
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, stdout_streamer)
        stream.filter(languages=LANGUAGES, track=tags, async=True, )
    except Exception, e:
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        print e.message
        stream.disconnect()
