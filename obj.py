"""holds the tweeter info"""

from collections import defaultdict
from twitter import get

nameslist = ['realDonaldTrump', 'HillaryClinton', 'BarackObama', 'ChelseaClinton', 'BillClinton']

class Tweeter:

    def __init__(self, user):
        self.user = user
        self.handle = user.name
        self.tweets = defaultdict(Tweet)

        #userobj from API
        #tweetdump
        #


class Tweet:

    def __init__(self, msg):
        self.msg = msg
        self.stats = {}

    def update_stats(self, stats):
        #run stats on msg
        self.stats = stats

"""Helper function to send and retrieve data from dicts"""

def get_user_dict(api):
    tweeters = defaultdict(Tweeter)
    for name in nameslist:
        user = api.get_user(screen_name=name)
        print(user.name)
        tweeters[user.name] = Tweeter(user)
    return tweeters

def print_tweeter_names(tweeters):
    for name, tweeter in tweeters.items():
        print(name + " ID: " + str(tweeter.user.id))

