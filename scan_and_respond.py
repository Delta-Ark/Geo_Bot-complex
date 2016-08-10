#!/usr/bin/python
# real_time_vis.py
# Saito 2015

"""
Scans tweets and asks the user to verify them before sending a tweet response.

A queue is created of tweets as they arrive via the REST API. The user
is then asked to look over these tweets and decide if they are
relevant. If they are, the relevant parts are saved to a JSON file. If
they respond flag -r was passed, a public tweet is sent out with the
user tagged in it.

"""

from __future__ import division

import Queue
import argparse
import json
import threading
import sys
import time

import geo_converter
import geosearchclass
from utils import new_tweets
import utils


def scan(geosearchclass, q):
    global keep_scanning
    search_results = geosearchclass.search()
    old_ids = [sr.id for sr in search_results]
    for s in search_results:
        q.put(s)
    while keep_scanning:
        for i in range(5):
            if keep_scanning:
                time.sleep(1)
            else:
                return
        geosearchclass.result_type = "recent"
        search_results = geosearchclass.search()
        new_search_results = new_tweets(search_results, old_ids)
        if new_search_results:
            for nsr in new_search_results:
                q.put(nsr)
    return


def verify(geosearchclass, filename):
    q = Queue.Queue()
    global keep_scanning
    keep_scanning = True
    thread = threading.Thread(target=scan, args=(geosearchclass, q))
    thread.daemon = True
    thread.start()
    respond = False
    with open(filename, 'a') as json_file:
        json_file.seek(0)
        json_file.truncate()

        print """\n\n\tThis program will present a series of tweets and ask for you to
        verify if they should be responded to. If so, they will be saved
        to the JSON file. When you quit scanning, the public tweets will
        be sent out.\n"""

        print """Would you like to send tweet responses at the end of this verification
        session?"""
        response = ""
        while response != 'y' and response != 'n':
            response = raw_input("[y for Yes, n for No] :  ")
            print response
        if response == 'y':
            respond = True
        elif response == 'n':
            respond = False

        first = True
        while True:
            if q.empty():
                time.sleep(5)
                continue
            status = q.get()
            print "\n\nVerify if this tweet is what you want:"
            simplified_tweet = utils.get_simplified_tweet(status)
            response = ""
            while response != 'y' and response != 'n' and response != 'q':
                response = raw_input("[y for Yes, n for No, q for Quit] :  ")
            if response == 'y':
                j = json.dumps(simplified_tweet, indent=1)
                if first:
                    json_file.write('[\n')
                    json_file.write(j)
                    first = False
                    continue
                json_file.write(',\n')
                json_file.write(j)
            elif response == 'n':
                continue
            elif response == 'q':
                keep_scanning = False
                thread.join()
                json_file.write('\n]')
                break
    responder(respond, filename)
    return


def responder(respond, filename):
    if not respond:
        print "No responses sent!"
        return
    print "\n\nResponding to :"
    with open(filename, 'rU') as json_file:
        json_string = json_file.read()
        tweets = json.loads(json_string)
        for tweet in tweets:
            print '\n'
            for el in tweet:
                print el
    return


def get_parser():
    """ Creates a command line parser

    --doc -d
    --help -h
    --filename -f
    --respond -r
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
    parser.add_argument('-a',
                        '--address',
                        help='''give an ADDRESS to get geocoordinates for.''')
    parser.add_argument(
        '-o', '--output',
        help='''specify an OUTPUT file to write to.
        Default is tweets.json''')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.doc:
        print __doc__
        import sys
        sys.exit(0)

    g = geosearchclass.GeoSearchClass()

    if args.filename:
        print 'Using parameters from ' + str(args.filename)
        g.set_params_from_file(args.filename)
    else:
        print "Using search values from params.txt"
        g.set_params_from_file('params.txt')

    if args.output:
        fn = str(args.output)
    else:
        fn = 'tweets.json'
    print 'Output file: ' + fn

    if args.address:
        print "Finding geocoordates for address:\n{}".format(args.address)
        coords = geo_converter.get_geocoords_from_address(args.address)
        if coords:
            g.latitude = coords[0]
            g.longitude = coords[1]
        else:
            print "Failed to find coordinates"
            sys.exit()

    verify(g, fn)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Main function interrupted"
        print "JSON file may be in incomplete format"
        sys.exit()
