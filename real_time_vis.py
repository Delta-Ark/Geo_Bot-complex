#!/usr/bin/python
# fake_real_time_vis.py
# Saito 2015
"""This grabs tweets and visualizes them in fake real time.

Must wait 5 seconds between queries (5.5 to be safe)

"""


import time
import visualize
import geosearchclass
import real_time_vis

def main():
    fn = 'params.txt'
    print 'Using parameters from ' + fn
    g = geosearchclass.GeoSearchClass()
    g.set_params_from_file(fn)
    old_ids = set()
    product = []
    for i in xrange(4):        
        search_results = g.api_search()
        new_search_results = real_time_vis.new_tweets(search_results, old_ids)
        filtered_words = visualize.process(new_search_results)
        if filtered_words:
            product.extend(filtered_words)
        visualize.visualize_old(filtered_words)            
        old_ids = old_ids.update(set([s.id for s in search_results]))
        time.sleep(5)  # wait >=5s to get more tweets


if __name__ == '__main__':
    main()
