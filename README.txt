geotweets.py README file

Ariel Kalinowski and Trevor Owens 11/8/2015

This library is composed of several tools for scraping geolocated tweets and
visualizing data gleaned from these tweets.

One tool, called 'geotweets' allows you to scrape and save geolocated
twitter data in batch form. You can optionally search
within this set for specific words or hash tags. See geotweets.py for
details or from command line run:

  $ python geotweets.py --help
  $ python geotweets.py --doc
  
USAGE :
  $ python geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]


Another tool, called 'real_time_vis' uses the previous tool to create a
word frequency distribution chart which can grow and change in near real
time as more tweets are grabbed. See real_time_vis.py for details or
from the command line run:

  $ python real_time_vis.py --help
  $ python real_time_vis.py --doc
  
USAGE :
  $ python real_time_vis.py [-h][-d][-f FILENAME][-n NUMBER]


Both files use a parameter file with geolocation and search
terms. See params.txt for an example.

The program requires a file in this folder called consumerkeyandsecret
which contains only a consumer key on the first line and consumer
secret (the longer one) on the second line. You can get this by
creating an app under your twitter account online.

The program also relies on the tweepy python package, which can be
installed with pip. You may have to adjust your PYTHONPATH variable to
run the program from the command line. Otherwise, using the python
interpreter you can run it.

Examples:

Grabbing geo-located tweets using paramter file params.txt, print to
command line and write to output.txt:

  $ python geotweets.py -f params.txt --verbose

Visualizing the data, 20 initial words, growing chart:

  $ python real_time_vis.py -g -n 20








