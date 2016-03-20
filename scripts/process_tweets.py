import argparse
import collections

from gensim import models
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

from twitterkit.preprocess import replace_user, replace_url, replace_number


def preprocess(text, tokenizer, preprocessor):
    """Lowercases, replaces urls, replaces usernames, and tokenizes"""
    return tokenizer(preprocessor(replace_number(replace_user(replace_url(text.lower())))))


def train_model(sentences):
    # Set values for various parameters
    num_features = 300
    min_word_count = 5
    num_workers = 4
    window = 5
    negative = 10
    model = models.Word2Vec(
        workers=num_workers,
        size=num_features,
        min_count=min_word_count,
        window=window,
        negative=negative
    )
    model.build_vocab(sentences)
    model.train(sentences)
    return model


def get_token_author(tweets, model, dim=(300, 1), field='tokens'):
    """Gets vectors used for discovering similar users."""
    token_user = collections.defaultdict(set)
    user_vector = {}
    for num_tweet in tweets.iterrows():
        _, tweet = num_tweet
        print(_)
        tokens = tweet[field]
        user_id = tweet['user_id']
        for token in tokens:
            token_user[token].add(user_id)
            try:
                vector = model[token].reshape(dim)
                if user_id in user_vector:
                    user_vector[user_id] += vector
                else:
                    user_vector[user_id] = vector
            except KeyError:
                continue
    return token_user, user_vector


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args(args)
    dtype = {'user_id': str, 'id_str': str}
    df = pd.read_csv(args.input_file, sep='\t', encoding='utf-8', dtype=dtype)
    df = df[pd.notnull(df['text'])]
    tokenizer = CountVectorizer().build_tokenizer()
    preprocessor = CountVectorizer().build_preprocessor()
    df['clean_tweet'] = df['text'].apply(lambda x: preprocess(x, tokenizer, preprocessor))
    model = train_model(df['clean_tweet'].tolist())
    return df, model


if __name__ == '__main__':
    df, model = main()
