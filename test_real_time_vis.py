#!/usr/bin/python
# test_real_time_vis.py
# Saito 2015
""" Test unit for real_time_vis """

import unittest
from real_time_vis import new_tweets
import geosearchclass
 
class TestRTV(unittest.TestCase):
 
    def setUp(self):                
        self.g = geosearchclass.GeoSearchClass()        
        self.g.latitude =37.7821
        self.g.longitude =-122.4093
        self.g.radius =10
        self.g.search_term=""
        self.g.result_type='mixed'
        self.g.count = 100
        self.sr = self.g.search()

    def test_new_tweets(self):
        sr2 = self.sr[0:10]  # 10 old same one
        old = [s.id for s in sr2]
        old = set(old)
        #print 'len(sr) = %d' % len(self.sr)
        #print 'len(sr2) = %d' % len(sr2)
        self.assertEqual(
            len(new_tweets(self.sr,old)),90)

        sr2 = self.sr
        old = [s.id for s in sr2]
        old = set(old)
        self.assertEqual(
            len(new_tweets(self.sr,old)),0)

        self.g.latitude = 40.734073
        self.g.longitude =-73.990663
        self.g.radius =10
        self.g.search_term=""
        self.g.result_type='mixed'
        self.g.count = 10        
        sr2 = self.g.search()    # all different (15 old different ones)
        old = [s.id for s in sr2]
        old = set(old)
        self.assertEqual(
            len(new_tweets(self.sr, old)),100)


    def tearDown(self):
        pass 
if __name__ == '__main__':
    unittest.main()
