geotweets.py README file

Ariel Kalinowski and Trevor Owens 11/8/2015

This program is made to search for and return tweets at a specific
location as determined by geocoordinates. You can optionally search
within this set for specific words or hash tags.

It takes in a parameter file with geolocation and search
terms and returns tweets with those specifications. See params.txt for
an example.

The program requires a file in this folder called consumerkeyandsecret
which contains only a consumer key on the first line and consumer
secret (the longer one) on the second line. You can get this by
creating an app under your twitter account online.

The program also relies on the tweepy python package, which can be
installed with pip. You may have to adjust your PYTHONPATH variable to
run the program from the command line. Otherwise, using the python
interpreter you can run it.

USAGE :
  >> ./geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]
OR using the python interpreter : 
  >> python geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]

Examples:

Default search:
  >> ./geotweets.py 

OR to grab tweets using a parameter file:
  >> python geotweets.py -f params.txt

OR to grab tweets using a parameter file, print to output and print a
verbose readout to the command line:
  >> python geotweets.pyc -v -f params.txt -o output.txt
  
For more information see the docstring for geotweets:
>> python import geotweets
>> python help(geotweets)

To initialize the geosearchclass with a parameter file and the
consumer key and secret file:
g = GeoSearchClass(params_filename, consumer_key_and_secret_filename)
and use:
g.search()
g.print_search_results()





