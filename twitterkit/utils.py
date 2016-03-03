import os

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


def extract_text(tweet):
    """Extracts text data from a tweet object"""
    source = extract_value(tweet, 'source')
    if source != 'null':
        # remove html tags
        source = source.split('>')[1].split('<')[0]
    return {
        'id_str': extract_value(tweet, 'id_str'),
        'user_id': extract_value(tweet, 'user.id_str'),
        'created_at': extract_value(tweet, 'created_at'),
        'source': source,
        'text': extract_value(tweet, 'text'),
        'coordinates': extract_value(tweet, 'coordinates.coordinates'),
        'full_name': extract_value(tweet, 'place.full_name'),
        'country_code': extract_value(tweet, 'place.country_code'),
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


def process_tweets(input_file, output_prefix, table_funcs):
    with open(input_file, 'r') as input_obj:
        tweets = load_json(input_obj)
        for num, tweet in enumerate(tweets):
            print(num)
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
