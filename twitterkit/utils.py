import logging
import os
import time

import psycopg2
import ujson as json
import unicodecsv as csv



def load_json(filelike):
    for line in filelike:
        yield json.loads(line)


def write_json(data, filelike):
    json.dump(data, filelike)
    filelike.write('\n')


def extract_value(data, key_str, null='null'):
    """Extract arbitrary values from a dictionary"""
    keys = key_str.split('.')
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError):
            return null
    return data


def extract_user(tweet):
    """Extracts user object data"""
    return {
        'user_id': extract_value(tweet, 'user.id_str'),
        'created_at': extract_value(tweet, 'user.created_at'),
        'screen_name': extract_value(tweet, 'user.screen_name'),
    }


def extract_text(tweet, null='null'):
    """Extracts text data from a tweet object"""
    source = extract_value(tweet, 'source') or null
    if source != null:
        # remove html tags
        source = source.split('>')[1].split('<')[0]
    return {
        'id_str': extract_value(tweet, 'id_str'),
        'user_id': extract_value(tweet, 'user.id_str'),
        'created_at': extract_value(tweet, 'created_at'),
        'source': source,
        'text': sanitize_string(extract_value(tweet, 'text')),
    }


def extract_entity(tweet, key_str, entity_key, null='null'):
    # Ugly hack for now
    entities = extract_value(tweet, key_str, null=null)
    if entities == null:
        return entities
    return '/'.join([entity[entity_key] for entity in entities])


def extract_entities(tweet):
    """Extracts text data from a tweet object"""
    entities = extract_entity(tweet, 'entities.hashtags', 'text')
    if entities is None:
        return None
    return {
        'id_str': extract_value(tweet, 'id_str'),
        'user_id': extract_value(tweet, 'user.id_str'),
        'created_at': extract_value(tweet, 'created_at'),
        'hashtags': entities
    }


def process_tweets_to_csv(input_file, output_prefix, table_funcs):
    for table, func in table_funcs.items():
        start_time = time.time()
        output_file = '{}_{}.tsv'.format(output_prefix, table)
        with open(output_file, 'a') as f:
            fieldnames = func({})
            csv_writer = csv.DictWriter(f, fieldnames, delimiter='\t')
            if not os.path.getsize(output_file):
                csv_writer.writeheader()
            with open(input_file, 'r') as input_obj:
                tweets = load_json(input_obj)
                for num, tweet in enumerate(tweets):
                    if not num % 1000:
                        elapsed_time = time.time() - start_time
                        rate_per_second = num / elapsed_time
                        print('{} per second'.format(rate_per_second))
                    parsed_tweet = func(tweet)
                    if parsed_tweet:
                        csv_writer.writerow(parsed_tweet)


def process_tweet_obj(tweet, output_prefix, table_funcs):
    for table, func in table_funcs.items():
        output_file = '{}_{}.tsv'.format(output_prefix, table)
        with open(output_file, 'a') as f:
            fieldnames = func({})
            csv_writer = csv.DictWriter(f, fieldnames, delimiter='\t')
            if not os.path.getsize(output_file):
                csv_writer.writeheader()
            parsed_tweet = func(tweet)
            if parsed_tweet:
                csv_writer.writerow(parsed_tweet)


def process_tweet(tweet, func_file):
    for table, func_writer in func_file.items():
        func, csv_writer = func_writer
        parsed_tweet = func(tweet)
        if parsed_tweet:
            csv_writer.writerow(parsed_tweet)


def get_logger(name, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    fh = logging.FileHandler('{}.log'.format(name))
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def sanitize_string(input_string):
    """Remove non-printing characters from a string."""
    return ''.join(c if ord(c) >= 32 else u'?' for c in input_string)


def connect(user, password='', host='localhost', port='5432', db='twitter'):
    """Establish a connection to a postgresql database."""
    return psycopg2.connect(database=db, user=user, password=password, host=host, port=port)


def insert_query(conn, query, args):
    """Returns a list of rows (as dictionaries) that are the result of the query """
    with conn.cursor() as cursor:
        cursor.execute(query, args)
