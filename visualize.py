## NLTK stuff
import nltk, re
#from nltk.tokenize import word_tokenize
#from nltk.probability import FreqDist
from nltk.corpus import stopwords

def do_it_all(search_results):
    visualize(process(search_results))

def visualize(word_list):
    fdist = nltk.probability.FreqDist(word_list)
    textOb = nltk.text.Text(word_list)
    print textOb.collocations()
    #fdist.plot(30)    
    # print "vocab is: "
    # print textOb.vocab()


def process(search_results):
    tokens = tokenize_results(search_results)
    filtered_words = filter(tokens)
    return filtered_words

    
def tokenize_results(search_results):
    tweet_text = u''
    for sr in search_results:
        tweet_text = tweet_text + sr.text

    tokens=nltk.tokenize.word_tokenize(tweet_text)
    return tokens
    
    
def filter(word_list):
    #remove stop words and do some basic filtering
    tokens = [word.lower() for word in word_list]
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    #remove urls with another filter using reg expressions
    p = re.compile(r'//t.co/')
    filtered_words = [word for word in filtered_words if not p.match(word)]
    p2 = re.compile(r'https')
    filtered_words = [word for word in filtered_words if not p2.match(word)]
    filtered_words = [word for word in filtered_words if len(word)>2]
    return filtered_words
