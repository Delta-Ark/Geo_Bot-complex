#!/usr/bin/python
# write.py
# Saito 2015

"""
This program classifies tweets into phrase type.

It produces a JSON array, "phrases.json" with properties:
 phrase
 tweeter
 type
 geolocation
"""
# TODO:
# Try a faster parser, like chart parser or something


import nltk
import json
import cPickle
import re
import types
import logging
from nltk.corpus import treebank
from nltk import treetransforms
#from nltk.grammar import WeightedProduction, Nonterminal
from nltk.grammar import ProbabilisticProduction, Nonterminal


class PCFGViterbiParser(nltk.ViterbiParser):

    def __init__(self, grammar, trace=0):
        super(PCFGViterbiParser, self).__init__(grammar, trace)

    def parse(self, tokens):
        tagged = nltk.pos_tag(tokens)
        missing = False
        for tok, pos in tagged:
            if not self._grammar._lexical_index.get(tok):
                missing = True
                self._grammar._productions.append(
                    ProbabilisticProduction(Nonterminal(pos), [tok], prob=0.000001))
# WeightedProduction(Nonterminal(pos), [tok], prob=0.000001))
        if missing:
            self._grammar._calculate_indexes()

        # returns a generator, so call 'next' to get the ProbabilisticTree
        tree = super(PCFGViterbiParser, self).parse(tokens)
        if issubclass(tree.__class__, nltk.tree.Tree):
            print 'returning a tree'
            return tree
        elif isinstance(tree, types.GeneratorType):
            try:
                return next(tree)
            except(StopIteration):
                tweet = ' '.join(tokens)
                print u'Couldn\'t parse {}'.format(tweet)
                return None
        else:
            error("Type of tree is: {}".format(type(tree)))


def train_pcfg():
    print 'training grammar'
    productions = []
    # print len(treebank.fileids())
    trees = []
    # up to 199 less for shorter grammar for quicker training
    for fileid in treebank.fileids()[0:20]:
        for tree in treebank.parsed_sents(fileid):
            # perform optional tree transformations, e.g.:
            # Remove branches A->B->C into A->B+C so we can avoid infinite
            # productions
            tree.collapse_unary(collapsePOS=False)
            # Remove A->(B,C,D) into A->B,C+D->D (binarization req'd by CKY parser)
            # horizontal and vertical Markovization: remember parents and siblings in tree
            #     This gives a performance boost, but makes the grammar HUGE
            #     If we use these we would need to implement a tag forgetting method
            #tree.chomsky_normal_form(horzMarkov = 0, vertMarkov=0)
            tree.chomsky_normal_form()
            productions += tree.productions()
    S = nltk.Nonterminal('S')
    grammar = nltk.induce_pcfg(S, productions)
    print "grammar trained!"
    return grammar


def traverse_tree_grab_phrases(tree, phrases):
    """Finds all examples of each label and returns the phrases dictionary.

    Usage: phrases = traverse_tree_grab_phrase(tree, 'VP')

    Phrases is a dictionary with a key for each label you which to
    find, and each value is a list.
    """

    for subtree in tree:
        logging.debug('type of subtree= {}'.format(type(subtree)))
        if issubclass(subtree.__class__, nltk.tree.Tree):
            logging.debug('this subtree has label {}'.format(subtree.label()))
            if subtree.label() in phrases.keys():
                logging.debug('found {} label'.format(subtree.label()))
                tokens = subtree.leaves()
                phrase = ' '.join(tokens)
                logging.debug(u'which has this phrase \n {}'.format(phrase))
                phrases[subtree.label()].append(phrase)
            logging.debug('going one deeper')
            phrases = traverse_tree_grab_phrases(subtree, phrases)
        elif type(subtree) == unicode:
            logging.debug(subtree)
    return phrases


def traverse_tree_grab_phrase(tree, label):
    """Finds the first example of the label and returns the phrase.

    Usage: phrase = traverse_tree_grab_phrase(tree, 'VP')

    For exhaustive search try the sister function
    traverse_tree_grab_phrases(tree,phrases)
    """
    phrase = None
    logging.debug("tree type: {}".format(type(tree)))

    for subtree in tree:
        logging.debug('type of subtree= {}'.format(type(subtree)))
        if issubclass(subtree.__class__, nltk.tree.Tree):
            logging.debug('this subtree has label {}'.format(subtree.label()))
            logging.debug('subtree {} == label {} : {}'.format(
                subtree.label(), label, subtree.label() == label))
            if subtree.label() == label:
                logging.debug('found {} label'.format(label))
                tokens = subtree.leaves()
                phrase = ' '.join(tokens)
                logging.debug(u'which has this phrase \n {}\n'.format(phrase))
                return phrase
            else:
                phrase = traverse_tree_grab_phrase(subtree, label)
                if phrase != None:
                    return phrase
    return phrase


