Ariel Kalinowski and Trevor Owens 5/14/2016

Install:

git, python 2.7.X, pip
On Windows: upgrade powershell
   (you may still have unicode problems when printing to command line)
Python packages required: tweepy, nltk, matplotlib
$ python -m pip install
$ pip install <packages>
Need some data, so we’ll use the nltk downloader
Run a python shell:
$ python
$ import nltk
$ nltk.download()
Less data:
1) under corpora -> highlight stopwords, click download
2) under corpora -> highlight treebank, click download
3) under all packages -> highlight punkt, click download
4) under models -> highlight averaged-perceptron-tagger, click download
OR if you don't mind much more data:
On main page, highlight book, click download and that should be it... 

This created a folder called “nltk_data” in your home folder which is
used by the program

Navigate to the folder where you want getweets to be
git clone https://github.com/owenst/geotweets.git
get consumerkeyandsecret and put that in the folder
cd into folder
run geotweets.py

Consumer Key and Secret:
The program requires a file in this folder called consumerkeyandsecret
secret (the longer one) on the second line. This should have 4 lines,
with the consumer key on the first line, the secret on the next and
then an access token on the 3rd and the access token secret on the
4th. You can get these by logging on to your twitter account in a web
browser and creating an app. These are used in the geosearchclass and
streamer modules.


About:
This library is composed of several tools for scraping
geolocated tweets and visualizing data gleaned from these tweets.

One tool, called 'geotweets' allows you to scrape and save geolocated
twitter data in batch form. You can optionally search within this set
for specific words or hash tags. See geotweets.py for details or from
command line run:

  $ python geotweets.py --help
  $ python geotweets.py --doc
  
USAGE :
  $ python geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]


Another tool, called 'real_time_vis' uses the previous tool to create
a word frequency distribution chart which can grow and change in near
real time as more tweets are grabbed. See real_time_vis.py for details
or from the command line run:

  $ python real_time_vis.py --help
  $ python real_time_vis.py --doc
  
USAGE :
  $ python real_time_vis.py [-h][-d][-f FILENAME][-n NUMBER]


Both files use a parameter file with geolocation and search
terms. See params.txt for an example.

You may have to adjust your PYTHONPATH variable to run the program
from the command line. Otherwise, using the python interpreter you can
run it.

Examples:

Grabbing geo-located tweets using paramter file params.txt (default),
print to command line and write to output.txt (default):

  $ python geotweets.py --verbose

Visualizing the data, 20 initial words, growing chart, using
params.txt (default):

  $ python real_time_vis.py -g -n 20








