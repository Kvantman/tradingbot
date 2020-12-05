# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:31:39 2020

@author: JLuca
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quantstats as qs
import statistics
from binance.client import Client
import datetime

# Load api key and secret
with open(r'C:\Users\JLuca\Documents\repos\Trading Bot\API_key.txt') as f:
    api_key = f.read()
with open(r'C:\Users\JLuca\Documents\repos\Trading Bot\API_secret.txt') as f:
    api_secret = f.read()
 
# initialize client
client = Client(api_key, api_secret)

# Set symbol
symbol = "BTCUSDT"

# Shorting?
shorting=False

# Data time intervals
start_date = "1 Jan, 2018"
end_date = "1 Jan, 2021"


# fetch data
data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date, end_date)

# create prices df
df_prices = pd.DataFrame(data)
df_prices.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',' Number of trades', 'Taker buy base asset volume', 'Taker buy qoute asset volume', 'Ignore']

price_column = "Close"

period_fast=[2, 4, 6, 8]
period_slow=[20, 25, 30, 40]
periods = set(period_fast+period_slow)

# Fix datetime colmn
df_prices['Open time'] = pd.to_datetime(df_prices['Open time'], unit='ms')
df_prices['Close time'] = pd.to_datetime(df_prices['Close time'], unit='ms')

# SMA
for period in periods:
    df_prices["SMA"+str(period)] = df_prices[price_column].rolling(period).mean()
    
    
# Remove first data rows for SMA to work  
start = max(periods)
df_prices = df_prices[start:]


# Create signals dataframe
df_signals = pd.DataFrame()

for a in period_fast:
    for b in period_slow:
        if a!=b and a<b:
            sma_name=f"SMA({a},{b})"
            df_signals[sma_name] = df_prices[f"SMA{a}"] > df_prices[f"SMA{b}"]
        
        
# Create strategy evaluation datafram
df_performance = pd.DataFrame(columns=df_signals.columns)

now = start + 1

buy_count = 0
sell_count = 0

long_count= 0
short_count = 0

if symbol == "BNBUSDT":
    trading_fee = 0.075/100
else:
    trading_fee = 0.1/100
    
taker_fee = 0.04/100
spread_percentage = 0.05/100

start_val = 100


# Calculate Performance DataFrame
for col in df_performance.columns:
    myMonies = start_val

    for row in range(now,len(df_signals)):
        
        df_performance.at[row-1, sma_name] = myMonies
        
        sma_name = col
        oldSignal = df_signals.at[row-1, sma_name]
        newSignal = df_signals.at[row, sma_name]       
 
        oldPrice = df_prices.at[row-1, price_column]
        newPrice = df_prices.at[row, price_column]
        # Win will be for price of tomorrow compared to today
        futurePrice = df_prices.at[row+1, price_column]
        delta  = float(futurePrice) / float(newPrice)    
        
        if not shorting: 

            # Crossing UP --> Buy
            if oldSignal == False and newSignal == True:
                 myMonies = (1-trading_fee-spread_percentage)*(myMonies*delta)
                 buy_count += 1
                 
            # Continued UPTREND --> remain invested, do nothing
            elif oldSignal == True and newSignal == True:
                 myMonies = myMonies*delta                 
            
            # Crossing DOWN --> Sell
            elif oldSignal == True and newSignal == False:
                 myMonies = (1-trading_fee-spread_percentage)*myMonies
                 sell_count += 1   
                 
            # Continued DOWNTREND --> remain out, do nothing
            elif oldSignal == False and newSignal == False:
                pass

    
        if shorting:
            
            # Continued UPTREND --> remain invested, do nothing
            if oldSignal == True and newSignal == True:
                 myMonies = (myMonies * delta)
                 
            
            # Crossing DOWN --> Short 
            if oldSignal == True and newSignal == False:
                 myMonies = (1-taker_fee-spread_percentage)*(myMonies * 1/delta)
                 short_count += 1
                 
                 
            # Continued DOWNTREND --> remain shorted, do nothing
            if oldSignal == False and newSignal == False:
                 myMonies = (myMonies * 1/delta)
    
    
            # Crossing UP --> Long
            if oldSignal == False and newSignal != True:
                 myMonies = (1-taker_fee-spread_percentage)*(myMonies * delta)
                 long_count += 1
            

# Add symbol hold-only portfolio value to Performance DataFrame
temp = pd.to_numeric(df_prices[price_column])
BTC_USDT_portfolio = temp*(100/temp.iloc[0])*(start_val/100)
df_performance[symbol+" "+price_column] = BTC_USDT_portfolio 


# Calculate Stats DataFrame
df_stats = pd.DataFrame(columns=df_performance.columns)

for col in df_performance.columns:
    
    series = df_performance[col]
    
    # Variance
    #var = statistics.variance(series)
    #df_stats.loc['Variance', col] = "{:.2f}".format(var)
    
    # Portfolio value at beginning
    start_val = df_performance.at[start,col]
    df_stats.loc['Value at start', col] = "{:.0f}".format(start_val)
    
    # Portfolio value at end
    end_val = df_performance.at[len(df_performance)+start-1,col]
    df_stats.loc['Value at end', col] = "{:.0f}".format(end_val)
    
    # Total return
    return_percentage = end_val/start_val-1
    df_stats.loc['Return', col] = "{:.0%}".format(return_percentage)
    
    # Standard deviation
    stdev = statistics.stdev(series)
    df_stats.loc['Stdev', col] = "{:.0f}".format(stdev)
    
    # Sharpe ratio
    sharpe = qs.stats.sharpe(series)
    df_stats.loc['Sharpe', col] = "{:.3f}".format(sharpe)
    
    # Sortino (Funkar ej?)
    #sortino = qs.stats.sharpe(series)
    #df_stats.loc['Sortino', col] = "{:.3f}".format(sortino)
    
    # Max drawdown
    maxDD = qs.stats.max_drawdown(series)
    df_stats.loc['Max DD', col] = "{:.3%}".format(maxDD)
    
    # Average returns
    avg_returns = qs.stats.avg_return(series)
    df_stats.loc['Avg returns (%)', col] = "{:.3%}".format(avg_returns)
    
    # Geometric mean
    geometric_mean = qs.stats.geometric_mean(series)
    df_stats.loc['Geometric mean (%)', col] = "{:.3%}".format(geometric_mean)


print(df_stats)


# Plot Performance DataFrame
plt.figure()
#x_axis = range(0,len(df_performance))
#df_performance.plot(logy=True)
df_performance.plot(y=df_performance.columns)
plt.show()


plt.figure()
df_prices['Close']=pd.to_numeric(df_prices['Close'])
df_prices.plot(y=df_prices.columns)
plt.show()
plt.savefig('output.png')






            