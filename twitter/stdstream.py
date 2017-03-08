"""Streaming Class and methods"""

import tweepy
from . import twt

class StreamListener(tweepy.StreamListener):
    """Listens for stream updates and responds"""

    cnt = 0

    def on_status(self, tweet):
        """Handles new status updates from stream"""

        print(str(StreamListener.cnt) + ':\n ' +tweet.text)
        StreamListener.cnt += 1

    def on_error(self, status_code):
        """Handles errors on stream"""
        if status_code == 420:
            #disconnect, rate limiting
            return False
        else:
            print(status_code)

def print_stream(user):
    """prints stream for given name to stdout"""

    stream = get_stream()
    try:
        stream.filter(follow=[user.user_id], async=False)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        exit(1)

def get_stream():
    """starts a tweepy stream listening to name in tweeters dict"""

    listener = StreamListener()
    try:
        stream = tweepy.Stream(auth=twt.API.auth, listener=listener)
    except:
        print('Exception: Unable to create stream')
    return stream
