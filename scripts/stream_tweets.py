import os
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']


class StreamAccess(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


def main():
    stream_access = StreamAccess()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, stream_access)
    stream.filter(track=['python'])


if __name__ == '__main__':
    sys.exit(main())
