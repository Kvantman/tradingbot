# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 19:04:03 2020

@author: JLuca
"""
import pandas as pd
import numpy as np

class HODLPortfolio:
    
    def __init(self, df_price: pd.DataFrame, start_date: str, end_date: str, date_col: str, price_col: str, start_capital: float) -> pd.DataFame:
        self.df_prices = df_prices
        self.start_date = start_date
        self.end_date = end_date
        self.price_col = price_col
        self.start_capital = start_capital
    
    def _filter_date():
        self.df_temp = self.df_prices[[date_col,price_col]].copy()
        self.df_temp = df_temp[df_temp[date_col]>start_date]
        self.df_temp = df_temp[df_temp[date_col]<end_date]
        
    def _to_numeric():
        self.numeric_prices = pd.to_numeric(df_temp[price_col])
        self.df_prices[price_col] = numeric_prices
        
    def _HODL_performance():
        self.first_price = self.df_temp[price_col].iloc[0]
        self.last_price = self.df_temp[price_col].iloc[-1]
        self.portfolio_return = last_price / first_price
        self.df_portfolio = (df_temp / first_price) * start_capital
    
    
        
# Add symbol hold-only portfolio value to Performance DataFrame
#temp = pd.to_numeric(df_prices[price_column])
#BTC_USDT_portfolio = temp*(100/temp.iloc[0])*(start_val/100)
#df_performance[symbol+" "+price_column] = BTC_USDT_portfolio 