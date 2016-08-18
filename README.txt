Ariel Kalinowski and Trevor Owens 5/14/2016

Install:

git, python 2.7.X, pip
Python packages required: tweepy, nltk, matplotlib, geopy, argparse, json

On Windows: upgrade powershell
   (you may still have unicode problems when printing to command line)
$ python -m pip install
For each required package listed above run:
$ pip install <package>

Now we need some data, so we’ll use the nltk downloader
Run a python shell from the command line:
$ python
$ import nltk
$ nltk.download()
On main page, highlight book, click download and that should be it... 
These are the exact packages from nltk that are required in case you want less data:
1) under corpora -> highlight stopwords
2) under corpora -> highlight treebank
3) under all packages -> highlight punkt
4) under models -> highlight averaged-perceptron-tagger

This created a folder called “nltk_data” in your home folder which is
used by the program

Navigate to the folder where you want getweets to be
git clone https://github.com/owenst/geotweets.git
get consumerkeyandsecret (see below) and put that in the folder
cd into folder
run geotweets.py

Consumer Key and Secret:

The program looks for a file in the geotweets folder called
consumerkeyandsecret This should have 4 lines, with the consumer key
on the first line, the secret (the longer one) on the next and then an
access token on the 3rd and the access token secret on the 4th. You
can get these by going to https://apps.twitter.com in a web browser and
creating an app. Then hit the button to create access tokens. You may
have to set the app permissions to "read and write" if you want to use
this to send tweets on your behalf. After creating the app, copy the 4
alphanumeric keys into a blank file called "consumerkeyandsecret" as
described above and put this file in your "geotweets" folder.


About:
This library is composed of several tools for scraping
geolocated tweets and visualizing data gleaned from these tweets.

We rely on geo-located tweets. Please allow your location to be seen
when tweeting, especially when using this application! You can modify
this by logging into your main twitter account and under "Security and
Privacy" check the box next to "Tweet location". THANKS!


geotweets:
One tool, called 'geotweets' allows you to scrape and save geolocated
twitter data in batch form. You can optionally search within this set
for specific words or hash tags. See geotweets.py for details or from
command line run:

  $ python geotweets.py --help
  $ python geotweets.py --doc
  
USAGE :
  $ python geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]


real time visualizer:
Another tool, called 'real_time_vis' uses the previous tool to create
a word frequency distribution chart which can grow and change in near
real time as more tweets are grabbed. See real_time_vis.py for details
or from the command line run:

  $ python real_time_vis.py --help
  $ python real_time_vis.py --doc
  
USAGE :
  $ python real_time_vis.py [-h][-d][-f FILENAME][-n NUMBER][-s][-a ADDRESS]


Both files use a parameter file with geolocation and search
terms. See params.txt for an example.

You may have to adjust your PYTHONPATH variable to run the program
from the command line. Otherwise, using the python interpreter you can
run it.

Examples:

Grabbing geo-located tweets using paramter file params.txt (default),
print to command line and write to output.txt (default):

  $ python geotweets.py --verbose

Visualizing the data, 20 initial words, using
params.txt (default):

  $ python real_time_vis.py -n 20

Streaming real time data word frequency chart using a local address:

  $ python real_time_vis.py -a "175 5th Avenue NYC" -s








