#!/usr/bin/env python

"""
Functions for parsing the raw text (from sec filings, etc.) into English-language sentences
using nltk (installation and usage: http://nltk.org/)

"""

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

ABBREVIATIONS = [
    # edit as needed with things
    # likely to be found in filing text
    'dr', 'vs', 'mr', 'mrs', 'prof',
    'inc', 'llc', 'ltd'
]

def preprocess (text):
    """When the last word of the sentence has an apostrophe or
    a quotation mark attached to it, nltk gets fooled, so pad
    cases like that with spaces"""

    return text.replace('?"', '? "').replace('!"', '! "').replace('."', '. "')

def parse (text):
    """Use nltk's PunktSentenceTokenizer to convert the text string into
    a list of English-language sentences."""

    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(ABBREVIATIONS)
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    return sentence_splitter.tokenize(preprocess(text))
