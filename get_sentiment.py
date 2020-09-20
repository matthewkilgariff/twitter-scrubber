import datetime as dt
from keys import API_KEY
from keys import API_SECRET
from keys import ACCESS_TOKEN
from keys import ACCESS_TOKEN_SECRET
import nltk
import numpy as np
import pandas as pd 
from textblob import TextBlob
import tweepy
import twitter

'''
The Twitter API has several tiers for extracting data, etc.

The standard tier (free) only returns a select few tweets from a search,
so getting detailed searches with all tweets about a specific stock is impossible.
These limitations make backtesting impossible, since you can't pick specific dates
to pull tweets from.

If I wasn't a college student and had some disposable income, maybe I would pay the 
$149 a month for a premium tier.  Alas, the rest of this project is more of a proof
of concept that can be expanded to potentially an actual

I've also been having issues with the authenticating in the python-twitter wrapper.
So, I'm going to try the tweepy module instead... Hopefully, this works...
'''

# api = twitter.Api(consumer_key=API_KEY(), 
#                     consumer_secret=API_SECRET(), 
#                     access_token_key=ACCESS_TOKEN(), 
#                     access_token_secret=ACCESS_TOKEN_SECRET())

auth = tweepy.OAuthHandler(API_KEY(), API_SECRET())
auth.set_access_token(ACCESS_TOKEN(),ACCESS_TOKEN_SECRET())
api = tweepy.API(auth)

# Pull tweets given a ticker and start and end dates.
def pull_tweets(ticker, start, end, premium=False):
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    if not premium:
        return api.search(ticker)
        #return api.GetSearch(raw_query="q=${}".format(ticker))
    # This is what I would return if I had premium access
    else:
        return api.GetSearch(raw_query="q=${}%20since%3Astart%20until%3Aend")

# Pulls tweets, then returns a list of tuples corresponding with each tweets 
# polarity (ranges from -1 to 1) and objectivity (ranges from 0 to 1).
# This is done via TextBlob, an easy to use NLP library. I would also like to experiment
# with some of the NLP methods in the scikit-learn library at some point.
def get_sentiment(ticker, start, end):
    tweets = pull_tweets(ticker, start, end)
    sentiments = []
    for tweet in tweets:
        sent = TextBlob(tweet.text)
        sentiments.append((sent.polarity, sent.subjectivity))
    return sentiments

# 
def sentiment_metadata(ticker, start, end):
    sentiments = get_sentiment(ticker, start, end)
    average_sentiment = 0
    average_subjectivity = 0
    for tweet in sentiments:
        average_sentiment += tweet[0]
        average_subjectivity += tweet[1]
    length = len(sentiments)
    average_sentiment /= length
    average_subjectivity /= length
    return average_sentiment, average_subjectivity, length

start = dt.datetime(2020,8,1)
end = dt.datetime(2020,8,2)

sentiment = sentiment_metadata("QQQ", start, end)
print(sentiment)