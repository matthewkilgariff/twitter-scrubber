# twitter-scrubber

Project intended to use sentiment of certain stocks on twitter to create
buy/sell signals.

Design:
1. Build twitter scrubber
2. Analyze sentiment of tweets
3. Find correlation between changes in sentiment on twitter and price movements
4. Send alerts to buy/sell

This project was the culmination of me learning how to use some of the data science and machine learning tools with Python.

There were many issues I ran into, mostly having to deal with lack of available data.  As mentioned in comments throughout
the code, the Twitter API has many tiers.  Without paying hundreds of dollars a month, I experienced issues with rate limiting
and lack of Twitter's advanced search features.

This project was originally inteded to pull as much data from Twitter and be able to test as many stock tickers as possible in 
any time frame.  Sadly, I was only able to pull a small selection of popular tweets published the same day as my requests to the API.

So, the project evolved to a proof-of-concept to use sentiment analysis to correlate with stock movements.  In the future, this could be
expanded to help model virtually any stock, currency, cryptocurrency, or other asset.  For now, it is just a snapshot of one week of the
components of the S&P 100 index.
