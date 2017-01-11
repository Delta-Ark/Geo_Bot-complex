# NLTK stuff

"""This is a utils file for the other programs.

It contains Natural language processing tools from NLTK, some basic
visualizer, a tweet status object info extractor and a new tweet
identifier.

"""


import re
import nltk
import tweepy
from nltk.corpus import stopwords



def get_credentials(keys_file="consumerkeyandsecret", app_only=True):
    '''This function gives credentials  to the API.

    When app_only is true, application only authorization level
    credentials are supplied. This is sufficient for searching tweet
    history. It must be False for streaming access and to post tweets.

    It requires that your consumerkeyandsecret have 4 lines, with the
    consumer key on the first line, the secret on the next and then an
    access token on the 3rd and the access token secret on the
    4th. You can get these by logging on to your twitter account and
    creating an app.

    USAGE: (api, auth) = get_creds(keys_file, [app_only=[True/False]])
        The second argument is optional

    '''
    with open(keys_file, 'rU') as myfile:
        auth_data = [line.strip() for line in myfile]
        CONSUMER_KEY = auth_data[0]
        CONSUMER_SECRET = auth_data[1]
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        if not app_only:
            ACCESS_TOKEN = auth_data[2]
            ACCESS_TOKEN_SECRET = auth_data[3]
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    return (api, auth)
            

def get_simplified_tweet(status):
    """ Takes in a tweet status object and parses it"""
    user = status.user.screen_name
    print user
    d = status.created_at
    isotime = d.isoformat()
    print isotime
    id_string = status.id_str
    print id_string
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
    simplified_tweet = [user, isotime, id_string, text, loc_name, loc]
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
    # import matplotlib
    # matplotlib.use('qt4agg')  # workaround for virtual environments
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
    plt.yticks(range(
        1, 1 + len(samples)), [s for s in samples], rotation=0)
    plt.ylabel("Samples")
    plt.xlabel("Counts")
    plt.show()
    return fdist
