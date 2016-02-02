#!/usr/bin/python
# fake_real_time_vis.py
# Saito 2015
"""This grabs tweets and visualizes them in fake real time.

Must wait 5 seconds between queries (5.5 to be safe)

"""


import time
import vis_helper
import geosearchclass
import real_time_vis
from  matplotlib import pylab

def update_fdist(fdist,new_words):
    for word in new_words:
        fdist[word]+=1
    return fdist


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


def main():
    fn = 'params.txt'
    print 'Using parameters from ' + fn
    g = geosearchclass.GeoSearchClass()
    g.set_params_from_file(fn)
    search_results = g.api_search()
    filtered_words = vis_helper.process(search_results)
    fdist = vis_helper.get_freq_dist(filtered_words)
    #set up plot
    samples = [item for item, _ in fdist.most_common(30)]


    freqs = [fdist[sample] for sample in samples]
    pylab.grid(True, color="silver")
    pylab.plot(freqs)
    pylab.xticks(range(len(samples)), [str(s) for s in samples], rotation=90)
    pylab.xlabel("Samples")
    pylab.ylabel("Counts")
    pylab.ion()
    pylab.show()

    time.sleep(5)
    # set up loop    
    old_ids = set([s.id for s in search_results])
    product = []
    for i in xrange(100):
        g.result_type = "recent" #use mixed above, change to recent here
        search_results = g.api_search()
        new_search_results = new_tweets(search_results, old_ids)
        if new_search_results:
            filtered_words = vis_helper.process(new_search_results)
            fdist = update_fdist(fdist,filtered_words)
            freqs = [fdist[sample] for sample in samples]
            pylab.plot(freqs)
            print '%d new tweet(s)' % len(new_search_results)
            old_ids.update(set([s.id for s in new_search_results]))
        else:
            print "no updates"
        pylab.pause(5)
        #time.sleep(5)  # wait >=5s to get more tweets


if __name__ == '__main__':
    main()
