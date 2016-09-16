#!/usr/bin/python
# suggest_bot.py
# Saito 2016

"""This creates robot assisted poems!


"""
import argparse
import codecs
import os
import random
import sys

import geosearchclass
import utils


def create_poem(words):
    """ This creates a poem with user input by suggesting from the words supplied.

    A user can use the word, decline the word, or add their own input.
    """
    poem = []
    # for no, yes and finish (print poem)
    options = ['y', 'n', 'f']
    keep_adding = True
    print """
        This robot poet will present a series of suggestions. You can
        either choose to use these suggestions by typing 'y' (for
        yes), or 'n' (for no, give me another word) or by typing your
        own input then hitting enter. These will be succeessively
        added to a poem, which will be printed and saved to an output
        file. To finish writing type f (for finish).

        y: yes use this word or phrase
        n: no, skip this and give me a new phrase
        f: finish writing
    """
    while keep_adding:
        chosen = random.choice(for_poem)
        print chosen,
        response = raw_input("[Enter y, n, or f or your own prose] :  ")
        # include the chosen word:
        if response == "y":
            poem.append(chosen)
            formatted_poem = " ".join(poem),
            print formatted_poem,
            # regenerate new work:
        if response == "n":
            chosen = random.choice(for_poem),
            formatted_poem = " ".join(poem),
            print formatted_poem,
            # add the poets' thing:
        if response not in options:
            if response == "\\n":
                response = '\n'
            poem.append(response),
            formatted_poem = " ".join(poem),
            print formatted_poem,
            # print"
        if response == "f":
            formatted_poem = " ".join(poem)
            print ""
            print formatted_poem
            keep_adding = False
    return formatted_poem


def get_parser():
    """ Creates a command line parser

    --doc -d
    --help -h
    --params_file -p
    --output -o
    --search -s

    This automatically grabs arguments from sys.argv[]
    """

    parser = argparse.ArgumentParser(
        description='Create a robot assisted poem.')

    parser.add_argument(
        '-d', '--doc', action='store_true',
        help='print module documentation and exit')
    parser.add_argument(
        '-p', '--params_file',
        help='''specify a PARAMS_FILE to use as the parameter file.
        If not specified, will use 'params.txt'.''')
    parser.add_argument(
        '-s', '--search', action='store_true',
        help="""Perform a geolocated tweet search using the params
        file and use the vocab from this to add to the poems""")
    parser.add_argument(
        '-o', '--output',
        help='''specify an OUTPUT file to write to.
        Default is output.txt''')

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.doc:
        print __doc__
        sys.exit()

    if args.search:
        g = geosearchclass.GeoSearchClass()
        if args.params_file:
            print 'Using parameters from ' + str(args.filename)
            # turn parameter file into dictionary
            g.set_params_from_file(args.filename)
        search_results = g.search()
        filtered_words = utils.tokenize_and_filter(search_results)
        print filtered_words
        for_poem.extend(filtered_words)

    formatted_poem = create_poem(for_poem)
    
    if args.output:
        print 'writing formatted poem to ' + str(args.output)
        output_file = args.output
    else:
        print "writing formatted poem to output.txt"
        output_file = "output.txt"

    fileSystemEncoding = sys.getfilesystemencoding()
    OUTPUT_FILE = os.path.expanduser(u'./' + output_file)
    with codecs.open(OUTPUT_FILE,
                     encoding=fileSystemEncoding,
                     mode="w") as f:
        f.write(formatted_poem)


