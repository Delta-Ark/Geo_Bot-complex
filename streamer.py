#!/usr/bin/python

import Queue
import json
import sys
import time

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

global stream


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


class ListenerQueue(StreamListener):
    """A StreamListener implementation for accessing Twitter Streaming API
    that writes to a queue object sent on initialization.

    Usage: myListener = ListenerQueue(queue)
    Stream(authorization, myListener)

    """

    def __init__(self, queue, filename):
        super(ListenerQueue, self).__init__()
        self.queue = queue
        self.json_file = open(filename, 'a')
        self.json_file.seek(0)
        self.json_file.truncate()

    def on_status(self, status):
        self.queue.put(status)
        # sj = status._json
        user = status.user.screen_name
        print user
        time = status.created_at.isoformat()
        print time
        text = status.text
        print text
        sj = [user, time, text]
        print sj
        j = json.dumps(sj, indent=1)
        self.json_file.write(j)
        return True

    def on_error(self, status):
        # error codes: https://dev.twitter.com/overview/api/response-codes
        print status
        if status == 420:
            print "Too many attempts made to contact the Twitter server"
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
    auth = get_creds()
    L = ListenerQueue(q, fn)
    stream = Stream(auth, L)
    if search_terms:
        stream.filter(locations=bounding_box, track=search_terms, async=True)
    else:
        stream.filter(locations=bounding_box, async=True)
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
    q = Queue.Queue()
    bounding_box = [-122.75, 36.8, -121.75, 37.8]
    global stream
    stream = start_stream(q, bounding_box)

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
        kill_stream(stream)
        sys.exit()
        pass
