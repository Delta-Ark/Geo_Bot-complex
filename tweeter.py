#!/usr/bin/python

import geosearchclass
import utils


def tweet(api, text, in_reply_to_status_id=None):
    """Send a tweet, possibly in response to another tweet

    REF: http://docs.tweepy.org/en/v3.5.0/api.html#API.update_status
    """
    if len(text) > 140:
        raise ValueError("Text is over 140 Characters. Can\'t tweet")
        return
    if in_reply_to_status_id:
        status = api.update_status(
            status=text, in_reply_to_status_id=in_reply_to_status_id)
    else:
        status = api.update_status(status=text)
    return status

        
def get_user_timeline(api, screen_name, count=20):
    """
    This returns a users timeline

    REF: http://docs.tweepy.org/en/v3.5.0/api.html#API.user_timeline
    """
    statuses = api.user_timeline(
        screen_name=screen_name, count=count)
    return statuses
    #  API.user_timeline(
    # [id/user_id/screen_name][, since_id][, max_id][, count][, page])
    

def main():
    (api, __) = utils.get_credentials('consumerkeyandsecret', False)
    g = geosearchclass.GeoSearchClass('params.txt', None, api)

    # Robotic Tweet:
    print g.tweet_text
    tweet_text = g.tweet_text + " @SaitoGroup"
    print tweet_text
    api = g.api
    status = tweet(api, tweet_text, 745399390219739137)
    utils.get_simplified_tweet(status)


    # Get user timeline:
    # screen_name = "SaitoGroup"
    # print "returning user timeline for {}".format(screen_name)
    # statuses = get_user_timeline(g, screen_name, 50)
    # for status in statuses:
    #     utils.get_simplified_tweet(status)
    #     print "\n NEXT TWEET \n"


if __name__ == '__main__':
    main()
