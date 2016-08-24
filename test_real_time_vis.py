#!/usr/bin/python
# test_real_time_vis.py
# Saito 2015
""" Test unit for real_time_vis """

import unittest
import time
from utils import new_tweets
from real_time_vis import update_fdist
import geosearchclass
import utils


class TestRTV(unittest.TestCase):

    def setUp(self):
        self.g = geosearchclass.GeoSearchClass()
        self.g.latitude = 37.7821
        self.g.longitude = -122.4093
        self.g.radius = 100
        self.g.search_term = ""
        self.g.result_type = 'mixed'
        self.g.count = 100
        self.sr = self.g.search()

    def test_new_tweets(self):
        sr2 = self.sr[0:10]  # 10 old same one
        old = [s.id for s in sr2]
        old = set(old)
        print 'len(sr) = %d' % len(self.sr)
        print 'len(sr2) = %d' % len(sr2)
        self.assertEqual(
            len(new_tweets(self.sr, old)), 90)

        sr2 = self.sr
        old = [s.id for s in sr2]
        old = set(old)
        self.assertEqual(
            len(new_tweets(self.sr, old)), 0)

        self.g.latitude = 40.734073
        self.g.longitude = -73.990663
        self.g.radius = 10
        self.g.search_term = ""
        self.g.result_type = 'mixed'
        self.g.count = 10
        sr2 = self.g.search()    # all different (15 old different ones)
        old = [s.id for s in sr2]
        old = set(old)
        self.assertEqual(
            len(new_tweets(self.sr, old)), 100)

    def test_update_fdist(self):
        filtered_words = utils.tokenize_and_filter(self.sr)
        fdist = utils.get_freq_dist(filtered_words)
        # take distribution and send it empty list
        fdist2 = update_fdist(fdist, [])
        self.assertEqual(fdist, fdist2)

        time.sleep(5)
        self.g.latitude = 40.734073
        self.g.longitude = -73.990663
        self.g.count = 100
        self.sr = self.g.search()
        filtered_words = utils.tokenize_and_filter(self.sr)
        # updating with entirely new word set -> should be longer
        old_len_fdist = len(fdist)
        fdist = update_fdist(fdist, filtered_words)
        self.assertTrue(len(fdist) > old_len_fdist)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
