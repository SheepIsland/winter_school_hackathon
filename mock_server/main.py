import flask
from flask import request
import json

app = flask.Flask(__name__)


EMOJI_MAP = {
    'fun': '😁'
}


def get_sentiments(text):
    return ['fun']


@app.route('/get_emojis', methods=['POST'])
def get_emojis():
    text = request.data
    print(text)
    emojis = []
    for sentiment in get_sentiments(text):
        emoji = EMOJI_MAP.get(sentiment)
        if emoji is not None:
            emojis.append(emoji)

    return json.dumps(emojis, ensure_ascii=False)


app.run(
    host='0.0.0.0',
    port=8089,
    debug=True)
