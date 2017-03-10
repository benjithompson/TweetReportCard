"""main bot script"""

from twitter import config
from twitter import twt
from utils import io

"""TODO:
    - Handle excepts - IN PROGRESS
    - Start stream to analyse new tweets from specified user(s) -IN PROGRESS
    - Run nltk over each user - NOT STARTED
    - Run textstat, get user's avgs - NOT STARTED
    - Repost tweet and stats - NOT STARTED
    - sys.argv command line args - NOT STARTED

      COMPLETE
X   - Get twitter API auth - DONE
X   - get tweetdumps of users, specified in a config list. -DONE
X   - pickle - DONE
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
    else:
        print('Downloading tweet dump:')
        tweeters = twt.get_peer_dict(config.nameslist)
        # twt.print_tweeter_names(tweeters)
        twt.load_tweets(tweeters, 0)
        twt.update_tweeters_stats(tweeters)
    twt.print_tweeter_stats(tweeters)

    # Monitors new tweets from nameslist
    twt.listener(config.target, tweeters, config.wait)

    filename = input('save pickle file: ')
    io.save_data_to_file(tweeters, filename)

if __name__ == '__main__':
    run()
