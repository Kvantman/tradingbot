# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 18:59:18 2021

@author: JLuca
"""

class Trade:
        
        def __init__(self):
            pass
    
        def _trade(self):
        trade_signal = self._get_trade_signal()
        
        #if trade_signal:
        if trade_signal == 'BUY': # BUY
            print("TODO: BUY")
            self._order_target_percent(symbol = "LTC", target_percent = 100)
            print("buy done")
            
        elif trade_signal == 'SELL': # SELL
            self._order_target_percent("LTC", 0)
            print("sell")
            
        elif trade_signal == 'PASS': #PASS
            print("pass ok")
            
            
    def _get_trade_signal(self):
        
        indicator_signal = self._get_indicator_signal()
        
        # Check if already invested
        self._get_account_balance()
        if self.account_balance_USDT['LTC'] > self.minNotional:
            invested = True
        else:
            invested = False
        
        # Get buy or sell signal
        if indicator_signal == 0 and invested: # SELL
            signal = 'SELL'
            
        elif indicator_signal == 1 and not invested: # BUY
            signal = 'BUY'
            
        elif indicator_signal == 1 and invested: # Do nothing
            signal = 'PASS'

        elif indicator_signal == 0 and not invested: # Do nothing
            signal = 'PASS'
            
        else:
            signal = 'PASS'
        
        return signal
    
    
    def _order_target_percent(self, symbol, target_percent):
        total_value = self.account_balance_USDT[symbol] + self.account_balance_USDT["USDT"]
        target_value = total_value * (target_percent/100)
        delta = self.account_balance_USDT[symbol] - target_value
        delta_abs = abs(delta)

 
        if delta > 0 and abs(delta) > self.min_trade_val:
            # Sell
            if self.account_balance[symbol] == 0:
                amount = 0.99 * (self.account_balance['USDT']/self.current_price('LTCUSDT'))
            else:
                symbol_fraction = (delta_abs / self.account_balance[symbol])
                symbol_value = self.account_balance[symbol]
                amount = 0.99 * symbol_fraction * symbol_value
            
            self._market_order_sell(symbol = self.symbol_pair, quantity = self._order_format(amount))
            print("_order SELL")
            
    
        elif delta < 0 and abs(delta) > self.min_trade_val:
            # Buy
            if self.account_balance[symbol] == 0:
                amount = 0.99 * (self.account_balance['USDT']/self._get_current_price(symbol_pair = self.symbol_pair))
            else:
                symbol_fraction = (delta_abs / self.account_balance[symbol])
                symbol_value = self.account_balance[symbol]
                amount = 0.99 * symbol_fraction * symbol_value
                
            self._market_order_buy(symbol = self.symbol_pair, quantity = self._order_format(amount))
            print("_order BUY")

        else:
            print("_order pass")

            
    def _order_format(self, amount):
        precision = 5
        amount_str = "{:0.0{}f}".format(amount, precision)
        return amount_str
            
                                             
    def _market_order_buy(self, symbol, quantity):
        order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
        
        
    def _market_order_sell(self, symbol, quantity):
        order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
        
        
    def _order_limit_buy(self, symbol, quantity, price):
        order = client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)
        

    def _order_limit_sell(self, symbol, quantity, price):
        order = client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)