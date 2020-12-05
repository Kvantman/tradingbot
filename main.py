from binance.client import Client 
# jamel comment

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import quantstats as qs
#import statistics

#from KlineInterval import *
from BackTest import *

key_path = r'/home/pi/repos/TradingBot/tradingbot/API_key.txt'
secret_path = r'/home/pi/repos/TradingBot/tradingbot/API_secret.txt'

#input_key_path = input("Enter path to your API key: ")
#print(input_key_path)
#input_key_path = input("Enter path to your API secret: ")
#print(input_secret_path)

currency_pair = "BTCUSDT"
start = "1 Aug, 2020"
end = "30 Nov, 2020"

#bt = BackTest(input_key_path, input_secret_path)
bt = BackTest(key_path, secret_path)
bt.initialize_client()
data = bt.fetch_data(currency_pair, Client.KLINE_INTERVAL_2HOUR, start, end)

df_prices = bt.create_price_df(data)

period_fast = [2, 4, 6, 8]
period_slow = [20, 25, 30, 40]

df_sma = bt.create_sma_df(period_fast, period_slow)

periods = set(period_fast + period_slow)
start = max(periods)

df_prices = bt.remove_rows(df_prices, start)

print(df_prices)

df_signals = bt.create_signals(df_prices, period_fast, period_slow)
print(df_signals)
