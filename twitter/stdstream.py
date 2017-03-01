import tweepy

class StreamListener(tweepy.StreamListener): 
    cnt = 0
    def on_status(self, tweet):
        print(str(StreamListener.cnt) + ':\n ' +tweet.text)
        StreamListener.cnt += 1

    def on_error(self, status_code):
        if status_code == 420:
            #disconnect, rate limiting
            return False
        else:
            print(status_code)

def run_stream(api, name):
    """starts a tweepy stream listening to name in tweeters dict"""
    user = api.get_user(screen_name=name)
    listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(follow=[str(user.id)])
    