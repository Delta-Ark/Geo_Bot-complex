#!/usr/bin/python
# real_time_vis.py
# Saito 2015
"""This grabs tweets and visualizes them in near real time.

USAGE:
  $ python real_time_vis.py [-h][-d][-f FILENAME][-n NUMBER][-s][-a ADDRESS]
OR for help, try:
  $ ./real_time_vis.py -h
OR:
  $ python real_time_vis.py


Example using default parameter file 'params.txt', with 20 top words
to display, on a growing chart:

    $ ./real_time_vis --number 20
Or using the streaming API with an address:
    $ ./real_time_vis -n 20 -s -a "175 5th Avenue NYC"

There is a delay in updating with the REST API because Twitter API
policy requires you to wait 5 seconds between queries.

TO EXIT:
To exit one of these multithreaded programs, use a keyboard interrupt
like CTRL+C.

"""
from __future__ import division

import Queue
import argparse
import sys

import matplotlib.pyplot as plt

import geo_converter
import geosearchclass
import streamer
import vis_helper

global stream  # so that CTRL + C kills stream


def update_fdist(fdist, new_words):
    for word in new_words:
        if word in fdist:
            fdist[word] += 1
        else:
            fdist[word] = 1
    return fdist


def new_tweets(new_sr, old_ids):
    '''returns only search_results that do not have ids listed in old_ids
    new_sr is the new search results, old_ids is a set of ids

    '''
    new_tweets = []
    if old_ids:
        new_tweets = [sr for sr in new_sr if sr.id not in old_ids]
    else:
        new_tweets = new_sr
    return new_tweets


def remove_infrequent_words(samples, fdist):
    trimmed_samples = []
    for item in samples:
        if fdist[item] > 2:
            trimmed_samples.append(item)
    return trimmed_samples


def updating_plot(geosearchclass, number_of_words, grow=False):
    search_results = geosearchclass.search()
    filtered_words = vis_helper.process(search_results)
    fdist = vis_helper.get_freq_dist(filtered_words)
    # set up plot
    samples = [item for item, _ in fdist.most_common(number_of_words)]
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
    for i in xrange(100):
        plt.pause(5)
        # use mixed above, change to recent here
        geosearchclass.result_type = "recent"
        # perturbation study
        # if i%2:  # for testing purposes
        #     # #change location every odd time to nyc
        #     # geosearchclass.latitude =40.734073
        #     # geosearchclass.longitude =-73.990663
        #     # perturb latitude
        #     geosearchclass.latitude =geosearchclass.latitude + .001

        # else:
        #     #now back to sf
        #     # geosearchclass.latitude = 37.7821
        #     # geosearchclass.longitude =  -122.4093
        #     geosearchclass.longitude =geosearchclass.longitude + .001

        search_results = geosearchclass.search()
        new_search_results = new_tweets(search_results, old_ids)
        if new_search_results:
            filtered_words = vis_helper.process(new_search_results)
            fdist = update_fdist(fdist, filtered_words)
            if grow:
                newsamples = [item
                              for item, _ in fdist.most_common(number_of_words)
                              ]
                s1 = set(newsamples)
                s2 = set(samples)
                s1.difference_update(s2)
                if s1:
                    print "New words: " + str(list(s1))
                    newsamples = list(s1)
                    samples.extend(newsamples)
                    plt.yticks(range(len(samples)), [s for s in samples])
            freqs = [fdist[sample] for sample in samples]
            plt.plot(freqs, range(len(freqs)))
            if grow:
                plt.draw()
            print '%d new tweet(s)' % len(new_search_results)
            old_ids.update(set([s.id for s in new_search_results]))
        else:
            print "no updates"

# g = geosearchclass.GeoSearchClass()
# g.set_params_from_file('params.txt')
# search_results = g.search()


