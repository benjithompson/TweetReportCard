"""main bot script"""

"""TODO:
    1. Get twitter API auth
    2. get tweetdumps of users, specified in a config list. eg users = {'realDonaldTrump': userclass, 'Hillary': userclass, ...} defauldict
    3. Run textstat over all current tweetdumps to get each user's avgs and save to user object
    4. Run nltk over each user to get sentiment and save to user's object
    5. Once dumps and avgs are compiled, start stream to analyse new tweets from specified user(s)
    6. Repost tweet and stats
"""

import sys
from collections import defaultdict

from twitter import config
import twt

def run(args):

    twit_dict = twt.get_user_dict(config.nameslist)
    #twt.print_tweeter_names(twit_dict)

    #iterates over twit_dict and loads each object's tweets list
    twt.load_tweets(twit_dict)
    twt.update_tweeters_stats(twit_dict)
    twt.print_tweeter_stats(twit_dict)


if __name__ == '__main__':
    run(sys.argv)
