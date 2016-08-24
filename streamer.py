#!/usr/bin/python
""" This is a utility that allows tweets to be read off in real time

To stop, use a KeyboardInterrupt like CTRL + C"""


import Queue
import json
import sys
import threading
import time

import tweepy

import utils


global stream  # so that CTRL + C kills stream


class ListenerQueue(tweepy.streaming.StreamListener):
    """A StreamListener implementation for accessing Twitter Streaming API
    that writes to a queue object sent on initialization.

    Usage: myListener = ListenerQueue(queue)
    Stream(authorization, myListener)

    """

    def __init__(self, queue, filename, search_terms):
        super(ListenerQueue, self).__init__()
        self.queue = queue
        self.search_terms = search_terms
        self.json_file = open(filename, 'a')
        self.json_file.seek(0)
        self.json_file.truncate()

    def has_all_search_terms(self, text):
        for term in self.search_terms:
            if text.find(term) > -1:
                continue
            else:
                return False
        return True
            
    def on_status(self, status):
        text = status.text
        if self.search_terms:
            if not self.has_all_search_terms(text):
                return True
    
        self.queue.put(status)
        # sj = status._json
        sj = utils.get_simplified_tweet(status)
        # filter_lev = status.filter_level
        # print filter_lev
        j = json.dumps(sj, indent=1)
        self.json_file.write(j)
        return True

    def on_error(self, status):
        # error codes: https://dev.twitter.com/overview/api/response-codes
        print status
        if status == 420:
            print "Too many attempts made to contact the Twitter server"
            print "Wait awhile to use the tool again"
            return False  # returning False in on_data disconnects the stream

    def on_disconnect(self):
        super(ListenerQueue, self).on_disconnect()
        print "stream disconnected"
        self.json_file.close()
        if self.json_file.closed:
            print "json file closed successfully"


# def stream_to_json_file(fn='tweets.json'):
#     auth = get_creds()
#     L = ListenerJSON(fn)
#     stream = Stream(auth, L)
#     stream.filter(locations=[-122.75, 36.8, -121.75, 37.8], async=True)
#     # can find terms: by adding track=['python']
#     print "waiting 15s"
#     time.sleep(15)
#     print "terminating"
#     stream.disconnect()
#     L.json_file.close()


def get_tweets_from_q(queue):
    while True:
        status = queue.get(True, 5)
        print u"Tweet Message : {}\n\n".format(status.text)
        queue.task_done()


def start_stream(q, bounding_box, fn='tweets.json', search_terms=None):
    '''Takes in a Queue object, a bounding_box of [lon, lat, lon, lat] for
    SW and NE corners, a filename and a search term list. Examples in:
    bounding_box = geo_converter.get_bounding_box_from(g)
    search_terms = geo_converter.get_search_terms_from(g)
    '''
    global stream
    (__, auth) = utils.get_credentials("consumerkeyandsecret", False)
    L = ListenerQueue(q, fn, search_terms)
    stream = tweepy.Stream(auth, L)
    stream.filter(locations=bounding_box, filter_level='none', async=True)
    # if search_terms:
    #     # OR semantics:
    #     stream.filter(locations=bounding_box, track=search_terms, async=True)
    # else:
    #     stream.filter(locations=bounding_box, async=True)
    return stream


def kill_stream(stream):
    if stream:
        print "attempting to disconnect stream from kill_stream"
        stream.disconnect()
        print "closing file in 1 second..."
        time.sleep(1)
        stream.listener.json_file.close()
    else:
        print "stream not set"

    
def main():
    print __doc__
    
    q = Queue.Queue()
    bounding_box = [-122.75, 36.8, -121.75, 37.8]
    global stream
    stream = start_stream(q, bounding_box)
    
    # t = threading.Thread(target=start_stream, args=(q, bounding_box))
    # t.daemon = True
    # t.start()
    # t.join()
    # print "waiting 15s"
    # time.sleep(15)
    # kill_stream(stream)

    # stream_to_json_file()

    # get_tweets_from_q(q)
    # now read in the files
    # https://dev.twitter.com/streaming/overview/request-parameters
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Main function interrupted"
        if "stream" in globals():
            print "trying to kill stream"
            kill_stream(stream)
        sys.exit()




# class ListenerJSON(StreamListener):
#     """A StreamListener implementation for accessing Twitter Streaming API
#     that writes to a JSON file

#     """

#     def __init__(self, filename):
#         super(ListenerJSON, self).__init__()
#         self.json_file = open(filename, 'a')

#     def on_status(self, status):
#         # print data
#         # print u"Tweet Message : {}\n\n".format(status.text)
#         print type(status)
#         sj = status._json
#         j = json.dumps(sj, indent=1)
#         self.json_file.write(j)
#         return True

#     def on_error(self, status):
#         # error codes: https://dev.twitter.com/overview/api/response-codes
#         print status
#         if status == 420:
#             return False  # returning False in on_data disconnects the stream

#     def on_disconnect(self):
#         super(ListenerJSON, self).on_disconnect()
#         print "made it to disconnector"
#         self.json_file.close()
