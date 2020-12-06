from binance.client import Client 
# jamel comment

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import quantstats as qs
#import statistics

from KlineInterval import *
from BackTest import *
from ComputePerformance import *

key_path = r'/home/pi/repos/TradingBot/tradingbot/API_key.txt'
secret_path = r'/home/pi/repos/TradingBot/tradingbot/API_secret.txt'

#input_key_path = input("Enter path to your API key: ")
#print(input_key_path)
#input_key_path = input("Enter path to your API secret: ")
#print(input_secret_path)

#backtest_old = BackTest(input_key_path, input_secret_path)
backtest = BackTest(key_path, secret_path)
backtest_ema = BackTest(key_path, secret_path)
backtest_wma = BackTest(key_path, secret_path)


# # Optional
# backtest.symbol = "BTCUSDT"
backtest_wma.start_date = "1 Jun, 2018"
backtest_wma.end_date = "1 Jun, 2019"
# backtest.kline_interval = KlineInterval.TWELVE_HOURS
backtest_wma.periods_fast = [4, 6]
backtest_wma.periods_slow = [12, 18, 30]

backtest.indicator = "SMA"
backtest_ema.indicator = "EMA"
backtest_wma.indicator = "WMA"

backtest.initialize_client()
backtest_ema.initialize_client()
backtest_wma.initialize_client()

my_prices = backtest.df_prices
my_signals = backtest.df_signals

prices_ema = backtest_ema.df_prices
signals_ema = backtest_ema.df_signals

prices_wma = backtest_wma.df_prices
signals_wma = backtest_wma.df_signals


performance = ComputePerformance(my_signals, my_prices)
performance_ema = ComputePerformance(signals_ema, prices_ema)
performance_wma = ComputePerformance(signals_wma, prices_wma)

test = performance.get_macd_performance()
test_ema = performance_ema.get_macd_performance()
test_wma = performance_wma.get_macd_performance()

print("\n EMA")
print(test_ema)
print("\n WMA")
print(test_wma)
print("\n SMA")
print(test)


