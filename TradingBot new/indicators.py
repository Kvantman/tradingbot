# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 14:00:58 2021

@author: JLuca
"""

import pandas as pd
import numpy as np
from binance.client import Client 


class Indicators:
    
    def __init__(self, price_data_frame):
        """
        Initalizes the indicator Client
        price_data_frame = pd.DataFrame(data=historical_prices)
        """
        
        self.price_data_frame = price_data_frame
        
        
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