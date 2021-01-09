# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 19:04:03 2020

@author: JLuca
"""

import pandas as pd

class HODL:
    
    def __init__(self, prices: pd.DataFrame, periods: set, price_col: str, start_capital: float) -> pd.DataFrame:
        
        self.start = max(periods)
        self.start_capital = start_capital
        self.df_prices = pd.DataFrame(prices)[price_col].loc[self.start:]
        self.df_prices = pd.to_numeric(self.df_prices)
        self.first_price = self.df_prices[self.start]
        self.last_price = self.df_prices[len(self.df_prices)-1]
        
    
    def performance(self):
        self.portfolio = (self.df_prices / self.first_price) * self.start_capital
        self.portfolio = self.portfolio.to_frame()
        return self.portfolio
    

