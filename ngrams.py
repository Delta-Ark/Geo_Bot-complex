#!/usr/bin/python
# ngrams.py
# Saito 2017

import random

import utils


def make_ngram(text, n):
    ngram = dict()
    tokens = utils.tokenize_normal_words(text)
    i = 0
    while i < (len(tokens)-(n-1)):
        l = list()
        for j in range(n-1):
            token = tokens[i+j]
            token = token.lower()
            # print token
            l.append(token)
        key = tuple(l)
        # print key
        value = tokens[i+n-1]
        value = value.lower()
        if key in ngram:
            ngram[key].append(value)
        else:
            ngram[key] = list()
            ngram[key].append(value)
        i += 1
    return ngram


def generate(ngram, seed):
    """given an ngram dictionary and a string or tuple of words, this \
returns a word. For efficiency, pass in all words as a list"""
    if type(seed) is not tuple:
        l = list()
        tokens = utils.tokenize_normal_words(seed)
        tokens = [t.lower() for t in tokens]
        l.extend(tokens)
        seed = tuple(l)

    word = ""
    if seed in ngram:
        word = random.choice(ngram[seed])
        # print "found in dictionary"
        # print ngram[seed]

    # elif words is None:
    #     print "Combining all dictionary values."
    #     words = sum(ngram.values(), [])
    #     word = random.choice(words)
    # else:
    #     word = random.choice(words)
    return word


def make_bigram_trigram_dictionary(text):
    bigram = make_ngram(text, 2)
    # print bigram
    trigram = make_ngram(text, 3)
    # print trigram
    bigram.update(trigram)
    # print "printing bigram"
    # print bigram
    return bigram


def main():
    initial_text = u"""
This is my poem.
It is not very clever,
But I'm fond of it.
"""

    print initial_text
    ngram = make_bigram_trigram_dictionary(initial_text)
    word = generate(ngram, 'this')
    print "response should be 'is'"
    print word
    

if __name__ == '__main__':
    main()
