import logging
import os
import sys
import time
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import ProtocolError, ReadTimeoutError

from tweepy import OAuthHandler
from tweepy import Stream

from twitterkit import tweet
from twitterkit import utils


logger = utils.get_logger('collect_tweets.py')

ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
LANGUAGES = ['en']
TABLENAME = 'tweet'


def main():
    while True:
        try:
            with utils.connect('ng') as conn:
                with conn.cursor() as cur:
                    cur.execute("""CREATE TABLE IF NOT EXISTS {tablename}(
                        id_str text PRIMARY KEY,
                        source text,
                        user_id text,
                        created_at timestamp,
                        text text)""".format(tablename=TABLENAME))
                data_streamer = tweet.PostgresStreamer(conn=conn, tablename=TABLENAME)
                auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
                auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
                stream = Stream(auth, data_streamer)
                stream.sample(languages=LANGUAGES)
                conn.commit()
        except KeyboardInterrupt:
            stream.disconnect()
            break
        except (IndexError, ConnectionError, ProtocolError, ReadTimeoutError):
            #logger.exception(e)
            stream.disconnect()
            time.sleep(90)
            continue


if __name__ == '__main__':
    sys.exit(main())
