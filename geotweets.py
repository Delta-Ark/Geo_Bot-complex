#!/usr/bin/python
# geotweets
# Saito 2015

"""This program is for grabbing geo-located tweets using the Twitter API


USAGE:
  >> ./geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]

Print command line help:
>> ./geotweets.py --help   (or just -h)

Example: This uses parameter file 'params.txt', prints results to
command line and writes them to 'out.txt': 
>> ./geotweets.py --verbose --filename params.txt --output out.txt

The program requires a consumer key and secret stored in a file called
consumerkeyandsecret. See README for details.

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
    # Create command line argument parser
    parser = argparse.ArgumentParser(
        description='Perform a geo-located search.')
    # need to add arguments here
    #parser.add_argument('filename', metavar='filename', type=str, help='The parameter file name')
    parser.add_argument('-d', '--doc', action='store_true',
                        help='print module documentation and exit')
    parser.add_argument(
        '-f', '--filename', help='specify a FILENAME to use as the parameter file. If not specified, will use default arguments.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='additionally print output to command line')
    parser.add_argument(
        '-o', '--output', help='specify an OUTPUT file to write to. The default is output.txt')
    parser.add_argument('-vis', '--visualize',
                        action='store_true', help='visualize using nlp tools')

    # automatically grabs arguments from sys.argv[]
    
    return parser

def command_line_runner():
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
        print "Using default search values"

    g.search()
    # print formatted results with extra info to terminal
    if args.verbose:
        g.print_search_results()

    if args.output:
        g.write_search_results(args.output)
    else:
        g.write_search_results()

    if args.visualize:
        import vis_helper
        filtered_words = vis_helper.process(g.search_results)
        fdist = vis_helper.visualize_old(filtered_words)
    
    

def main():
    command_line_runner()
    

if __name__ == '__main__':
    main()
