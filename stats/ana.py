"""Text analysis functions"""

import re

# import nltk
from textstat import textstat as ts


def init_stats():
    """initializes all stat fields to 0"""

    return {
        'flesch_ease': 0.0,  # [0-100] Lower more challenging. Wiki: Avg=49.13, Politicians = 46.93
        'flesch_grade': 0.0, # 1-20] Grade level
        'dalechall': 0.0,    # [0-9.9], grade level 0-15th(college)
        'ari': 0.0,          # [1-20], kindergarden-college
        'colemanliau': 0.0,  # [1-30] Grade level
        'linsear': 0.0,      # [1-20] Grade level
        'smog': 0.0,         # [1-240] Years of education needed to comprehend.
        'difcwords': 0.0,
        'sentences': 0.0,
        'lexiconcnt': 0.0,
        'avgsyllables': 0.0,
        'totalavg': 0.0
        }

def get_msg_stats(msg):
    """creates new dict and loads it with textstat fields for given msg"""

    #remove regex things...
    msg = clean_text(msg)
    s = {}
    s['flesch_ease'] = ts.textstat.flesch_reading_ease(msg)
    s['flesch_grade'] = ts.textstat.flesch_kincaid_grade(msg)
    s['dalechall'] = ts.textstat.dale_chall_readability_score(msg)
    s['ari'] = ts.textstat.automated_readability_index(msg)
    s['colemanliau'] = ts.textstat.coleman_liau_index(msg)
    s['linsear'] = ts.textstat.linsear_write_formula(msg)
    s['smog'] = ts.textstat.smog_index(msg)
    s['difcwords'] = ts.textstat.difficult_words(msg)
    s['sentences'] = ts.textstat.sentence_count(msg)
    s['lexiconcnt'] = ts.textstat.lexicon_count(msg)
    s['avgsyllables'] = ts.textstat.avg_syllables_per_word(msg)
    s['stdreadability'] = ts.textstat.text_standard(msg)
    s['totalavg'] = (((1-s['flesch_ease'])/100.0) +
                     (s['flesch_grade']/20.0) +
                     (s['dalechall']/10.0) +
                     (s['ari']/20.0) + (s['colemanliau']/30.0) +
                     (s['linsear']/20.0) +
                     (s['smog']/240.0))/7.0
    return s

def clean_text(text):
    """removes symbols"""

    text = re.sub('\B#\w\w+', ' ', text) # remove hashtags
    text = re.sub('\B@\w\w+', ' ', text) # remove tag
    text = re.sub('https?://.*[\r\n]*', ' ', text) #remove urls
    return text

# def update_stat(newmsg):
#     """Incomplete: Optimized way to update numerical stats by updating via single msg
#         weight"""

#     # new_val = ts.textstat.flesch_reading_ease(newmsg)
#     # mean = self.stats['flesch_ease']
#     # num_tweets = len(self.tweets)
#     # new_mean = mean + ((new_val - mean)/num_tweets)
