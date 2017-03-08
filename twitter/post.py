"""Posts tweets to twitter account"""
import tweepy as tp

def post_tweet(msg, api):
    """adds tweet to api user"""

    try:
        api.update_status(msg)
    except tp.TweepError as terr:
        print(terr)

def reply(msg, tweeter_id, api):
    """reposts msg using id of tweeter"""

    try:
        api.update_status(msg, in_replay_to_status_id=tweeter_id)
    except tp.TweepError as terr:
        print(terr)
        