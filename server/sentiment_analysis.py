import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
import pickle
from nltk import WordNetLemmatizer
import numpy as np
import pandas as pd


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


tiv = load(TFIDF_VECTORIZER_DATA)
svd = load(SVD_DATA)

pos_words = read_dictionary(POSITIVE_WORDS)
neg_words = read_dictionary(NEGATIVE_WORDS)


l = [
    'fun',
    'happiness',
    'hate',
    'love',
    'neutral',
    'relief',
    'sadness',
    'surprise',
    'worry'
]


model2 = []
for i, name in enumerate(l):
    with open(name + 'class_last.pickle', 'rb') as fid:
        model = pickle.load(fid)
        model2.append(model)


def normalize(text):
    tokens = [word_tokenize(text)][0]
    lower_tokens = [w.lower() for w in tokens]
    non_stop_words = [token for token in lower_tokens if token not in nltk.corpus.stopwords.words('english')]
    non_stop_words_and_punctuation = [word for word in non_stop_words if word not in list(punctuation)]
    lemmatizer = WordNetLemmatizer()
    normalized_sents = []
    normalized_sents.append([lemmatizer.lemmatize(word) for word in non_stop_words_and_punctuation])
    s = ''
    for i in normalized_sents[0]:
        s += i
        s += ' '
    return normalized_sents


def predict(svd_data, models, l):
    return [l[i] for i, model in enumerate(models) if model.predict(svd_data.reshape(1, -1)) == 1]


def get_sentiments(text):
    # return ['fun', 'anger']

    text_normalized = normalize(text)
    text_normalized_tiv = tiv.transform([text])
    svd_data = svd.transform(text_normalized_tiv)

    svd_data = np.column_stack((svd_data, pd.Series([text.count('!')])))
    svd_data = np.column_stack((svd_data, pd.Series([text.count('?')])))
    svd_data = np.column_stack((svd_data, pd.Series([sum(el in pos_words for el in text_normalized[0])])))
    svd_data = np.column_stack((svd_data, pd.Series([sum(el in neg_words for el in text_normalized[0])])))

    return predict(svd_data, model2, l)
