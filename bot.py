"""main bot script"""

import twt, os
from utils import io
from twitter import stdstream as ss
from twitter import config


"""TODO:
X. Get twitter API auth - DONE
X. get tweetdumps of users, specified in a config list. -DONE
   eg users = {'realDonaldTrump': userclass, 'Hillary': userclass, ...} defauldict -DONE
    3. Run textstat over all current tweetdumps to get each user's avgs and save to user object -PASSING
    4. Run nltk over each user to get sentiment and save to user's object - NOT STARTED
    5. Once dumps and avgs are compiled, start stream to analyse new tweets from specified user(s) -IN PROGRESS
    6. Repost tweet and stats - NOT STARTED
    7. Handle excepts - IN PROGRESS
    8. sys.argv command line args - NOT STARTED
    9. pickle - IN PROGRESS
"""

def run():
    """Main bot runner to start tweet agrigation and streaming analysis"""

    #open pickle if exists
    filename = input('Load pickle file: ')
    path = io.get_path(filename)
    print('loading pickle from {0}'.format(path))
    tweeters = io.load_pickle(path)
    if tweeters is not None:
        twt.update_tweets(tweeters)
        twt.print_tweeter_tweets(tweeters)
    else:
        print('Downloading tweet dump for:')
        tweeters = twt.get_peer_dict(config.nameslist)
        twt.print_tweeter_names(tweeters)
        twt.load_tweets(tweeters, 0)
        twt.update_tweeters_stats(tweeters)

    twt.listener(tweeters, 5*60)
    filename = input('save pickle file: ')
    io.save_data_to_file(tweeters, filename)

if __name__ == '__main__':
    run()
