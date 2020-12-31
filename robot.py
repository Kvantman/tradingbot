# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:49:10 2020

@author: JLuca
"""
import pandas as pd
import numpy as np
from binance.client import Client 

class Robot:
    
    
    def __init__(self, symbol, api_key_path, api_secret_path):
        self.symbol = symbol
        self.api_key_path = api_key_path
        self.api_secret_path = api_secret_path
        with open(api_key_path) as f:
            self.api_key = f.read()
        with open(api_secret_path) as f:
            self.api_secret = f.read()
            
        
    def set_MACD_strategy(self, time_resolution = '1d', fast_period = 9, slow_period = 22):
        self.time_resolution = time_resolution
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.window = fast_period
        
        
    def run(self):
        self._login_client()
        prices = self._fetch_historical_prices()
        signals = self._get_signals()
        trade = self._trade()
        
        
    def _login_client(self):
        self.client = Client(self.api_key, self.api_secret)
        

    def _fetch_historical_prices(self):
        prices = self.client.get_historical_klines(self.symbol, Client.KLINE_INTERVAL_1DAY, "100 day ago UTC")
        prices = pd.DataFrame(prices)
        column_names = ['Open time', 'Open', 'High', 'Low',
                         'Close', 'Volume', 'Close time',
                         'Quote asset volume',' Number of trades',
                         'Taker buy base asset volume', 
                         'Taker buy qoute asset volume', 'Ignore']
        prices.columns = column_names
        self.prices = prices        
        
        
    def _get_signals(self): 
        self.ma_fast = self.prices['Close'].rolling(self.fast_period).mean()
        self.ma_slow = self.prices['Close'].rolling(self.slow_period).mean()

        signals = np.array([])
        # Buy when ma_fast is above ma_slow
        if self.ma_fast.iloc[-1] > self.ma_slow.iloc[-1]:
            signals = np.append(signals, 1)
            
        # Sell signal when ma_fast is below ma_slow
        elif self.ma_fast.iloc[-1] < self.ma_slow.iloc[-1]:
            signals = np.append(signals, 0)
            
        # if signal = 1 <-- Invest or stay invested
        # if signal = 0 <-- Sell or remain out
        if signals.mean() > 0.5:
            signal = 1
        else:
            signal = 0
        
        self.signal = signal
            

    def _buy_or_sell(self):
        
        # Check if already invested
        self._get_account_balance()
        
        if self.account_balance['BTC'] > 0.0001:
            invested = True 
        
        # Get buy or sell signal
        if self.signal == 0 and invested:
            sell = True
        elif self.signal == 1 and not invested:
            buy = True
        elif self.signal == 1 and invested:
            pass
        elif self.signal == 0 and not invested:
            pass
        
        # Return buy/sell signal
        if 'buy' in locals():
            self.buy = buy
        
        if 'sell' in locals():
            self.sell = sell
    
    
    def _get_account_balance(self):
        account_balance = {}
        assets = ['BTC', 'ETH', 'LTC']
        for asset in assets:
            balance = self.client.get_asset_balance(asset)
            account_balance[asset] = float(balance['free'])
        
        self.account_balance = account_balance
    
    
    def _trade(self):
        self._buy_or_sell()
    
    
    def _order_target_percent(self):
        pass
    def _log_trades(self):
        pass
