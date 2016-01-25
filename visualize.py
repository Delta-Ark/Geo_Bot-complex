## NLTK stuff
import nltk, re
from nltk.tokenize import word_tokenize
#from nltk.probability import FreqDist
from nltk.corpus import stopwords

def visualize(search_results):
    tweet_text = u''
    for sr in search_results:
        tweet_text = tweet_text + sr.text

    tokens=word_tokenize(tweet_text)
    #remove stop words and do some basic filtering
    tokens = [word.lower() for word in tokens]
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    #remove urls with another filter using reg expressions
    p = re.compile(r'//t.co/')
    filtered_words = [word for word in filtered_words if not p.match(word)]
    p2 = re.compile(r'https')
    filtered_words = [word for word in filtered_words if not p2.match(word)]
    filtered_words = [word for word in filtered_words if len(word)>2]
    fdist = nltk.probability.FreqDist(filtered_words)
    textOb = nltk.text.Text(filtered_words)
    print textOb.collocations()
    fdist.plot(30)

    # print "vocab is: "
    # print textOb.vocab()
