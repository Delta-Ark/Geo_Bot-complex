#!/usr/bin/python
# real_time_vis.py
# Saito 2015
"""
Must wait 5 seconds between queries (5.5 to be safe)
"""

import threading, time, argparse
import visualize, geotweets, geosearchclass


      
product = []
lock = threading.Lock()

class Producer( threading.Thread ):
    def __init__(self,geosearcher):
        threading.Thread.__init__(self)
        self.geosearcher = geosearcher
        
    def run ( self ):
        while True:
            with lock:
                search_results = self.geosearcher.api_search()
                filtered_words = visualize.process(search_results)
                product.extend( filtered_words)
                print 'Thread', self.getName(), 'ended'
            time.sleep(5)




class Consumer( threading.Thread ):
    def run ( self ):
        while True:
            with lock:
                print 'Thread', self.getName(), 'started.'
                visualize.visualize(product)
                print 'Thread', self.getName(), 'ended'
            time.sleep(5)

        



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


    

        







    

# Standard boilerplate to call the main() function to begin
# the program.         
if __name__ == '__main__':
    main()
