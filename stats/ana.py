"""Text analysis functions"""

from textstat import textstat as ts
import nltk


def init_stats():
    """initializes all stat fields to 0"""

    return {
        'flesch_ease': 0,
        'flesch_grade': 0,
        'dalechall': 0,
        'ari': 0,
        'colemanliau': 0,
        'lisear': 0,
        'smog': 0,
        'difcwords': 0,
        'sentences': 0,
        'lexiconcnt': 0,
        'avgsyllables': 0
        }

def get_msg_stats(msg):
    """creates new dict and loads it with textstat fields for given msg"""

    newstats = {}
    newstats['flesch_ease'] = ts.textstat.flesch_reading_ease(msg)
    newstats['flesch_grade'] = ts.textstat.flesch_kincaid_grade(msg)
    newstats['dalechall'] = ts.textstat.dale_chall_readability_score(msg)
    newstats['ari'] = ts.textstat.automated_readability_index(msg)
    newstats['colemanliau'] = ts.textstat.coleman_liau_index(msg)
    newstats['lisear'] = ts.textstat.linsear_write_formula(msg)
    newstats['smog'] = ts.textstat.smog_index(msg)
    newstats['difcwords'] = ts.textstat.difficult_words(msg)
    newstats['sentences'] = ts.textstat.sentence_count(msg)
    newstats['lexiconcnt'] = ts.textstat.lexicon_count(msg)
    newstats['avgsyllables'] = ts.textstat.avg_syllables_per_word(msg)
    newstats['stdreadability'] = ts.textstat.text_standard(msg)
    return newstats


def update_stat(newmsg):
    """Incomplete: Optimized way to update numerical stats by updating via single msg
        weight"""

    # new_val = ts.textstat.flesch_reading_ease(newmsg)
    # mean = self.stats['flesch_ease']
    # num_tweets = len(self.tweets)
    # new_mean = mean + ((new_val - mean)/num_tweets)
    # #TODO:update all stats