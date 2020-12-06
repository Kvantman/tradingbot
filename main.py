from binance.client import Client 
# jamel comment

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import quantstats as qs
#import statistics

from KlineInterval import *
from BackTest import *

key_path = r'/home/pi/repos/TradingBot/tradingbot/API_key.txt'
secret_path = r'/home/pi/repos/TradingBot/tradingbot/API_secret.txt'

#input_key_path = input("Enter path to your API key: ")
#print(input_key_path)
#input_key_path = input("Enter path to your API secret: ")
#print(input_secret_path)

#backtest = BackTest(input_key_path, input_secret_path)
backtest = BackTest(key_path, secret_path)

# # Optional
# backtest.set_symbol("BTCUSDT")
# backtest.set_start_date("1 Dec, 2019")
# backtest.set_end_date("1 Dec, 2020")
# backtest.set_kline_interval = TWELVE_HOURS # TODO: set type?
# backtest.set_periods_fast = [2, 4, 6, 8]
# backtest.set_periods_slow = [20, 25, 30, 40]
# backtest.set_price_column = "Close"

backtest.initialize_client()
my_prices = backtest.df_prices
my_SMA = backtest.df_sma
my_signals = backtest.df_signals

print(my_prices)
print("\n....hohohohoo..........\n")
print(my_SMA)
print("\n....hohohohoo..........\n")
print(my_signals)