def get_phrases_from_tree(tree, exhaustive=False):
    labels = [u'VP', u'NP', u'PP']
    phrases = dict.fromkeys(labels)
    for k in phrases.keys():
        phrases[k] = []
    if exhaustive:
        phrases = traverse_tree_grab_phrases(tree, phrases)
    else:
        for label in phrases.keys():
            # print '\n\n\n\nlooking for {}'.format(label)

            phrase = traverse_tree_grab_phrase(tree, label)

            if phrase is not None:
                phrases[label].append(phrase)
    return phrases


def parse_sentence(tokenized_sentence, grammar):
    """ Parses a tokenized sentence and returns a tree
    """
    #    parser = nltk.parse.ViterbiParser(grammar)
    parser = PCFGViterbiParser(grammar, trace=0)
    tree = parser.parse(tokenized_sentence)
    return tree


def json_phrases(phrases, filename):
    with open(filename, 'w') as f:
        j = json.dumps(phrases, indent=1)
        f.write(j)
    return


def pickle_grammar(grammar, fn):
    """ Write grammar to file (serialized, marshalled)
    """
    with open(fn, 'w') as f:
        #cPickle.dump(grammar, f, protocol=cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(grammar, f, protocol=0)


def unpickle_grammar(fn):
    """ Read grammar from a file and return it"""
    with open(fn, 'rU') as f:
        grammar = cPickle.load(f)
    return grammar


def get_grammar(fn='grammar.pickle'):

    try:
        grammar = unpickle_grammar(fn)
        print 'Loaded grammar'
        return grammar
    except IOError:
        print 'No grammar file, gotta train'
        grammar = train_pcfg()
        pickle_grammar(grammar, fn)
        return grammar


def create_info_phrase_add_to_list(phrases, status, dict_list):
    keys = ['phrase', 'phrase_type', 'tweet',
            'coordinates', 'time', 'screen_name']

    for pos in phrases:
        for phrase in phrases[pos]:
            print u'phrase: {}'.format(phrase)
            d = dict.fromkeys(keys)
            d['phrase_type'] = pos
            d['phrase'] = phrase
            d['tweet'] = status.text
            d['screen_name'] = status.user.screen_name
            d['time'] = str(status.created_at)
            if status.geo:
                d['coordinates'] = status.geo['coordinates']
            dict_list.append(d)
            del d

    return


def parse_tweets(search_results):
    grammar = get_grammar('grammar_20ids_HM0VM0.pickle')
    list_of_info_dicts = []
    for sr in search_results:
        print u'tweet text: {}'.format(sr.text)
        #        nltk.tree.Tree.draw(tree)
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sentence_detector.tokenize(sr.text)
        tokenizer = nltk.tokenize.casual.TweetTokenizer()
        for sent in sentences:
            if not sent:
                logging.debug('sent is None')
                continue
            tokens = tokenizer.tokenize(sent)
            logging.debug(tokens)
            p = re.compile(r'https.*')
            #        tokens = [word for word in tokens if not word == u'\xe2']
            tokens = [word for word in tokens if not p.match(word)]
            logging.debug(tokens)
            if not tokens:
                continue
            tree = parse_sentence(tokens, grammar)
            if not tree:
                logging.debug('tree was None')
                continue
            print tree
            phrases = get_phrases_from_tree(tree, exhaustive=True)
            print 'printing phrases dictionary for this tweet'
            for k, v in phrases.items():
                print u'{} : {}'.format(k, v)

            create_info_phrase_add_to_list(phrases, sr, list_of_info_dicts)

    i = 1
    for d in list_of_info_dicts:
        print '\n\n\n printing dictionary {}'.format(i)
        for k, v in d.items():
            print u'{} : {}'.format(k, v)
        i += 1

    json_phrases(list_of_info_dicts, 'phrases.json')
    return list_of_info_dicts


def main():
     # set to DEBUG, INFO, WARNING, ERROR, CRITICAL :
    logging.basicConfig(
        format='%(levelname)s:  %(message)s', level=logging.INFO)
    import geosearchclass
    g = geosearchclass.GeoSearchClass()
    print "Using search values from params.txt"
    g.set_params_from_file('params.txt')
    search_results = g.search()
    parse_tweets(search_results)
    # grammar = get_grammar()
    # #sentences = treebank.sentences()[34:35]
    # sentences = [nltk.word_tokenize('Numerous passing references to the phrase have occurred in movies')]
    # #print sentences

    # sentence_trees = parse_sentences(sentences, grammar)
    # phrases = get_phrases(sentence_trees)
    # print 'Now printing the phrases: '
    # for k,v in phrases.items():
    #     print '{} : {}'.format(k,v)
    # json_phrases(phrases, 'phrases.json')


if __name__ == '__main__':
    main()
