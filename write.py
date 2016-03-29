#!/usr/bin/python
# write.py
# Saito 2015

"""
This program is for doing automatic writing. 

It produces a JSON array with properties:
 phrase
 tweeter
 type
 geolocation


"""
# TODO:
# get tweets
# for each tweet:
# parse
# get phrases, tweeter, geo
# add to dictionary
# add dictionary to array
# Make a json array from list of dicts



import sys
import nltk
import json
import cPickle
from nltk.corpus import treebank
from nltk import treetransforms

def train_pcfg():
    print 'training grammar'
    productions = []
    #print len(treebank.fileids())
    trees = []
    for fileid in treebank.fileids()[0:10]: #add this for shorter grammar for quicker training
        for tree in treebank.parsed_sents(fileid):
            # perform optional tree transformations, e.g.:
            #  Remove branches A-B-C into A-B+C
            tree.collapse_unary(collapsePOS = False)
            # Remove A->(B,C,D) into A->B,C+D->D
            tree.chomsky_normal_form(horzMarkov = 2, vertMarkov=0) 
            productions += tree.productions()
    S = nltk.Nonterminal('S')
    grammar = nltk.induce_pcfg(S, productions)
    return grammar


    

def traverse_tree_grab_phrases(tree, phrases):
    for subtree in tree:
        print 'type of subtree= {}'.format(type(subtree))       
        if issubclass(subtree.__class__, nltk.tree.Tree):
            print 'this subtree has label {}'.format(subtree.label())
            if subtree.label() in phrases.keys():
                print 'found {} label'.format(subtree.label())
                tokens = subtree.leaves()
                phrase = ' '.join(tokens)
                print 'which has this phrase \n {}'.format(phrase)
                phrases[subtree.label()].append(phrase)
            print 'going one deeper'
            traverse_tree_grab_phrases(subtree, phrases)
        elif type(subtree)==unicode:
            print subtree
    return

def traverse_tree_grab_phrase(tree, label):
    phrase = None
    for subtree in tree:
        #print 'type of subtree= {}'.format(type(subtree))       
        if issubclass(subtree.__class__, nltk.tree.Tree):
            #print 'this subtree has label {}'.format(subtree.label())
            #print 'subtree {} == label {} : {}'.format(subtree.label(), label, subtree.label() == label)
            if subtree.label() == label:
                #print 'found {} label'.format(label)
                tokens = subtree.leaves()
                phrase = ' '.join(tokens)
                #print 'which has this phrase \n {}\n'.format(phrase)
                return phrase
            else:
                phrase = traverse_tree_grab_phrase(subtree, label)
                if phrase != None:
                    return phrase
    return phrase

def get_phrases(sentence_trees):
    labels = [u'VP', u'NP', u'PP']
    phrases = dict.fromkeys(labels)
    for k in phrases.keys():
        phrases[k]=[]
    print phrases
    for tree in sentence_trees:
        print tree
        for label in phrases.keys():
            #print '\n\n\n\nlooking for {}'.format(label)
            phrase = traverse_tree_grab_phrase(tree, label)
            if phrase != None:
                phrases[label].append(phrase)
    return phrases

def parse_sentences(sentences, grammar):
    """ Parses a list of sentences. Sentences must be tokenized first
    """
    parser = nltk.parse.ViterbiParser(grammar)
    trees = []
    for sent in sentences:
        for t in parser.parse(sent):
            trees.append(t)
    return trees

def json_phrases(phrases, filename):
    with open(filename, 'w') as f:
        j = json.dumps(phrases, indent=1)
        f.write(j)
    return

def pickle_grammar(grammar, fn):
    """ Write grammar to file (serialized, marshalled)
    """
    with open(fn, 'w') as f:
        cPickle.dump(grammar, f, protocol=cPickle.HIGHEST_PROTOCOL)

def unpickle_grammar(fn):
    """ Read grammar from a file and return it"""
    with open(fn, 'rU') as f:
        grammar = cPickle.load(f)
    return grammar

def get_grammar():
    fn = 'grammar.pickle'
    try:
        grammar = unpickle_grammar(fn)
        print 'Loaded grammar'
        return grammar
    except IOError:
        print 'No grammar file, gotta train'
        grammar = train_pcfg()
        pickle_grammar(grammar, fn)
        return grammar
        
        
        
    

def main():
    grammar = get_grammar()
    sents = treebank.sents()[0:10]
    print sents
    sentence_trees = parse_sentences(sents, grammar)
    phrases = get_phrases(sentence_trees)
    print 'Now printing the phrases: '
    for k,v in phrases.items():
        print '{} : {}'.format(k,v) 
    json_phrases(phrases, 'phrases.json')


    
if __name__ == '__main__':
    main()

