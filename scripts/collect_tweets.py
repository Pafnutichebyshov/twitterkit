import argparse

#from http.client import IncompleteRead
import logging
import os
import sys
import time
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import ProtocolError

from tweepy import OAuthHandler
from tweepy import Stream

from twitterkit import support
from twitterkit import tweet_access
from twitterkit import utils


logger = logging.getLogger()

ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
LANGUAGES = ['en']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file', help='Prefix for output file.')
    args = parser.parse_args()

    logger = support.getLogger('tsv_writer')

    funcs = {
        'user': utils.extract_user,
        'tweet':  utils.extract_text,
        'hashtag': utils.extract_entities,
    }

    while True:
        try:
            data_streamer = tweet_access.TsvStreamer(
                output=args.output_file, func=funcs, monitor=True)
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
            stream = Stream(auth, data_streamer)
            stream.sample(languages=LANGUAGES)
        except KeyboardInterrupt, e:
            stream.disconnect()
            break
        except (IndexError, ConnectionError, ProtocolError), e:
            logger.exception(e)
            stream.disconnect()
            time.sleep(60)
            continue


if __name__ == '__main__':
    sys.exit(main())
