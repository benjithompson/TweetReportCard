"""holds the tweeter info"""

import sys
import time
from datetime import datetime
from collections import defaultdict
from pprint import pprint

import tweepy
from textstat import textstat as ts

from stats import ana
from twitter import config as c


def get_api():
    """returns tweepy api object"""

    try:
        auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
        auth.set_access_token(c.access_token, c.access_token_secret)
        api = tweepy.API(auth)
    except tweepy.TweepError as terror:
        print(terror)

    return api

def get_peer_dict(nameslist):
    """returns dict of users objects specified from namelist and returned from api"""

    tweeters = defaultdict(Tweeter)

    for name in nameslist:

        try:
            user = API.get_user(screen_name=name)
        except tweepy.TweepError:
            print(tweepy.TweepError)

        tweeters[user.screen_name] = Tweeter(user)

    return tweeters

def load_tweets(tweeters, cnt):
    """Loads tweets from the API and list of tweeters"""

    for name, tweeter in tweeters.items():
        print('loading tweets from ' + name + '...')
        if cnt <= 0:
            tweeter.load_all_tweets()
            print('{0} tweets loaded.'.format(tweeter.tweet_cnt))
        else:
            tweeter.get_tweet_dump(cnt)

def update_tweets(tweeters):
    """adds new tweets for each tweeter in list"""
    for name, tweeter in tweeters.items():
        tweeter.update_tweets()

def update_tweeters_stats(tweeters):
    """Updates the stats for tweeters in list"""

    for name, tweeter in tweeters.items():
        print('Updating {0} stats...'.format(name))
        tweeter.update_stats()
        print('Update complete.')

def print_tweeter_names(tweeters):
    """prints all tweeter names in dict"""

    for name, tweeter in tweeters.items():
        print(name + " ID: " + str(tweeter.user.id))

def print_tweeter_tweets(tweeters):
    """prints all tweets from tweeters in dict"""

    for name, tweeter in tweeters.items():
        print(name)
        tweeter.print_tweets()

def print_tweeter_stats(tweeters):
    """prints stats from all tweeters in dict"""

    for name, tweeter in tweeters.items():
        print(name)
        tweeter.print_stats()

def listener(target, tweeters, wait):
    """checks for new status updates per wait time"""

    print('Listening for new tweets. Target: {0}'.format(target))

    try:
        while True:
            # print('.', end='')
            sys.stdout.flush()
            for name, tweeter in tweeters.items():
                if tweeter.add_new_tweet_msg():
                    #get msg stats
                    msg_stats = ana.get_msg_stats(str(tweeter.get_last_tweet_msg()))

                    print('Msg Stats: ')
                    pprint(msg_stats)
                    tweeter.update_stats()

                    if tweeter.screen_name == target:
                        print(target + ' tweeted! Retweeting stats...')

                        s_id = tweeter.get_last_tweet().id
                        t_id = tweeter.user_id
                        name = tweeter.screen_name

                        # msg = '@{0} Overall Stats: {1}'.format(
                        #     name,
                        #     tweeter.stats['stdreadability'])
                        # print(msg)
                        # update_status(msg, t_id)

                        msg = '@{0} Tweet Stats: \nAvg Syllables: {1}\nFlesch Grade: {2}\nFlesch Ease: {3}\nColeman Liau: {4}\nARI: {5}'.format(
                            name,
                            msg_stats['avgsyllables'],
                            msg_stats['flesch_grade'],
                            msg_stats['flesch_ease'],
                            msg_stats['colemanliau'],
                            msg_stats['ari'])
                        print(msg)
                        update_status(msg, t_id)

                        time.sleep(5)
                        retweet(name, s_id)

                else:
                    pass
            time.sleep(wait)
    except KeyboardInterrupt as kbi:
        print(kbi)

def post_tweet(msg):
    """adds tweet to api owner"""

    try:
        API.update_status(msg)
    except tweepy.TweepError as terr:
        print(terr)

def update_status(msg, tweeter_id):
    """reposts msg using id of tweeter"""

    try:
        API.update_status(msg, in_replay_to_status_id=tweeter_id)
    except tweepy.TweepError as terr:
        print(terr)

def retweet(name, status_id):
    """retweet as status with msg"""

    try:
        API.update_status('https://twitter.com/{0}/status/{1}'.format(name, status_id), status_id)
    except tweepy.TweepError as terr:
        print(terr)

API = get_api()

class Tweeter:
    """Holds tweet text and stats as well as common user attributes for easy access"""

    def __init__(self, user):
        self.user = user
        self.name = user.name
        self.screen_name = user.screen_name
        self.user_id = str(user.id)
        self.tweets = []
        self.stats = ana.init_stats()
        self.tweet_cnt = 0
        self.last_status_id = self.get_updated_tweet_id()

    def update_tweets(self):
        """Adds newest tweets to list that haven't been added yet"""

        if len(self.tweets) == 0:
            self.load_all_tweets()
        else:
            new_tweets = API.user_timeline(screen_name=self.screen_name,
                                           since_id=self.last_status_id)

            print('{0} new tweets added from {1}'.format(len(new_tweets), self.screen_name))
            self.tweet_cnt += len(new_tweets)
            self.tweets.extend(new_tweets)

    def load_tweets(self, count=200):
        """receives tweet text from api and appends to objects tweets list"""

        try:
            tweet_dump = API.user_timeline(screen_name=self.screen_name,
                                           count=count)
        except tweepy.TweepError:
            print(tweepy.TweepError)

        for tweet in tweet_dump:
            self.tweets.append(tweet.text)

        self.tweet_cnt += len(self.tweets)

    def load_all_tweets(self):
        """Used from github user yanofsky. Loads all tweets from user"""

        alltweets = []

        new_tweets = API.user_timeline(screen_name=self.screen_name,
                                       count=200)

        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            # print("getting tweets before {0}".format(oldest))

            new_tweets = API.user_timeline(screen_name=self.screen_name,
                                           count=200,
                                           max_id=oldest)

            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1

            # print("...{0} tweets downloaded so far".format(len(alltweets)))
        self.tweets.extend(alltweets)
        self.tweet_cnt = len(self.tweets)

    def get_updated_tweet_id(self):
        """returns the last status id"""
        return str(API.user_timeline(id=self.user_id, count=1)[0].id)

    def get_last_tweet(self):
        """returns last tweet object"""
        return self.tweets[-1]

    def get_last_tweet_msg(self):
        """returns the last status msg"""
        return self.tweets[-1].text


    def add_new_tweet_msg(self):
        """appends msg to objects tweets list if has newer id"""

        new_id = self.get_updated_tweet_id()
        old_id = self.last_status_id

        if new_id > old_id:
            tweet = API.user_timeline(id=self.user_id, count=1)[0]
            self.tweets.append(tweet)
            self.tweet_cnt += 1
            self.last_status_id = new_id

            print('\nNew tweet: ' + tweet.created_at.strftime('%w:%b:%y %H.%M.%S'))
            print('Name: {0}\nMsg: {1}\nNumTweets: {2}'
                  .format(self.screen_name, tweet.text, self.tweet_cnt))
            return True
        else:
            return False

    def update_stats(self):
        """trivial way to update stats by concatinating all tweets from tweets list and
           reavaluating stats on entire str"""

        tweets_str = ''
        for tweet in self.tweets:
            tweets_str += tweet.text

        self.stats = ana.get_msg_stats(tweets_str)

    def print_stats(self):
        """prints stats dict using pprint"""

        pprint(self.stats)

    def print_tweets(self):
        """prints all tweets from self tweets list"""

        for tweet in self.tweets:
            print(tweet.text)