def updating_stream_plot(q, number_of_words=30):
    """This plot uses the streaming API to get real time twitter
    information from a given region, determined by a geo-coordinate
    bounding box. The upper left and lower right determine the
    bounding box.

    q is a queue instance, which holds tweets
    
    number_of_words determines the average number of words in the
    plot. Once the plot reaches 2 x number_of_words, it is shrunk down
    to the new set of words and starts growing again

    To exit the program early, hit CTRL + Z to stop the python script
    and then CTRL + D twice to kill the terminal process and close the
    window.

    """
    setup = False
    fdist = None
    samples = None
    draw_time = 0.1
    samples = []
    plt.ion()
    plt.grid(True, color="silver")

    for i in range(100000):
        status = q.get()
        search_results = [status]
        while not q.empty():
            print "getting another tweet"
            status = q.get()
            search_results.append(status)

        if not setup:
            print "Gathering enough data to begin plotting"
            while len(samples) < 1:
                status = q.get()
                search_results.append(status)
                filtered_words = vis_helper.process(search_results)
                if fdist is None:
                    fdist = vis_helper.get_freq_dist(filtered_words)
                else:
                    fdist = update_fdist(fdist, filtered_words)
                n_words = min(10, len(fdist))
                samples = [item for item, _ in fdist.most_common(n_words)]
                # print "len(samples) = {}".format(len(samples))
                samples = remove_infrequent_words(samples, fdist)
            freqs = [fdist[sample] for sample in samples]
            plt.plot(freqs, range(len(freqs)))
            plt.yticks(range(len(samples)), [s for s in samples])
            plt.ylabel("Samples")
            plt.xlabel("Counts")
            plt.title("Top Words Frequency Distribution")
            plt.show()
            plt.pause(draw_time)
            setup = True

        else:
            filtered_words = vis_helper.process(search_results)
            fdist = update_fdist(fdist, filtered_words)
            newsamples = [item
                          for item, _ in fdist.most_common(number_of_words)]
            newsamples = remove_infrequent_words(newsamples, fdist)
            s1 = set(newsamples)
            s2 = set(samples)
            s1.difference_update(s2)
            if s1:
                print "New words: " + str(list(s1))
                newsamples = list(s1)
                samples.extend(newsamples)
                if len(samples) > 2*number_of_words:
                    samples = newsamples
                    plt.close()
                plt.yticks(range(len(samples)), [s for s in samples])
            freqs = [fdist[sample] for sample in samples]
            plt.plot(freqs, range(len(freqs)))
            plt.draw()
            plt.pause(draw_time)
    kill_plot()
    return


def kill_plot():
    print "turning interactive off"
    plt.ioff()
    print "closing plot"
    plt.close()
    return


def get_parser():
    """ Creates a command line parser

    --doc -d
    --help -h
    --filename -f
    --grow -g
    --number -n
    """
    # Create command line argument parser
    parser = argparse.ArgumentParser(
        description='Create an updating word frequency distribution chart.')

    parser.add_argument('-d',
                        '--doc',
                        action='store_true',
                        help='print module documentation and exit')
    parser.add_argument(
        '-f',
        '--filename',
        help='''specify a FILENAME to use as the parameter file.
        If not specified, will use 'params.txt'.''')
    parser.add_argument(
        '-a',
        '--address',
        help='''give an ADDRESS to get geocoordinates for.''')
    # parser.add_argument('-r',
    #                     '--rest',
    #                     action='store_true',
    #                     help='Use the REST API to create a growing chart\
    #                     as new words arrive.')
    parser.add_argument('-n',
                        '--number',
                        help='specify NUMBER of words to display. The\
                        streaming plot will grow to twice this number\
                        before shrinking again')
    parser.add_argument('-s',
                        '--stream',
                        action='store_true',
                        help='Use streaming API to update a growing plot. \
                        Use Interrupt signal, like CTRL + C to exit. \
                        This uses the LOCATION and SEARCH_TERM from\
                        parameter file. The geolocation is approximately\
                        converted, by inscribing a bounding box square in the\
                        circle around the geocoordinates. Also, a search term\
                        searches all tweets, while geolocation searches only\
                        in that area (unlike the REST API).')

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    # print args
    # print args.help
    
    if args.doc:
        print __doc__
        import sys
        sys.exit(0)

    if args.number:
        number = int(args.number)
    else:
        number = 30

    g = geosearchclass.GeoSearchClass()

    if args.filename:
        print 'Using parameters from ' + str(args.filename)
        g.set_params_from_file(args.filename)
    else:
        print "Using search values from params.txt"
        g.set_params_from_file('params.txt')

    if args.address:
        print "Finding geocoordates for address:\n{}".format(args.address)
        coords = geo_converter.get_geocoords_from_address(args.address)
        if coords:
            g.latitude = coords[0]
            g.longitude = coords[1]
        else:
            print "Failed to find coordinates"
            sys.exit()
    
    if args.stream:
        print "using streaming queue"
        q = Queue.Queue()
        bounding_box = geo_converter.get_bounding_box_from(g)
        search_terms = geo_converter.get_search_terms_from(g)
        print "bounding_box = {}".format(bounding_box)
        print "search_terms = {}".format(search_terms)
        global stream
        fn = 'tweets.json'
        stream = streamer.start_stream(q, bounding_box, fn, search_terms)
        updating_stream_plot(q, number)
    else:
        print "using REST API updating plot"
        updating_plot(g, number, True)  # set grow flag to True


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Main function interrupted"
        if "stream" in globals():
            streamer.kill_stream(stream)
        kill_plot()
        sys.exit()
