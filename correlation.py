# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 19:19:16 2020

@author: JLuca
"""
from binance.client import Client 

import pandas as pd

# Stock market data
SP500 = pd.read_csv("SP500.csv")
SP500 = SP500[['Date','Close']]
SP500['Date'] = pd.to_datetime(SP500['Date'])

# CRYPTO DATA

api_key = r'C:\Users\JLuca\Documents\repos\TradingBot/API_key.txt'
api_secret = r'C:\Users\JLuca\Documents\repos\TradingBot/API_secret.txt'

start_date = "26 Dec, 2019"
end_date = "24 Dec, 2020"
symbol="BCHUSDT"

# Initialize client
client = Client(api_key, api_secret)

# Get Data
prices = client.get_historical_klines(symbol,Client.KLINE_INTERVAL_1DAY,start_date,end_date)
prices = pd.DataFrame(prices)

column_names = ['Open time', 'Open', 'High', 'Low',
                             'Close', 'Volume', 'Close time',
                             'Quote asset volume',' Number of trades',
                             'Taker buy base asset volume', 
                             'Taker buy qoute asset volume', 'Ignore']
    
prices.columns = column_names

coin = prices[['Open time', 'Close']]
coin['Open time'] = pd.to_datetime(prices['Open time'], unit='ms')

# Create date-matched DataFrame with prices
new_df = pd.DataFrame([])
new_df['SP500'] = []
new_df['coin'] = []

ind = 0
for A in SP500['Date']:
    SP500_price = float(SP500['Close'][ind])    
    for B in coin['Open time']:
        coin_price = float(coin['Close'][ind])
        if A == B:
            new_df.loc[ind] = [SP500_price] + [coin_price]
            ind += 1

# Get correlation
corr = new_df.corr(method='pearson')

print(corr)

new_df.plot(logy=True)