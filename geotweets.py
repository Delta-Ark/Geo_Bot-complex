#!/usr/bin/python
# geotweets.py
# Saito 2015

"""This program is for grabbing and saving geo-located tweets


USAGE:
  $ ./geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT][-vis]

Print command line help:
  $ ./geotweets.py --help   (or just -h)

Example: This uses parameter file 'params.txt', prints results to
command line and writes them to 'out.txt': 
  $ ./geotweets.py --verbose --filename params.txt --output out.txt

The program requires a file in this folder called consumerkeyandsecret
which contains only a consumer key on the first line and consumer
secret (the longer one) on the second line. You can get this by
creating an app under your twitter account online.

The program can optionally take a parameter file as input. This file,
must be in python dictionary format and contain these paramters:
latitude, longitude, radius, search_term, result_type and
count. Please see the file "params.txt" for an example.

Example of params.txt:
{"latitude" : 37.7821, 
"longitude": -122.4093,
"radius" : 10,
"search_term" : "#SF+tech",
"result_type" : "mixed",
"count" : 15}

"""

#import ast, tweepy
import sys
import argparse
import geosearchclass


def get_parser():
    """ Creates a command line parser

    --doc -d 
    --help -h
    --filename -f
    --verbose -v
    --output -o
    --visualize -vis
    --default
    """

    parser = argparse.ArgumentParser(
        description='Perform a geo-located search.')

    parser.add_argument(
        '-d', '--doc', action='store_true',
        help='print module documentation and exit')
    parser.add_argument(
        '-f', '--filename',
        help='''specify a FILENAME to use as the parameter file. 
        If not specified, will use 'params.txt'.''')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='additionally print output to command line')
    parser.add_argument(
        '--default', action='store_true',
        help="""ignore parameter file and use default search
        terms from geosearchclass""")
    parser.add_argument(
        '-o', '--output',
        help='''specify an OUTPUT file to write to. 
        Default is output.txt''')
    parser.add_argument(
        '-j', '--json',
        help='''specify an OUTPUT JSON file to write to.''')
    parser.add_argument('-vis', '--visualize',
                        action='store_true', help='visualize using nlp tools')

    # automatically grabs arguments from sys.argv[]

    return parser


def main():

    parser = get_parser()
    args = parser.parse_args()

    if args.doc:
        print __doc__
        sys.exit()

    g = geosearchclass.GeoSearchClass()

    if args.filename:
        print 'Using parameters from ' + str(args.filename)
        # turn parameter file into dictionary
        g.set_params_from_file(args.filename)
    else:
        if args.default:
            print 'Using default search terms'
        else:
            print 'Using parameters from params.txt'
            g.set_params_from_file('params.txt')

    g.search()
    # print formatted results with extra info to terminal
    if args.verbose:
        g.print_search_results()

    if args.output:
        g.write_search_results(args.output)
    else:
        g.write_search_results()

    if args.json:
        g.json_search_results(args.json)

    if args.visualize:
        import vis_helper
        filtered_words = vis_helper.process(g.search_results)
        fdist = vis_helper.visualize_old(filtered_words)


if __name__ == '__main__':
    main()
