import argparse

from twitterkit import utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('input_file', help='input file.', type=str)
    parser.add_argument('output', help='output prefix.', type=str)
    args = parser.parse_args()
    table_funcs = {
        'user': utils.extract_user,
        'tweet':  utils.extract_text,
        'hashtag': utils.extract_entities,
    }
    utils.process_tweets_to_csv(args.input_file, args.output, table_funcs)
