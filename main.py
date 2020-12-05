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

print(key_path)
print(secret_path)

currency_pair = "BTCUSDT"
start = "1 Aug, 2020"
end = "30 Nov, 2020"

bt = BackTest(key_path, secret_path)
bt.initialize_client()
data = bt.fetch_data(currency_pair, Client.KLINE_INTERVAL_2HOUR, start, end)

df_prices = bt.create_price_df(data)

print(df_prices)