import re

import pandas as pd
import markovify


word_split_pattern = re.compile(r"\s+")
STOP_SYMBOLS = set('\\"\'[]()')


def parse_sentence(sentence):
    sentence = ''.join(sym for sym in sentence if sym not in STOP_SYMBOLS)
    words = re.split(word_split_pattern, sentence)
    words = [w for w in words if not w.startswith('@')]
    return words


def main():
    corpus = pd.read_csv('text_emotion_norm.csv')
    sentences = []
    for i, row in corpus.iterrows():
        sentences.append(row['sentiment'] + ' ' + row['content'])
    parsed_sentences = list(map(parse_sentence, sentences))
    print('\n'.join(map(str, parsed_sentences[:20])))
    print(set(s[0] for s in parsed_sentences))

    model = markovify.Text(input_text=None, parsed_sentences=parsed_sentences)
    model_json = model.to_json()
    with open('markov_chain.json', 'w') as f:
        f.write(model_json)


if __name__ == '__main__':
    main()
