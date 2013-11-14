import nltk
import sys
import os
import re
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIRECTORY = os.path.join(BASE_DIR, 'txt_sentoken')

def load_data(pos_dir):
    pos_list = [os.path.join(pos_dir, item) for item in os.listdir(pos_dir)]
    pos_txt_list = []
    for item in pos_list:
        with open(item, 'r') as f:
            pos_txt_list.append(f.read())
    return pos_txt_list

def tokenize_data(data):
    # strip off unwanted char
    data = data.replace('\n', '')
    word_reg = re.compile('[a-zA-Z0-9\']+')
    # tokenize the rest of the words
    tokens = [item.lower() for item in re.findall(word_reg, data)]
    # stem the tokenized words
    stemmer = nltk.stem.SnowballStemmer('english')
    stem_tokens = [stemmer.stem(word) for word in tokens]
    # bigram
    stem_tokens += nltk.bigrams(stem_tokens)
    # kick out stop-words
    stopwords = nltk.corpus.stopwords
    stop_free = filter(lambda x: x not in stopwords.words('english'),
            stem_tokens)
    # return a list of tokens and bigrams
    return stop_free

def parse_data(tokenized_data):
    pass

def run():
    pos_dir = os.path.join(TRAINING_DIRECTORY, 'pos')
    neg_dir = os.path.join(TRAINING_DIRECTORY, 'neg')
    pos_list = load_data(pos_dir)
    neg_list = load_data(neg_dir)
    tokenized = tokenize_data(pos_list[1])


if __name__ == '__main__':
    run()



