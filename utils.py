# NLTK stuff
import re

import nltk
from matplotlib import pylab
from nltk.corpus import stopwords


def new_tweets(new_sr, old_ids):
    '''returns only search_results that do not have ids listed in old_ids
    new_sr is the new search results, old_ids is a set of ids

    '''
    new_tweets = []
    if old_ids:
        new_tweets = [sr for sr in new_sr if sr.id not in old_ids]
    else:
        new_tweets = new_sr
    return new_tweets


def do_it_all(search_results):
    visualize(process(search_results))


def visualize(word_list):
    fdist = get_freq_dist(word_list)
    textOb = nltk.text.Text(word_list)
    print textOb.collocations()
    # print textOb.vocab()

    # fdist.plot(30)

    return fdist


def get_freq_dist(word_list):
    fdist = nltk.probability.FreqDist(word_list)
    return fdist


def visualize_old(word_list):
    fdist = get_freq_dist(word_list)
    textOb = nltk.text.Text(word_list)
    print textOb.collocations()
    # fdist.plot(30)

    samples = [item for item, _ in fdist.most_common(30)]
    freqs = [fdist[sample] for sample in samples]
    pylab.grid(True, color="silver")
    pylab.plot(freqs)
    pylab.xticks(range(len(samples)), [str(s) for s in samples], rotation=90)
    pylab.xlabel("Samples")
    pylab.ylabel("Counts")
    pylab.show()
    return fdist


def process(search_results):
    tokens = tokenize_results(search_results)
    filtered_words = filter(tokens)
    return filtered_words


def tokenize_results(search_results):
    tweet_text = u''
    for sr in search_results:
        tweet_text = tweet_text + sr.text
    tokenizer = nltk.tokenize.casual.TweetTokenizer()
    tokens = tokenizer.tokenize(tweet_text)
#    tokens = nltk.tokenize.word_tokenize(tweet_text)
    return tokens


def filter(word_list):
    # remove stop words and do some basic filtering
    tokens = [word.lower() for word in word_list]
    filtered_words = [
        word for word in tokens if word not in stopwords.words('english')]
    # remove urls with another filter using reg expressions
    p = re.compile(r'//t.co/')
    filtered_words = [word for word in filtered_words if not p.match(word)]
    p2 = re.compile(r'https')
    filtered_words = [word for word in filtered_words if not p2.match(word)]
    filtered_words = [word for word in filtered_words if len(word) > 2]
    return filtered_words
