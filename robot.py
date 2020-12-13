# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:49:10 2020

@author: JLuca
"""
import pandas as pd

class Robot:
    
    
    def __init__(symbol = 'BTCUSDT', api_key_path, api_secret_path):
        self.symbol = symbol
        self.interval = Client.KLINE_INTERVAL_1DAY 
        self.window = "100 day ago UTC"
        self.api_key_path = api_key_path
        self.api_secret_path = api_secret_path
        with open(api_key_path) as f:
            self.api_key = f.read()
        with open(api_secret_path) as f:
            self.api_secret = f.read()
    
    
    def login_client():
        self.client = Client(self.api_key, self.api_secret)
        
        
        
    def set_MACD_strategy(time_resolution = '1d', fast_period = 9, slow_period = 22):
        self.time_resolution = time_resolution
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.window = fast_period
        
        
    def run_robot():
        
        prices = self._fetch_historical_prices()
    
        signals = self._get_signals()
        
        trade = self._trade()

        account_balance = self._get_account_balance()
    
    
    def _fetch_historical_prices(self):
        prices = client.get_historical_klines(self.symbol, self.interval, self.window = "100 day ago UTC", "TODAY")
        prices = pd.DataFrame(prices)
        
    
    def _get_signals():        
        pass
        
    
    def _trade():
        pass
    
    
    def _get_account_balance():
        pass
