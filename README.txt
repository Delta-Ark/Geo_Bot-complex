geotweets.py README file

Trevor Owens 11/8/2015

This program takes in a parameter file with geolocation and search
terms and returns tweets with those specifications.

The program requires a file called consumerkeyandsecret which contains
only a consumer key on the first line and consumer secret (the longer
one) on the second line. You can get this by creating an app under
your twitter account online. The program also relies on the tweepy python
package, which can be installed with pip. You may have to adjust your
PYTHONPATH variable to run the program from the command
line. Otherwise, using the python interpreter you can run it.

USAGE:
  >> ./geotweets.py [-h][-d][-v][-f FILENAME][-o OUTPUT]

Run it like this: 
  >> ./geotweets.py 
OR
  >> python geotweets.py -f params.txt
OR
  >> python geotweets.pyc -v -f params.txt -o output.txt
  


For more information see the docstring:
>> python import geotweets
>> python help(geotweets)





