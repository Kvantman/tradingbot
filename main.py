# Import packages
from binance.client import Client 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
#import matplotlib.pyplot as plt
import quantstats as qs
import statistics

# Import Classes
from KlineInterval import *
from BackTest import *
from ComputePerformance import *
from ComputeStatistics import *
from HODL import *

key_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_key.txt'
secret_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_secret.txt'

backtest = BackTest(key_path, secret_path)

#--------------------- Optional -----------------#
backtest.symbol = "BTCUSDT"
backtest.start_date = "1 Jan, 2018"
backtest.end_date = "1 Jan, 2021"
backtest.kline_interval = KlineInterval.ONE_DAY
backtest.periods_fast = [7,9,12]
backtest.periods_slow = [18,22,26]
#------------------------------------------------#

backtest.indicator = "SMA"

backtest.initialize_client()

prices = backtest.df_prices

# Fix datetime colmn
prices['Open time'] = pd.to_datetime(prices['Open time'], unit='ms')
prices['Close time'] = pd.to_datetime(prices['Close time'], unit='ms')

# MACD Signals
signals = backtest.df_signals

# MACD performance
performance = ComputePerformance(df_signals=signals, df_prices=prices, shorting=False)
my_performance = performance.get_macd_performance()

# HODL
HODL_performance = HODL(prices, backtest.periods, 'Close', 100).performance()

# Add HODL to my_performance
my_df = my_performance
my_df['Close'] = HODL_performance

# STATS
# Get stats again to compare with HODL
comp_stats = ComputeStatistics()
stats = comp_stats.calculate_stats(my_df,backtest.periods)

# SMA PLOT
backtest.df_sma.plot()
plt.suptitle('SMA indicators', fontsize=18)
plt.ylabel('Price', fontsize=14)
plt.xlabel(f'Time resolution: {backtest.kline_interval}', fontsize=14)
plt.savefig('test.jpg')

# PORTFOLIO PLOT
#fig = plt.figure()
my_performance.plot()
plt.suptitle('Portfolio value over time', fontsize=18)
plt.ylabel('Portfolio value', fontsize=14)
plt.xlabel(f'Time resolution: {backtest.kline_interval}', fontsize=14)
plt.savefig('test.jpg')
#fig.savefig('test.jpg')


