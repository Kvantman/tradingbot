# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 19:05:14 2021

@author: JLuca
"""

class Portfolio:
    
    def __init__(self):
        pass
    
    
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