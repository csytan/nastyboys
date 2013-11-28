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

def train_data(training_set):
    '''in this function, we first load the pick file in to the list of tuples
    we wanted for nltk classifier then we run the training set'''
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier

def massage_trainging_data(label):
    
    label_dir = os.path.join(TRAINING_DIRECTORY, label)
    labeled_list = load_data(label_dir)
    labeled_data_set = []
    counter = 0
    for item in labeled_list:
        tokenized = tokenize_data(item)
        labeled_data_set.append(classifierizaton(tokenized, label))
        counter += 1
        print counter
    return labeled_data_set

def seperate_train_test_data(pos_set, neg_set):
    '''this small function combines pos & neg data, 
    and separate it into training set and testing set
    '''
    pos_cutoff = len(pos_set)*3/4
    neg_cutoff = len(neg_set)*3/4

    training_set = pos_set[:pos_cutoff] + neg_set[:neg_cutoff]
    testing_set = pos_set[pos_cutoff:] + neg_set[neg_cutoff:]
    
    return training_set,testing_set


def load_or_pickle_data(pos_label, neg_label):
    '''
    function loads training & testing data if it exists
    if not process the raw data files and pickle the train & test data
    pos_label & neg_label are the folder name of the labled files
    '''

    train_data_dir = os.path.join(BASE_DIR, "train_sample.pydata")
    test_data_dir = os.path.join(BASE_DIR, "test_sample.pydata")

    if os.path.exists(train_data_dir) and os.path.exists(test_data_dir):
        print "training & testing data exists"
        with open(train_data_dir, 'rb') as f:
            training_set = pickle.load(f)
        with open(test_data_dir, 'rb') as f:
            testing_set = pickle.load(f)
    else:
        print "training & testing data doesnt exists"
        pos_set = massage_trainging_data('pos')
        neg_set = massage_trainging_data('neg')

        training_set,testing_set = seperate_train_test_data(pos_set, neg_set)
        print "Pickling traing and testing data"
        
        with open(train_data_dir, 'wb') as f:
            pickle.dump(training_set, f, protocol=2)

        with open(test_data_dir, 'wb') as f:
            pickle.dump(testing_set, f, protocol=2)
    
    return training_set, testing_set


def getting_classifier(pos_label, neg_label):
    training_set, testing_set = load_or_pickle_data(pos_label, neg_label)
    classifier = train_data(training_set)
    
    import ipdb; ipdb.set_trace()



if __name__ == '__main__':
    #write_training_data('training_data.p')
    getting_classifier('pos', 'neg')   



