import bs4 as bs
import datetime as dt 
import matplotlib.pyplot as plt 
from matplotlib import style
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import os
import os.path
from os import path
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

import yfinance as yf

yf.pdr_override()

style.use('ggplot')

def save_sp500_tickers():
    #grab source code from wikipedia
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    #creating bs object
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('\n','')
        #wikipedia uses BRK.B when yahoo uses BRK-B so yur
        mapping = str.maketrans('.','-')
        ticker = ticker.translate(mapping)
        tickers.append(ticker)
    with open('sp500tickers.pickle','wb') as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers

# Runs the above method if reload_sp500=True, as you may not have the tickers saved already
# or if there have been changes to the S&P500.
# Start is a datetime variable for you first date to pull from.
# end is a datetime variable for your last date.
#
# This might take a few minutes to run.
def get_data_from_yahoo(start, end, reload_sp500=False,):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500tickers.pickle','rb') as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    # gets data for all 500 companies. Might want to do tickers[:100] 
    # or something if you don't need all 500 companies
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.get_data_yahoo(ticker, start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def get_one_stock(start, end, ticker):
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    print(ticker)
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
        df = web.get_data_yahoo(ticker, start, end)
        df.to_csv('stock_dfs/{}.csv'.format(ticker))
    else:
        print('Already have {}'.format(ticker))

# Creates a csv combining the OHLC of all the tickers in the S&p
def compile_data():
    with open('sp500tickers.pickle','rb') as f:
        tickers = pickle.load(f)
    
    print(type(tickers))
    main_df = pd.DataFrame()

    ticks = enumerate(tickers)
    for c, ticker in enumerate(tickers):
        if not path.exists("stock_dfs/{}.csv".format(ticker)):
            continue

    # enumerate() returns 0,A then 1,B 2,C etc so you can see where youre at 
    for count,ticker in enumerate(tickers):
        if not path.exists("stock_dfs/{}.csv".format(ticker)):
            continue
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        
        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        #Drop other columns w/ Adj Close w/ axis 1
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            #lookup in the panda documentation on why to use outer
            main_df = main_df.join(df, how='outer')
        
        #just to see where we at
        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

start = dt.datetime(2020,1,1)
end = dt.datetime(2020,7,31)

get_data_from_yahoo(start, end, True)
compile_data()