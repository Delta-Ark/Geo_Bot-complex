#!/usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#import tweepy
import json
import time
import Queue
import threading


def get_creds(keys_file="consumerkeyandsecret"):
    '''This function gives stream access to the API

    It requires that your consumerkeyandsecret have 4 lines, with the
    consumer key on the first line, the secret on the next and then an
    access token on the 3rd and the access token secret on the
    4th. You can get these by logging on to your twitter account and
    creating an app.

    USAGE: auth = get_creds(keys_file)

    '''
    with open(keys_file, 'rU') as myfile:
        auth_data = [line.strip() for line in myfile]
        CONSUMER_KEY = auth_data[0]
        CONSUMER_SECRET = auth_data[1]
        ACCESS_TOKEN = auth_data[2]
        ACCESS_TOKEN_SECRET = auth_data[3]
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth

    # class Listener(StreamListener):
    #     """A StreamListener implementation for accessing Twitter Streaming API

    #     Always call with the "with" statement.

    #     """

    #     def __init__(self,filename):
    #         super(Listener,self).__init__()
    #         self.json_file = open(filename,'a')

    #     def __enter__(self):
    #         return self

    #     def __exit__(self, exc_type, exc_value, traceback):
    #         self.json_file.close()

    #     def on_status(self, status):
    #         #print data
    #         #print u"Tweet Message : {}\n\n".format(status.text)
    #         print type(status)
    #         sj = status._json
    #         j = json.dumps(sj)
    #         #j = json.dumps(status, indent=1)
    #         self.json_file.write(j)
    #         return True

    #     def on_error(self, status):
    #         # error codes: https://dev.twitter.com/overview/api/response-codes
    #         print status
    #         if status_code == 420:
    #             return False #returning False in on_data disconnects the stream
    # with Listener('tweets.json') as L:
    #     stream = Stream(auth, L)
    #     stream.filter(locations=[-122.75,36.8,-121.75,37.8])


class ListenerJSON(StreamListener):
    """A StreamListener implementation for accessing Twitter Streaming API that writes to a JSON file
    """

    def __init__(self, filename):
        super(ListenerJSON, self).__init__()
        self.json_file = open(filename, 'a')

    def on_status(self, status):
        # print data
        # print u"Tweet Message : {}\n\n".format(status.text)
        print type(status)
        sj = status._json
        j = json.dumps(sj, indent=1)
        self.json_file.write(j)
        return True

    def on_error(self, status):
        # error codes: https://dev.twitter.com/overview/api/response-codes
        print status
        if status_code == 420:
            return False  # returning False in on_data disconnects the stream

    def on_disconnect():
        super(ListenerJSON, self).on_disconnect()
        print "made it to disconnector"
        self.json_file.close()


class ListenerQueue(StreamListener):
    """A StreamListener implementation for accessing Twitter Streaming API that writes to a queue object sent on initialization.

    Usage: myListener = ListenerQueue(queue)
    Stream(authorization, myListener)
    """

    def __init__(self, queue):
        super(ListenerQueue, self).__init__()
        self.queue = queue

    def on_status(self, status):
        self.queue.put(status)
        return True

    def on_error(self, status):
        # error codes: https://dev.twitter.com/overview/api/response-codes
        print status
        if status_code == 420:
            return False  # returning False in on_data disconnects the stream


def stream_to_json_file(fn='tweets.json'):
    auth = get_creds()
    L = ListenerJSON(fn)
    stream = Stream(auth, L)
    stream.filter(locations=[-122.75, 36.8, -121.75, 37.8], async=True)
    print "waiting 5s"
    time.sleep(5)
    print "terminating"
    stream.disconnect()
    L.json_file.close()


def get_tweets_from_q(queue):
    while True:
        status = queue.get()
        print u"Tweet Message : {}\n\n".format(status.text)
        queue.task_done()


def start_stream(q, q_handler_function):
    auth = get_creds()

    L = ListenerQueue(q)
    stream = Stream(auth, L)
    stream.filter(locations=[-122.75, 36.8, -121.75, 37.8], async=True)
#    t = threading.Thread(target=get_tweets_from_q(q))
    t = threading.Thread(target=q_handler_function(q))
    t.daemon = True
    t.start()
    print "waiting 5s"
    time.sleep(5)
    print "terminating"
    stream.disconnect()
    t.join()


if __name__ == '__main__':

    #    stream_to_json_file()
    q = Queue.Queue()
    start_stream(q, get_tweets_from_q)

    # now read in the files

    # https://dev.twitter.com/streaming/overview/request-parameters
