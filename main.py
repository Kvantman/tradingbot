# Import packages
from binance.client import Client 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quantstats as qs
import statistics

# Import Classes
from KlineInterval import *
from BackTest import *
from ComputePerformance import *
from ComputeStatistics import *

key_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_key.txt'
secret_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_secret.txt'

backtest = BackTest(key_path, secret_path)

#--------------------- Optional -----------------#
backtest.symbol = "ETHUSDT"
backtest.start_date = "1 Jan, 2018"
backtest.end_date = "8 Dec, 2020"
backtest.kline_interval = KlineInterval.ONE_DAY
backtest.periods_fast = [8,10,12,14]
backtest.periods_slow = [10,20,30,40,50,60,70,80]
#------------------------------------------------#

backtest.indicator = "WMA"

backtest.initialize_client()

prices = backtest.df_prices

# Fix datetime colmn
prices['Open time'] = pd.to_datetime(prices['Open time'], unit='ms')
prices['Close time'] = pd.to_datetime(prices['Close time'], unit='ms')

signals = backtest.df_signals

performance = ComputePerformance(df_signals=signals, df_prices=prices)

test = performance.get_macd_performance()

comp_stat = ComputeStatistics()

my_stats = comp_stat.calculate_stats(test, backtest.periods)

print("...MY STATS...")
print(my_stats)


#df_prices.loc[325,:]