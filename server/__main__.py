import flask
from flask import request
import json

from server.sentiment_analysis import get_sentiments
from server.markov_chain_prediction import generate_sentence


app = flask.Flask(__name__)


EMOJI_MAP = {
    'happiness': '😊',
    'hate': '😡',
    'love': '️❤️',
    'neutral': '😐',
    'relief': '😌',
    'sadness': '😔',
    'surprise': '😮',
    'worry': '😧',
    'enthusiasm': '👍',
    'fun': '😁',
    'anger': '😡'
}

INVERSE_EMOJI_MAP = {
    emoji.encode('utf-8'): sentiment
    for sentiment, emoji in EMOJI_MAP.items()
}


def get_emojis(text):
    emojis = []
    for sentiment in get_sentiments(text):
        emoji = EMOJI_MAP.get(sentiment)
        if emoji is not None:
            emojis.append(emoji)
        else:
            print('Sentiment {} does not have an emoji'.format(sentiment))

    return json.dumps(emojis, ensure_ascii=False)


def get_sentences(emoji):
    sentiment = INVERSE_EMOJI_MAP.get(emoji)
    if sentiment is None:
        return '[]'
    return json.dumps([generate_sentence(sentiment) for _ in range(5)])


@app.route('/get_predictions', methods=['POST'])
def get_predictions():
    data = request.data.strip()
    print(data, data in INVERSE_EMOJI_MAP)
    if data in INVERSE_EMOJI_MAP:
        return get_sentences(data)
    else:
        return get_emojis(data)


app.run(
    host='0.0.0.0',
    port=8089,
    debug=True)
