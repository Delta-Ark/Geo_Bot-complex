#!/usr/bin/python
# geotweets
# Saito 2015

"""
This program is for grabbing geo-located tweets using the Twitter API


USAGE:
  >> ./geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]

Print command line help:
>> ./geotweets.py --help   (or just -h)

Example:
This uses parameter file 'params.txt', prints results to command line and writes them to 'out.txt':
>> ./geotweets.py --verbose --filename params.txt --output out.txt

The program requires a consumer key and secret stored in a file called
consumerkeyandsecret. See README for details.

The program can optionally take a parameter file as input. This file,
must be in python dictionary format and contain these paramters:
latitude, longitude, radius, search_term, result_type and
count. Please see the file "params.txt" for an example.

Example of params.txt:
{"latitude" : 37.7821, 
"longitude": -122.4093,
"radius" : 10,
"search_term" : "#SF+tech",
"result_type" : "mixed",
"count" : 15}

"""


import sys, tweepy, ast, argparse
from geosearchclass import GeoSearchClass

def get_creds():
    '''USAGE: api = get_creds() This function gives App Only
    Authorization.  It is made for app access to the twitter rest API.
    '''
    with open ("consumerkeyandsecret", 'rU') as myfile:
        auth_data = [line.strip() for line in myfile]
        CONSUMER_KEY=auth_data[0]
        CONSUMER_SECRET = auth_data[1]
    auth = tweepy.auth.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth)            
    return api

    

def get_params(filename):
    with open(filename, 'rU') as f:
        params = dict()
        params.update(ast.literal_eval(f.read()))        
    for key in params.keys():
        print key + ' : ' + str(params[key])        
    return params

## NLTK stuff
import nltk, re
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
def visualize(search_results):
    tweet_text = u''
    for sr in search_results:
        tweet_text = tweet_text + sr.text

    tokens=word_tokenize(tweet_text)
    #remove stop words and do some basic filtering
    tokens = [word.lower() for word in tokens]
    print '\n\n\n\n stop words: \n'
    print   stopwords.words('english')
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    #remove urls with another filter using reg expressions
    p = re.compile(r'//t.co/')
    filtered_words = [word for word in filtered_words if not p.match(word)]
    p2 = re.compile(r'https')
    filtered_words = [word for word in filtered_words if not p2.match(word)]
    filtered_words = [word for word in filtered_words if len(word)>2]
    print '\n\n\n'
    print filtered_words
    fdist = FreqDist(filtered_words)
    fdist.plot(30)





def main():
    # Create command line argument parser
    parser = argparse.ArgumentParser(description='Perform a geo-located search.')
    #need to add arguments here
    #parser.add_argument('filename', metavar='filename', type=str, help='The parameter file name')
    parser.add_argument('-d', '--doc', action='store_true', help='print module documentation and exit')
    parser.add_argument('-f', '--filename', help='specify a FILENAME to use as the parameter file. If not specified, will use default arguments.')
    parser.add_argument('-v', '--verbose', action='store_true', help='additionally print output to command line')
    parser.add_argument('-o', '--output', help='specify an OUTPUT file to write to. The default is output.txt')
    parser.add_argument('-vis', '--visualize', action='store_true', help='visualize using nlp tools')
    
    #automatically grabs arguments from sys.argv[]
    args = parser.parse_args()

    if args.doc:
        print __doc__
        sys.exit()

    g = GeoSearchClass()
    
    if args.filename:
        print 'Using parameters from ' + str(args.filename)
        params_FN = args.filename
        #turn parameter file into dictionary
        params = get_params(params_FN)
        #extract params:
        g.latitude =    params['latitude']
        g.longitude =   params['longitude']
        g.radius =      params['radius']
        g.search_term = params['search_term']
        g.result_type = params['result_type']
        g.count =       params['count']
    else:
        print "Using default search values"

    api = get_creds()
    g.api_search(api) #perform geolocation based search
    # print formatted results with extra info to terminal
    if args.verbose:
        g.print_search_results()
        
    if args.output:
        g.write_search_results(args.output)
    else:
        g.write_search_results()

    if args.visualize:
        visualize(g.search_results)



# Standard boilerplate to call the main() function to begin
# the program.         
if __name__ == '__main__':
    main()

