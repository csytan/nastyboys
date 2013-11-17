import cPickle as pickle
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
    stop_free_tokens = filter(lambda x: x not in stopwords.words('english'),
            stem_tokens)
    # return a list of tokens and bigrams
    return stop_free_tokens

def classifierizaton(tokenized_data, tag):
    '''we are going to massage the data we go from tokenize_data into the form
    that nltk naivebayseclassifier wants. the data should be something like
    ({'contains(word)': True, 'contrains(word2)': True}, 'positive') 
    '''
    classify_dict = {key : True for key in tokenized_data}
    return (classify_dict, tag)

def write_training_data(pickle_file):
    counter = 0
    pos_dir = os.path.join(TRAINING_DIRECTORY, 'pos')
    neg_dir = os.path.join(TRAINING_DIRECTORY, 'neg')
    pos_list = load_data(pos_dir)
    neg_list = load_data(neg_dir)
    training_set = []
    for item in pos_list:
        tokenized = tokenize_data(item)
        training_set.append(classifierizaton(tokenized, 'pos'))
        counter += 1
        print counter
    for item in neg_list:
        tokenized = tokenize_data(item)
        training_set.append(classifierizaton(tokenized, 'neg'))
        counter += 1
        print counter
    with  open(pickle_file, 'w') as f:
        pickle.dump(training_set, f)

def train_data(pickle_file):
    '''in this function, we first load the pick file in to the list of tuples
    we wanted for nltk classifier then we run the training set'''
    with open(pickle_file, 'r') as f:
        training_set = pickle.load(f)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    #write_training_data('training_data.p')
    train_data('training_data.p')



