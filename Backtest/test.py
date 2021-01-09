# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:25:04 2020

@author: JLuca
"""
from binance.client import Client 


key_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_key.txt'
secret_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_secret.txt'

api_key_path = key_path
api_secret_path = secret_path
with open(api_key_path) as f:
    api_key = f.read()
with open(api_secret_path) as f:
    api_secret = f.read()

symbol = "BTCUSDT"

client = Client(api_key, api_secret)

# Get average price
avg_price = client.get_avg_price(symbol=symbol)

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")