#!/usr/bin/python
# real_time_vis.py
# Saito 2015
"""
Must wait 5 seconds between queries (5.5 to be safe)
"""

import threading, time, argparse, copy
import visualize, geotweets, geosearchclass


      
product = []
#lock = threading.Lock()
condition = threading.Condition()


def new_tweets(new_sr, old_sr):
    only_new_list = []
    new_set = set(new_sr)
    old_set = set(old_sr)
    new_set.difference_update(old_set)
    if new_set:
        only_new_list = list(new_set)
    return only_new_list


def new_tweets_by_id(new_sr,old_ids):
    ''' old_ids is a set of ids'''
    new_tweets=[]
    print type(old_ids)
    print len(old_ids)
    print type(new_sr)
    if old_ids:
        print 'processing out old tweet'
        new_tweets = [sr for sr in new_sr if sr.id not in old_ids]
    else:
        new_tweets = new_sr
    return new_tweets

    

class Producer( threading.Thread ):
    def __init__(self,geosearcher):
        threading.Thread.__init__(self)
        self.geosearcher = geosearcher
        
    def run ( self ):
        old_ids = set()
        while True:
            search_results = self.geosearcher.api_search()
            print "\n\n\n len(search_results) = " + str(len(search_results))
            print "\len(old_ids) = " + str(len(old_ids))
            new_search_results = new_tweets_by_id(search_results,old_ids)
            #new_search_results = new_tweets(search_results,old_search_results)
            print "len(new_search_results) = " + str(len(new_search_results)) + "\n\n\n"
            filtered_words = visualize.process(new_search_results)
            if filtered_words:
                with condition:
                    print 'Thread', self.getName(), 'got lock'
                    product.extend( filtered_words)
                    #product.append(  filtered_words)
                    condition.notifyAll()
                    print 'Thread', self.getName(), 'notified others'
            old_ids = set([s.id for s in search_results])
            time.sleep(5) #wait >=5s to get more tweets

            

class Consumer( threading.Thread ):
    def run ( self ):
        n_words = 0
        while True:
            with condition:
                print 'Thread', self.getName(), 'got lock'
                print ' len(product) = ' + str(len(product))
                condition.wait()
                visualize.visualize(product)



def _verbose_new_tweets(new_sr, old_sr):
    only_new_list = []
    min_l = min(len(new_sr),len(old_sr))
    new_ids = set()
    old_ids = set()
    for i in xrange(min_l):
        new_ids.add(new_sr[i].id)
        old_ids.add(old_sr[i].id)
        print "new id " + str(new_sr[i].id )
        print "old id " + str(old_sr[i].id )
        print 'different? ' + str(new_sr[i].id != old_sr[i].id)
    print 'printing new ids before and after diff update'
    print "length of new ids before " + str(len(new_ids))
    new_ids.difference_update(old_ids)
    print "length of new ids after " + str(len(new_ids))
    
    new_set = set(new_sr)
    old_set = set(old_sr)
    print 'new set len ' + str(len(new_set))
    print 'old set len ' + str(len(old_set))
    #only_new_set = new_set.difference_update(old_set)
    print 'equivalent sets? ' + str(new_set == old_set)
    new_set.difference_update(old_set)
    print 'only new set len ' + str(len(new_set))
    if new_set:
        print 'changing to list'
        only_new_list = list(new_set)
    return only_new_list


def _test_new_tweet_filter(i):
    fn = 'params.txt'
    fn2 = 'params2.txt'
    print 'Using parameters from ' + fn
    g = geosearchclass.GeoSearchClass()
    g.set_params_from_file(fn)
    sr = g.api_search()
    if i==1:
        print "This test creates a new search from NYC - all different"
        g.set_params_from_file(fn2) # NYC
        sr2 = g.api_search()    # all different (15 old different ones)
#        new_tweets_only = _verbose_new_tweets(sr, sr2) 
        #new_tweets_only = new_tweets(sr, sr2)

        old = [s.id for s in sr2]
        old = set(old)
        print old
        new_tweets_only = new_tweets_by_id(sr,old)
        
        print "\n\n\nshould keep all 100 new tweets\n\n\n"
    if i==2:
        print "This test keeps 10 of the same tweets as old ones"
        sr2 = sr[0:10] # 10 old same one
        #new_tweets_only = _verbose_new_tweets(sr, sr2)
        #new_tweets_only = new_tweets(sr, sr2)
        old = [s.id for s in sr2]
        old = set(old)
        print old
        new_tweets_only = new_tweets_by_id(sr, old)
        print "\n\n\nshould see only 90 new tweets\n\n\n"
    if i==3:
        print "This test has same 100 tweets twice"
        sr2 = sr #all the same
        #new_tweets_only = _verbose_new_tweets(sr, sr2)
        #new_tweets_only = new_tweets(sr, sr2)
        old = [s.id for s in sr2]
        print old
        old = set(old)
        new_tweets_only = new_tweets_by_id(sr,old)
        print "\n\n\nshould see 0 new tweets\n\n\n"
    
    print "len(sr) = " + str(len(sr))
    print "len(sr2) = " + str(len(sr2))
    print "len(new_tweets_only) = " + str(len(new_tweets_only))
    print "\n\n\n"

        



def main():
    # _test_new_tweet_filter(1)
    # _test_new_tweet_filter(2)
    # _test_new_tweet_filter(3)
    
    
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


    

        







    

# Standard boilerplate to call the main() function to begin
# the program.         
if __name__ == '__main__':
    main()
