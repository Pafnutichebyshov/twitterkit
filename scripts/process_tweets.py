import argparse

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
    window = 10
    negative = 10
    bigram = models.Phrases(sentences)
    sentences = [s for s in bigram[sentences]]
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


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args(args)
    df = pd.read_csv(args.input_file, sep='\t', encoding='utf-8')
    df = df[pd.notnull(df['text'])]
    tokenizer = CountVectorizer().build_tokenizer()
    preprocessor = CountVectorizer().build_preprocessor()
    df['clean_tweet'] = df['text'].apply(lambda x: preprocess(x, tokenizer, preprocessor))
    model = train_model(df['clean_tweet'].tolist())
    return df, model


if __name__ == '__main__':
    df, model = main()
