# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:49:10 2020

@author: JLuca
"""
import pandas as pd
import numpy as np
from binance.client import Client 

class Robot:
    
    min_trade_val = 1
    assets = ['EUR', 'USDT','BTC', 'ETH', 'LTC', 'BNB']
    
    def __init__(self, symbol_pair, api_key_path, api_secret_path):
        self.symbol_pair = symbol_pair
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
        self._fetch_historical_prices()
        self._trade()
        
        
    def _login_client(self):
        self.client = Client(self.api_key, self.api_secret)
        
    
    def _fetch_historical_prices(self):
        prices = self.client.get_historical_klines(self.symbol_pair, Client.KLINE_INTERVAL_1DAY, "100 day ago UTC")
        prices = pd.DataFrame(prices)
        column_names = ['Open time', 'Open', 'High', 'Low',
                         'Close', 'Volume', 'Close time',
                         'Quote asset volume',' Number of trades',
                         'Taker buy base asset volume', 
                         'Taker buy qoute asset volume', 'Ignore']
        prices.columns = column_names
        self.prices = prices

    
    def _trade(self):
        trade_signal = self._get_trade_signal()

        if trade_signal == 'BUY': # BUY
            _order_target_percent(self, self.symbol_pair, 100)
            print("buy")
            
        if trade_signal == 'SELL': # SELL
            _order_target_percent(self, self.symbol_pair, 0)
            print("sell")
            
        if trade_signal == 'PASS': #PASS
            print("pass")
            
            
    def _get_trade_signal(self):
        
        indicator_signal = self._get_indicator_signal()
        
        # Check if already invested
        self._get_account_balance()
        
        if self.account_balance_USDT['BTC'] > 1:
            invested = True
        else:
            invested = False
        
        # Get buy or sell signal
        
        if indicator_signal == 0 and invested: # SELL
            signal = 'SELL'
            print("1")
            
        elif indicator_signal == 1 and not invested: # BUY
            signal = 'BUY'
            print("2")
            
        elif indicator_signal == 1 and invested: # Do nothing
            signal = 'PASS'
            print("3")

        elif indicator_signal == 0 and not invested: # Do nothing
            signal = 'PASS'
            print("4")
        
        return signal
            
      
    def _get_indicator_signal(self): 
        self.ma_fast = self.prices['Close'].rolling(self.fast_period).mean()
        self.ma_slow = self.prices['Close'].rolling(self.slow_period).mean()

        signal_array = np.array([])
        
        # Buy when ma_fast is above ma_slow
        if self.ma_fast.iloc[-1] > self.ma_slow.iloc[-1]:
            signal_array = np.append(signal_array, 1)
            
        # Sell signal when ma_fast is below ma_slow
        elif self.ma_fast.iloc[-1] < self.ma_slow.iloc[-1]:
            signal_array = np.append(signal_array, 0)
            
        # if signal = 1 <-- Invest or stay invested
        # if signal = 0 <-- Sell or remain out
        if signal_array.mean() > 0.5:
            signal = 1
        else:
            signal = 0
            
        return signal
            
            
    def _get_account_balance(self):
        account_balance = {}
        for asset in self.assets:
            balance = self.client.get_asset_balance(asset)
            account_balance[asset] = float(balance['free'])
        self.account_balance = account_balance
        
        # Get account value in USDT
        self._get_account_balance_USDT()
        
        
    def _get_account_balance_USDT(self):
        account_balance_USDT = {} # Qouted in USDT
        
        for asset in self.account_balance.keys():
            if asset != 'USDT':
                symbol_pair = asset+'USDT'
                asset_price = float(self.client.get_avg_price(symbol = symbol_pair)['price']) # Avg 5 min price 
                asset_value = asset_price * self.account_balance[asset]
            elif asset == 'USDT':
                asset_value = self.account_balance['USDT']
            account_balance_USDT[asset] = asset_value
        self.account_balance_USDT = account_balance_USDT
         
            
    def _order_target_percent(self, symbol, target_percent):
        print("order target percent")
        total_value = self.account_balance_USDT[symbol]
        print(total_value)
        target_value = total_value * (target_percent/100)
        print(target_value)
        delta = self.account_balance_USDT[symbol] - target_value
        print(delta)
        
        
        if delta > 0 and abs(delta) > self.min_trade_val:
            # Sell
            pass
            #quantity_sell = 
            #_market_order_sell(self, symbol=self.symbol, quantity = quantity_sell)
            
    
        elif delta < 0 and abs(delta) > self.min_trade_val:
            # Buy
            pass
            #quantity_buy =                   
            #_market_order_buy(self, symbol=self.symbol, quantity = quantity_buy)
            
                                             
    def _market_order_buy(self, symbol, quantity):
        order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
        
        
    def _market_order_sell(self, symbol, quantity):
        order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
        
        
    def _order_limit_buy(self, symbol, quantity, price):
        order = client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)


    def _order_limit_sell(self, symbol, quantity, price):
        order = client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)


    def _log_trades(self):
        pass
