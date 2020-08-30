from datetime import datetime as dt
from get_sentiment import pull_tweets
import glob
from keys import API_KEY
from keys import API_SECRET
from keys import ACCESS_TOKEN
from keys import ACCESS_TOKEN_SECRET
import nltk
import numpy as np
import os
import os.path
from os import path
import pandas as pd 
import pickle
from stock_price import save_sp500_tickers
from textblob import TextBlob
import time
import twitter


'''
Scraping the free twitter api to hopefully get as much data as possible
'''

def scrape(ticker):
    # Just using datetime.now() as the start and end dates, as this is an unused parameter
    # if using the standard twitter api.
    tweets = pull_tweets(ticker, dt.now(), dt.now())
    tweet_dict = []
    for tweet in tweets:
        tweet_dict.append([tweet.created_at, tweet.text])
    df = pd.DataFrame(tweet_dict, columns=["Creation","Text"])
    if not os.path.exists("tweets"):
        os.makedirs("tweets")
    df.set_index("Creation",inplace=True)
    df.to_csv("tweets/{}-{}.csv".format(ticker, dt.now().date()))

def combine_tweets(ticker):
    # read what we have saved
    # add new tweets
    # resave
    if not os.path.exists("tweets"):
        sys.exit("No data saved.")
    if not os.path.exists("tweets/{}-{}.csv".format(ticker, dt.now().date())):
        sys.exit("Today's data not saved.")
    if os.path.exists("tweets/{}-combined.csv".format(ticker)):
        df_old = pd.read_csv("tweets/{}-combined.csv".format(ticker))
        df_new = pd.read_csv("tweets/{}-{}.csv".format(ticker, dt.now().date()))
        df_old = pd.concat([df_old, df_new], ignore_index=True)
        for filename in glob.glob("tweets/{}*".format(ticker)):
            os.remove(filename)
        df_old.set_index("Creation", inplace=True)
        df_old.to_csv("tweets/{}-combined.csv".format(ticker))
    else:
        os.rename("tweets/{}-{}.csv".format(ticker, dt.now().date()),"tweets/{}-combined.csv".format(ticker))
    

# Let's get some data
def get_init_data():
    if not os.path.exists("sp500tickers.pickle"):
        save_sp500_tickers()
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)
    for ticker in tickers:
        if os.path.exists("tweets/{}-{}.csv".format(ticker, dt.now().date())):
            print("Already scraped: ", ticker)
            continue
        scrape(ticker)
        print("Scraped: ", ticker)

def get_combined():
    if not os.path.exists("sp500tickers.pickle"):
        save_sp500_tickers()
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)
    for ticker in tickers:
        if os.path.exists("tweets/{}-combined.csv".format(ticker)):
            print("Already scraped: ", ticker)
            continue
        combine_tweets(ticker)
        print("Combined: ", ticker)

def run_everyday():
    if not os.path.exists("sp500tickers.pickle"):
        save_sp500_tickers()
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)
    for ticker in tickers:
        schedule.every().day.at("20:30").do(get_combined(ticker))
    while 1:
        schedule.run_pending()
        time.sleep(1)

'''
Testing
'''
scrape("TSLA")
combine_tweets("TSLA")
get_init_data()
get_combined()