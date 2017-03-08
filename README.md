## Tweet Report Card Bot

This is a Twitter Bot script that gathers tweets and runs text analysis to determine various features.

Written in Python 3.



### Installation

1. Run install_dep.sh to install all necessary python package dependencies.
2. Add the required fields in config.py to authenticate the [Twitter API connection](https://dev.twitter.com/overview/api)
3. (Optional) - Change the nameslist tweeters to desired targets. 
4. run `>python bot.py`
5. Follow prompts to use pickle as needed.
6. Wait...


### TextStat 

Tweets are loaded into a list and analysed using the python package [TextStat 0.3.1](https://pypi.python.org/pypi/textstat). All textstat stat values are averaged to determine a final score, which is used in the posted message. Due to textstat text grading relying on sentence length, twitter may receive an artificially lower score from the imposed character limit per tweet. This is mitigated by using a relative average tweet grade from other peer to the target tweeter.

### NLTK

Not implimented yet.


