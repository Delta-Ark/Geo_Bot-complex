#!/usr/bin/python
# real_time_vis.py
# Saito 2015
"""This grabs tweets and visualizes them.

It creates 2 threads, 1 to produce local tweets and the other to
visualize them in a producer consumer format.

Must wait 5 seconds between queries (5.5 to be safe)

"""

import threading
import time
import argparse
import copy
import vis_helper
import geotweets
import geosearchclass


product = []
condition = threading.Condition()


def new_tweets(new_sr, old_ids):
    ''' returns only search_results that do not have ids listed in old_ids
    new_sr is the new search results, 
    old_ids is a set of ids
    '''
    new_tweets = []
    if old_ids:
        new_tweets = [sr for sr in new_sr if sr.id not in old_ids]
    else:
        new_tweets = new_sr
    return new_tweets


class Producer(threading.Thread):

    def __init__(self, geosearcher):
        threading.Thread.__init__(self)
        self.geosearcher = geosearcher

    def run(self):
        old_ids = set()
        while True:
            search_results = self.geosearcher.api_search()
            print "\n\n\n len(search_results) = " + str(len(search_results))
            print "len(old_ids) = " + str(len(old_ids))
            new_search_results = new_tweets(search_results, old_ids)
            #new_search_results = new_tweets(search_results,old_search_results)
            print "len(new_search_results) = " + str(len(new_search_results)) + "\n\n\n"
            filtered_words = vis_helper.process(new_search_results)
            if filtered_words:
                with condition:
                    print 'Thread', self.getName(), 'got lock'
                    product.extend(filtered_words)
                    #product.append(  filtered_words)
                    condition.notifyAll()
                    print 'Thread', self.getName(), 'notified others'
            old_ids = set([s.id for s in search_results])
            time.sleep(5)  # wait >=5s to get more tweets


class Consumer(threading.Thread):

    def run(self):
        n_words = 0
        while True:
            with condition:
                print 'Thread', self.getName(), 'got lock'
                print ' len(product) = ' + str(len(product))
                condition.wait()
                vis_helper.visualize(product)


def main():
    fn = 'params.txt'
    print 'Using parameters from ' + fn
    g = geosearchclass.GeoSearchClass()
    g.set_params_from_file(fn)

    producer = Producer(g)
    producer.setName('producer')
    producer.start()
    consumer = Consumer()
    consumer.setName('consumer')
    consumer.start()

if __name__ == '__main__':
    main()
