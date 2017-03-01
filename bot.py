"""main bot script"""


import tweepy

import twt
from twitter import config
from twitter import stdstream as ss

"""TODO:
    1. Get twitter API auth
    2. get tweetdumps of users, specified in a config list.
        eg users = {'realDonaldTrump': userclass, 'Hillary': userclass, ...} defauldict
    3. Run textstat over all current tweetdumps to get each user's avgs and save to user object
    4. Run nltk over each user to get sentiment and save to user's object
    5. Once dumps and avgs are compiled, start stream to analyse new tweets from specified user(s)
    6. Repost tweet and stats
    7. Handle excepts
"""

def run():
    """Main bot runner to start tweet agrigation and streaming analysis"""
    api = twt.get_api()
    tweeters = twt.get_user_dict(config.nameslist, api)
    # twt.print_tweeter_names(TWEETERS)
    # twt.load_tweets(api, TWEETERS)
    # twt.update_tweeters_stats(TWEETERS)
    # #twt.print_tweeter_stats(TWEETERS)
    ss.run_stream(api, 'realDonaldTrump')



if __name__ == '__main__':
    run()
