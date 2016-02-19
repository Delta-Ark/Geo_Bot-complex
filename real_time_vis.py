#!/usr/bin/python
# real_time_vis.py
# Saito 2015
"""This grabs tweets and visualizes them in near real time.

USAGE: $ ./real_time_vis -h for help

Example using default parameter file 'params.txt', with 10 top words to display,
on a growing chart:

    $ ./real_time_vis --grow --number 10
Equivalently:
    $ ./real_time_vis -g -n 10

There is a delay in updating because Twitter API policy requires you
to wait 5 seconds between queries.

"""


import vis_helper
import geosearchclass
import argparse
import matplotlib.pyplot as plt


def update_fdist(fdist, new_words):
    for word in new_words:
        if fdist.has_key(word):
            fdist[word] += 1
        else:
            fdist[word] = 1
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


def updating_plot(geosearchclass, number_of_words, grow=False):
    search_results = geosearchclass.search()
    filtered_words = vis_helper.process(search_results)
    fdist = vis_helper.get_freq_dist(filtered_words)
    # set up plot
    samples = [item for item, _ in fdist.most_common(number_of_words)]
    samples.reverse()  # want most frequent on top
    if grow:
        samples.reverse()  # -> doesn't work for extension
    freqs = [fdist[sample] for sample in samples]
    plt.grid(True, color="silver")
    plt.plot(freqs, range(len(freqs)))
    plt.yticks(range(len(samples)), [s for s in samples])
    plt.ylabel("Samples")
    plt.xlabel("Counts")
    plt.title("Top Words Frequency Distribution")
    plt.ion()
    plt.show()

    # set up loop
    old_ids = set([s.id for s in search_results])
    product = []
    for i in xrange(100):
        plt.pause(5)
        geosearchclass.result_type = "recent"  # use mixed above, change to recent here
        # if i%2:  # for testing purposes
        #     #change location every odd time to nyc
        #     geosearchclass.latitude =40.734073
        #     geosearchclass.longitude =-73.990663
        # else:
        #     #now back to sf
        #     geosearchclass.latitude = 37.7821
        #     geosearchclass.longitude =  -122.4093

        search_results = geosearchclass.search()
        new_search_results = new_tweets(search_results, old_ids)
        if new_search_results:
            filtered_words = vis_helper.process(new_search_results)
            fdist = update_fdist(fdist, filtered_words)
            if grow:
                newsamples = [item for
                              item, _ in fdist.most_common(number_of_words)]
                s1 = set(newsamples)
                s2 = set(samples)
                s1.difference_update(s2)
                if s1:
                    print "New words: " + str(list(s1))
                    newsamples = list(s1)
                    samples.extend(newsamples)
                    #plt.yticks(range(len(samples)), [str(s) for s in samples])
                    plt.yticks(range(len(samples)), [s for s in samples])
            freqs = [fdist[sample] for sample in samples]
            plt.plot(freqs, range(len(freqs)))
            if grow:
                plt.draw()
            print '%d new tweet(s)' % len(new_search_results)
            old_ids.update(set([s.id for s in new_search_results]))
        else:
            print "no updates"


def get_parser():
    """ Creates a command line parser

    --doc -d 
    --filename -f
    --grow -g
    --number -n
    """
    # Create command line argument parser
    parser = argparse.ArgumentParser(
        description='Create an updating word frequency distribution chart.')

    parser.add_argument(
        '-d', '--doc', action='store_true',
        help='print module documentation and exit')
    parser.add_argument(
        '-f', '--filename',
        help='''specify a FILENAME to use as the parameter file. 
        If not specified, will use 'params.txt'.''')
    parser.add_argument(
        '-g', '--grow', action='store_true',
        help='Grow chart as new words arrive')
    parser.add_argument(
        '-n', '--number',
        help='specify NUMBER of words to display')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.doc:
        print __doc__
        import sys
        sys.exit()

    g = geosearchclass.GeoSearchClass()

    if args.filename:
        print 'Using parameters from ' + str(args.filename)
        g.set_params_from_file(args.filename)
    else:
        print "Using search values from params.txt"
        g.set_params_from_file('params.txt')

    if args.number:
        number = int(args.number)
    else:
        number = 30

    if args.grow:
        updating_plot(g, number, True)  # set grow flag to True
    else:
        updating_plot(g, number, False)


if __name__ == '__main__':
    main()
