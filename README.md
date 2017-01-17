Saito Group 1-11-2017

About:
----------------------------------------------------------------------
This library is composed of several tools for scraping
geolocated tweets and visualizing data gleaned from these tweets.

Geo-tag your tweets!
--------------------
We rely on geo-tagged tweets. Please allow your location to be seen
when tweeting, especially when using this application! You can modify
this by logging into your main twitter account and under "Security and
Privacy" check the box next to "Tweet location". THANKS!


Install:
----------------------------------------------------------------------
git, python 2.7.X, pip
Python packages required: tweepy, nltk, matplotlib, geopy, argparse,
curses, bs4 (beautiful soup), locale

On Windows: upgrade powershell
   (you may still have unicode problems when printing to command line)
   
```
python -m pip install
```

For each required package listed above run:
```
pip install <package>
```
Now we need some data, so we’ll use the nltk downloader
Run a python shell from the command line:
```
python
import nltk
nltk.download()
```
On main page, highlight book, click download and that should be it... 
These are the exact packages from nltk that are required in case you want less data:
1) under corpora -> highlight stopwords
2) under corpora -> highlight treebank
3) under all packages -> highlight punkt
4) under models -> highlight averaged-perceptron-tagger

This created a folder called “nltk_data” in your home folder which is
used by the program

Navigate to the folder where you want getweets to be
```
git clone https://github.com/saitogroup/geotweets.git
```
get consumerkeyandsecret (see below) and put that in the folder
cd into folder
run sample.py from the command line (see below)


Consumer Key and Secret:
----------------------------------------------------------------------
The program looks for a file in the geotweets folder called
consumerkeyandsecret This should have at least 2 lines, with the
consumer key on the first line, the secret (the longer one) on the
next and then (for streaming and posting) 2 more lines. An access
token on the 3rd and the access token secret on the 4th. You can get
these by going to https://apps.twitter.com in a web browser and
creating an app. Then hit the button to create access tokens. You may
have to set the app permissions to "read and write" if you want to use
this to send tweets on your behalf. After creating the app, copy the 4
alphanumeric keys into a blank file called "consumerkeyandsecret" as
described above and put this file in your "geotweets" folder.


TOOLS:
----------------------------------------------------------------------
sample:
-------
One tool, called 'sample' allows you to scrape and save up to
100 geolocated tweets in batch form. You can optionally search within
this set for specific words or hash tags and visualize the top word
frequency. See sample.py for details or from command line run:
```
python sample.py --help
python sample.py --doc
```  
USAGE :
```
python sample.py [-h][-d][-v][-f FILENAME][-o OUTPUT][-vis]
```


real time visualizer:
---------------------
Another tool, called 'real_time_vis' creates a word frequency
distribution chart which can grow and change in near real time as more
tweets are grabbed. If you use -s, you'll get streaming results, which
are currently being tweeted. Otherwise you will get batched quotes,
every 5 seconds using the REST API, which will return tweets that are
from the recent past. See real_time_vis.py for details or from the
command line run:

```
python real_time_vis.py --help
python real_time_vis.py --doc
```  
USAGE :
```
python real_time_vis.py [-h][-d][-f FILENAME][-n NUMBER][-s][-a ADDRESS]
```

Both files use a parameter file with geolocation and search
terms. See params.txt for an example.

You may have to adjust your PYTHONPATH variable to run the program
from the command line. Otherwise, using the python interpreter you can
run it.


scan_and_respond
----------------

This tool scans tweets and asks the user to verify them before sending
a tweet response. The relevant tweets are also saved to a JSON
file. This requires write access, which means the consumerkeyandsecret
file must contain all 4 lines.

```
scan_and_respond.py [-h] [-d] [-f FILENAME] [-a ADDRESS] [-o OUTPUT]
```

suggest_bot
-----------
This is a robotically assisted poetry engine. The user can create
poems using a large supplied word corpus or use their own. It can also
add words to the corpus from the twitter-sphere using the search
option. It can also parse those twitter messages into phrases using
natural language processing.

scraper
--------
Given a URL this will scrape a website and save the text to scraped_text.txt
```
python scraper.py -u http://www.cnn.com -o scraped_text.txt
```


HELP:
----------------------------------------------------------------------
All programs can be run from the command line (a.k.a. terminal in OS X).

By typing
```python <program_name> -h```
you will get help on the various command line tool options.
By typing
```python <program_name> -d```
you will get the programs documentation string


EXAMPLES:
----------------------------------------------------------------------
Grabbing geo-located tweets using paramter file params.txt (default),
print to command line and write to output.txt (default):
```
python sample.py --verbose
```
Visualizing the data, using params.txt (default):
```
python real_time_vis.py
```
Streaming real time data to create a word frequency chart using a local address:
```
python real_time_vis.py -a "175 5th Avenue NYC" -s
```

UTILITIES:
----------------------------------------------------------------------
These modules contain methods to assist the "tools" listed above:
```
tweeter.py: this allows you to tweet at people, programmatically
utils.py
geo_converter.py: this returns geocoordinates for a given address
geosearchclass.py: searches the REST API
streamer.py : creates a multithreaded twitter API streamer
editor.py : creates a command line editor
ngrams.py : creates a markov chain ngram word generator
```

write
-----
This program classifies tweets into phrase types and
produces a JSON array containing these, called phrases.json. It uses
parameters from params.txt. This requires quite a bit of processing
time, which can be reduced by using a lower "count".

The below two modules run unit tests:
```
test_real_time_vis
test_write
```







