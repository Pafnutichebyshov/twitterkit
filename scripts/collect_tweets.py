import logging
import os
import sys
import time
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import ProtocolError

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
    # while True:
        # try:
    with utils.connect('ng') as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS {tablename}(
                id_str  varchar(255) PRIMARY KEY,
                source varchar(128),
                user_id varchar(255),
                created_at timestamp,
                text varchar(255))""".format(tablename=TABLENAME))
        data_streamer = tweet.PostgresStreamer(conn=conn, tablename=TABLENAME)
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, data_streamer)
        stream.sample(languages=LANGUAGES)
        conn.commit()
        # except KeyboardInterrupt, e:
            # stream.disconnect()
            # break
        # except (IndexError, ConnectionError, ProtocolError), e:
            # logger.exception(e)
            # stream.disconnect()
            # time.sleep(90)
            # continue


if __name__ == '__main__':
    sys.exit(main())
