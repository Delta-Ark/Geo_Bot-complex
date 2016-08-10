# NLTK stuff
import re

import nltk
from nltk.corpus import stopwords


def get_simplified_tweet(status):
    user = status.user.screen_name
    print user
    d = status.created_at
    isotime = d.isoformat()
    print isotime
    loc_name = None
    loc = None
    if status.place:
        if status.place.full_name:
            loc_name = status.place.full_name
            print loc_name
        if status.place.bounding_box:
            loc = status.place.bounding_box.origin()
            print loc
            text = status.text
            print text
            simplified_tweet = [user, isotime, loc_name, loc, text]
    return simplified_tweet


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


def get_freq_dist(word_list):
    """Returns a frequency distribution for a list of words"""
    fdist = nltk.probability.FreqDist(word_list)
    return fdist


def tokenize_and_filter(search_results):
    """Tokenizes and then filters search results"""
    tokens = tokenize_results(search_results)
    filtered_words = filter_words(tokens)
    return filtered_words


def tokenize_results(search_results):
    """This takes in search_results i.e. status return from a twitter
    search and tokenizes the results"""
    tweet_text = u''
    for sr in search_results:
        tweet_text = tweet_text + sr.text
    tokenizer = nltk.tokenize.casual.TweetTokenizer()
    tokens = tokenizer.tokenize(tweet_text)
#    tokens = nltk.tokenize.word_tokenize(tweet_text)
    return tokens


def filter_words(word_list):
    """remove stop words and do some basic filtering"""
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


def visualize(word_list):
    """Takes in a word list and visualizes the distribution of the top 30 words.

    This works well when combined with tokenize_and_filter(search_results)."""
    
    import matplotlib.pyplot as plt

    fdist = get_freq_dist(word_list)
    textOb = nltk.text.Text(word_list)
    print "\nCollocations: "
    print textOb.collocations()
    # fdist.plot(30)
    samples = [item for item, _ in fdist.most_common(30)]
    freqs = [fdist[sample] for sample in samples]
    plt.grid(True, color="silver")
    plt.plot(freqs, range(1, 1+len(freqs)))
    plt.yticks(range(1, 1 + len(samples)), [s for s in samples], rotation=0)
    plt.ylabel("Samples")
    plt.xlabel("Counts")
    plt.show()
    return fdist
