import logging
import os
import sys
import time

from tweepy import OAuthHandler
from tweepy import Stream

from twitterkit import support
from twitterkit import tweet_access


logger = logging.getLogger()

ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
FILENAME = '/Users/ng/data/2016-03-02.json'
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
    'makeamericagreatagain',
    'donald2016',
    'trump2016',
    'donaldtrump2016',
    'ted',
    'cruz',
    'tedcruz',
    'ted2016',
    'cruz2016',
    'tedcruz2016',
    'reignitingthepromiseofamerica',
    'marco',
    'rubio',
    'marcorubio',
    'marco2016',
    'rubio2016',
    'marcorubio2016',
    'anewamericancentury',
    'bernie',
    'sanders',
    'berniesanders',
    'feelthebern',
    'bernie2016',
    'sanders2016',
    'berniesanders2016',
    'apoliticalrevolutioniscoming',
    'hillary',
    'clinton',
    'hillaryclinton',
    'hillary2016',
    'clinton2016',
    'hillaryclinton2016',
    'everydayamericansneedachampion',
    'iwanttobethatchampion',
]


def main():
    logger = support.getLogger('tsv_writer')
    while True:
        try:
            data_streamer = tweet_access.JsonStreamer(filename=FILENAME)
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
            stream = Stream(auth, data_streamer)
            stream.sample(languages=LANGUAGES)
            #stream.filter(track=TAGS, languages=LANGUAGES, async=True)
        except Exception, e:
            logger.exception(e)
            stream.disconnect()
            time.sleep(90)


if __name__ == '__main__':
    sys.exit(main())
