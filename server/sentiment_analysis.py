import sys
import pickle

import pandas as pd
import numpy as np
import scipy
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn import preprocessing
import spacy


LABEL_ENCODER_DATA = 'label_encoder.pickle'
TFIDF_VECTORIZER_DATA = 'tfidf_vectorizer.pickle'
SVD_DATA = 'svd.pickle'
MODEL_DATA = 'model.pickle'
POSITIVE_WORDS = 'positive-words.txt'
NEGATIVE_WORDS = 'negative-words.txt'


def load(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def read_dictionary(filepath):
    with open(filepath) as f:
        return set(f.read().strip().split('\n'))


le = load(LABEL_ENCODER_DATA)
tiv = load(TFIDF_VECTORIZER_DATA)
svd = load(SVD_DATA)
model = load(MODEL_DATA)

pos_words = read_dictionary(POSITIVE_WORDS)
neg_words = read_dictionary(NEGATIVE_WORDS)

nlp = spacy.load('en')


def get_sentiments(text):
    normalized = nlp(text)....
    words = normalized.split()
    additional_features = [
        text.count('!'),
        text.count('?'),
        sum(1 for word in words if word in pos_words),
        sum(1 for word in words if word in neg_words)
    ]

    X = tiv.transform([normalized])
    X = svd.transform(X)

    X = np.concatenate((X, [additional_features]), axis=1)

    print(X)
    print(X.shape)

    probas = model.predict_proba([X])[0]
    predictions = []
    for i, proba in enumerate(probas):
        sentiment = le.inverse_transform([i])[0]
        predictions.append((proba, sentiment))
    predictions.sort(reverse=True)
    return [sentiment for proba, sentiment in predictions]


if __name__ == '__main__':
    get_sentiments('Hi Hello hiya')
