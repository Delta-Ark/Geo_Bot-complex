#!/usr/bin/python
# test_write.py
# Saito 2015

""" Test unit for write """

import unittest
import time
import geosearchclass
import nltk
import logging
from write import traverse_tree_grab_phrase
from write import traverse_tree_grab_phrases
from write import parse_sentence
from write import get_grammar


class TestWrite(unittest.TestCase):
    # def __init__(self):
    #     super(TestWrite, self).__init__()

    @classmethod
    def setUpClass(cls):
        pass
        # self.g = geosearchclass.GeoSearchClass()
        # self.g.latitude = 37.7821
        # self.g.longitude = -122.4093
        # self.g.radius = 10
        # self.g.search_term = ""
        # self.g.result_type = 'mixed'
        # self.g.count = 2
        # self.sr = self.g.search()

    def setUp(self):
         # set to DEBUG, INFO, WARNING, ERROR, CRITICAL :
        logging.basicConfig(
            format='%(levelname)s:  %(message)s', level=logging.INFO)
        self.tokens = nltk.word_tokenize(
            'Numerous passing references to the phrase have occurred in movies')
        self.grammar = get_grammar('grammar_20ids_HM0VM0.pickle')
        self.tree = parse_sentence(self.tokens, self.grammar)

    def test_traverse_tree_grab_phrase(self):
        print 'printing tree!!!'
        print self.tree

        label = 'VP'
        phrase = traverse_tree_grab_phrase(self.tree, label)
        print "For label {} returned this phrase: {}".format(label, phrase)
        self.assertEqual(phrase, 'have occurred in movies')

        label = 'NP'
        phrase = traverse_tree_grab_phrase(self.tree, label)
        print "For label {} returned this phrase: {}".format(label, phrase)
        self.assertEqual(phrase, 'Numerous passing references')

        label = 'PP'
        phrase = traverse_tree_grab_phrase(self.tree, label)
        print "For label {} returned this phrase: {}".format(label, phrase)
        self.assertEqual(phrase, 'to the phrase')

    def test_traverse_tree_grab_phrases(self):
        # # Now testing other function
        labels = [u'VP', u'NP', u'PP']
        phrases = dict.fromkeys(labels)
        for k in phrases.keys():
            phrases[k] = []
        phrases = traverse_tree_grab_phrases(self.tree, phrases)
        for k, v in phrases.items():
            print '{} : {}'.format(k, v)
        self.assertEqual(
            phrases['NP'], ['Numerous passing references', 'the phrase', 'movies'])
        self.assertEqual(
            phrases['VP'], ['have occurred in movies', 'occurred in movies'])
        self.assertEqual(phrases['PP'], ['to the phrase'])  # maybe 'in movies'

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestWrite)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # tw = TestWrite()
    # tw.setUp()
    # tw.test_traverse_tree_grab_phrases()