# These are some good default words used in the poem creator above
for_poem = [
    # emerging tech shit
    'Agricultural', 'ecological', 'systems', 'meat', 'genetically',
    'modified', 'precision', 'vertical', 'farming', 'printing', 'contour',
    'crafting', 'artificial', 'uterus', 'transplant', 'cryonics',
    'vitrification', 'suspended animation', 'de-extinction',
    'genetic engineering', 'gene therapy', 'life extension',
    'engineered negligible senescence',
    'nanomedicine', 'nanosensors', 'regenerative', 'medicine',
    'stem-cell', 'tissue engineering', 'robot assisted surgery',
    'synthetic biology', 'synthetic genomics', 'virus',
    'whole genome sequencing', 'bionic contact lens',
    'head-mounted display', 'virtual',
    'retinal', 'e-textiles', 'molecular', 'electronics', 'thermal',
    'copper', 'pillar', 'airborne wind turbine', 'artificial',
    'photosynthesis', 'biofuels', 'solar', 'power', 'fusion', 'fuel cell',
    'molten salt', 'photovoltaic', 'translation', 'machine vision',
    'speech recognition', 'fourth-generation', 'optical discs', 'storage',
    'holographic data', 'millipede', 'optical computing',
    'quantum computing', 'quantum cryptography', 'RFID', 'software-defined',
    'three-dimensional', 'integrated', 'circuit', 'artificial muscle',
    'superconductivity', 'superfluidity', 'metamaterials', 'cloaking',
    'metal', 'multi-function', 'superalloy', 'synthetic diamond',
    'weapon', 'laser', 'particle-beam', 'coilgun', 'plasma', 'stealth',
    'brain computer interface', 'retinal implant',
    'self reconfiguring modular robot', 'swarm robotics', 'pulse',
    'solar sail', 'backpack',
    'helicopter', 'delivery drone', 'detonation', 'engine', 'driverless\
    car', 'automated', 'vacuum', 'collection', 'cloak', 'immersive',
    'dilemma',
    # japanese shit
    'august', 'black', 'chinese', 'Gaugin', 'heaven', 'illusion',
    'island', 'Kibune', 'Michinoku', 'milky', 'Mogami', 'mother',
    'mount', 'mountain', 'Musashi', 'night', 'observe', 'October',
    'portrait', 'river', 'Roman', 'SUNSHINE', 'should', 'submit',
    'tangled', 'Tokiwa', 'washing', 'watching', 'world', 'Yoshino',
    'actual', 'admires', 'after', 'afterlife', 'again', 'against',
    'alive', 'almost', 'always', 'amidah', 'ancient', 'another',
    'armor', 'armored', 'arrayed', 'arrows', 'autumn', 'autumns',
    'awakening', 'bamboo', 'bathe', 'beads', 'become', 'becoming',
    'begins', 'behind', 'between', 'beyond', 'birth', 'blade',
    'blind', 'bloom', 'blooming', 'blossoms', 'break', 'breaks',
    'breeze', 'bridge', 'brings', 'brother', 'brush', 'buried',
    'burning', 'butterfly', 'calligraphy', 'calling', 'camellia',
    'cancer', 'candle', 'canyon', 'caress', 'carry', 'ceaseless',
    'cedars', 'center', 'certain', 'change', 'chanted', 'chases',
    'cherries', 'cherry', 'child', 'chill', 'chorus', 'chrysanthemum',
    'chrysanthemums', 'cicada', 'clock', 'closer', 'color', 'combing',
    'compare', 'completely', 'content', 'continent', 'corona',
    'could', 'crest', 'crossing', 'curve', 'dancers', 'darkens',
    'darkness', 'death', 'deepens', 'delusions', 'deserted',
    'destitute', 'distance', 'dream', 'dreaming', 'dreams', 'drips',
    'drops', 'drums', 'dying', 'early', 'eclipse', 'egret', 'ended',
    'entangling', 'escaped', 'evening', 'every', 'exhausted',
    'faintly', 'falling', 'falls', 'feeling', 'field', 'finished',
    'fireflies', 'firefly', 'fireworks', 'first', 'flash', 'flesh',
    'flies', 'float', 'flowers', 'flowing', 'flows', 'follow',
    'forever', 'forlorn', 'forth', 'fragile', 'frozen', 'garden',
    'gates', 'gauntlet', 'gauzy', 'gazing', 'geese', 'giant',
    'glances', 'going', 'grapes', 'grass', 'grasses', 'guards',
    'guided', 'gunshots', 'harbor', 'heart', 'heaven', 'hillside',
    'holding', 'horse', 'house', 'houses', 'hundred', 'hydrangea',
    'idling', 'image', 'insane', 'interrogation', 'invisible',
    'irrevocable', 'itself', 'journey', 'juice', 'karma', 'killed',
    'knotty', 'knowing', 'knowledge', 'later', 'leave', 'leaving',
    'letting', 'light', 'lightning', 'lilacs', 'limit', 'little',
    'lodging', 'longing', 'looks', 'loving', 'making', 'mantle',
    'marshes', 'memories', 'messengers', 'meteor', 'midnight',
    'might', 'mirror', 'mirrored', 'missed', 'month', 'moonlight',
    'mother', 'motorcycle', 'mouth', 'moving', 'myself', 'night',
    'nightingale', 'nights', 'north', 'nothing', 'nowhere', 'ocean',
    'octopus', 'opening', 'orchid', 'other', 'paradise', 'parting',
    'passes', 'passions', 'pattern', 'pealing', 'pears', 'people',
    'period', 'petal', 'place', 'plain', 'planters', 'playing',
    'poems', 'poppy', 'press', 'primal', 'primeval', 'purple',
    'quivered', 'rabbits', 'radiation', 'radio', 'rapids', 'reaches',
    'reality', 'really', 'recklessly', 'reconciled', 'relax',
    'remember', 'replies', 'returning', 'right', 'ripple', 'ripples',
    'rising', 'river', 'riverbank', 'rocky', 'rowing', 'running',
    'saying', 'seals', 'seeing', 'serpent', 'shadow', 'shall',
    'shaped', 'shattered', 'shell', 'shelves', 'shift', 'shining',
    'shore', 'short', 'shower', 'sided', 'silkworm', 'silkworms',
    'single', 'sleep', 'slept', 'slightest', 'slowly', 'smell',
    'snail', 'soiled', 'soldiers', 'solitary', 'somehow', 'something',
    'sometimes', 'sound', 'speak', 'spill', 'spilling', 'spray',
    'spreads', 'spring', 'squid', 'stable', 'stars', 'station',
    'steel', 'stirrups', 'stolen', 'stomach', 'stone', 'storm',
    'straighten', 'strands', 'strange', 'straw', 'streaming',
    'stripes', 'study', 'submit', 'summer', 'sunlight', 'sunrise',
    'sunset', 'sutra', 'sweet', 'swimsuit', 'tangled', 'taste',
    'temple', 'tethered', 'their', 'there', 'these', 'thighs',
    'thing', 'things', 'think', 'thought', 'thousand', 'throat',
    'through', 'throughout', 'tiger', 'tight', 'tossing', 'total',
    'toward', 'trace', 'transferred', 'traps', 'truth', 'turning',
    'turns', 'twilight', 'unborn', 'under', 'utterly', 'vanished',
    'village', 'visible', 'waiting', 'wandering', 'warrior',
    'warriors', 'washed', 'water', 'waves', 'weight', 'where',
    'which', 'whistling', 'white', 'whitecaps', 'willow', 'wings',
    'winter', 'wisteria', 'without', 'woman', 'world', 'yanking',
    'years', 'yesterday', 'yielded', 'young']


if __name__ == '__main__':
    main()
