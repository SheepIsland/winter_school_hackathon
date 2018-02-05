import markovify


with open('markov_chain.json') as f:
    model_json = f.read()
model = markovify.Text.from_json(model_json)


def _make_short_sentence(max_chars, start):
    sentence = model.make_sentence_with_start(start)
    while not sentence or len(sentence) > max_chars:
        sentence = model.make_sentence_with_start(start)
    return sentence


def generate_sentence(sentiment):
    return _make_short_sentence(60, sentiment)[len(sentiment) + 1:]


def main():
    for sentiment in SENTIMENTS:
        print(sentiment, generate_sentence(sentiment))


if __name__ == '__main__':
    main()
