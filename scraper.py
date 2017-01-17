#!/usr/bin/python
# scraper.py
# Saito 2017

import argparse
import sys
import urllib

from bs4 import BeautifulSoup

import utils


def scrape(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    [x.extract() for x in soup.find_all('script')]
    text = soup.get_text(" ", strip=True)
    # ftext = text.split(" ")
    return text


def scrape_and_save_to_file(url, filename="scraped_text.txt"):
    text = scrape(url)
    utils.save_file(filename, text)
    return text


def get_parser():
    """ Creates a command line parser

    --doc -d
    --help -h
    --url -u
    --output -o

    This automatically grabs arguments from sys.argv[]
    """

    parser = argparse.ArgumentParser(
        description='Scrape a website.')

    parser.add_argument(
        '-d', '--doc', action='store_true',
        help='print module documentation and exit')
    parser.add_argument(
        '-u', '--url',
        help='''specify a url to scrape. Use the full name like
        http://www.cnn.com''')
    parser.add_argument(
        '-o', '--output',
        help='''specify an OUTPUT file to write to.
        Default is scraped_text.txt''')

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.doc:
        print __doc__
        sys.exit()

    if args.url:
        url = args.url
    else:
        url = "http://chrisnovello.com/teaching/risd/computer-utopias/"

    if args.output:
        print '\nwriting file to ' + str(args.output)
        output_file = args.output
    else:
        print "\nwriting to scraped_text.txt"
        output_file = "scraped_text.txt"
    text = scrape_and_save_to_file(url, output_file)

    # # Example
    # url = "http://chrisnovello.com/teaching/risd/computer-utopias/"
    # # text = scrape(url)
    # text = scrape_and_save_to_file(url)
    print text
    

if __name__ == '__main__':
    main()

