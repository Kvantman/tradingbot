import pandas as pd
from binance.client import Client 
from KlineInterval import *

class ComputePerformance:
    
    start_capital = 100
    price_column = "Close"
    buy_count = {}
    sell_count = {}
    pass_count = {}
    long_count = {}
    short_count = {}
    trading_fee = 1/100
    taker_fee = 0.04/100
    spread_percentage = 0.05/100
    #shorting = False
    
    def __init__(self, df_signals: pd.DataFrame, df_prices: pd.DataFrame, shorting):
        self.df_signals = df_signals
        self.df_prices = df_prices
        self.shorting = shorting
        
        
    def get_macd_performance(self) -> pd.DataFrame:
        self.df_performance = pd.DataFrame(columns = self.df_signals.columns)
        
        for ma_column in self.df_performance.columns:
            myMonies = self.start_capital
            
            for row in range(self.df_signals.index[0 + 1], (self.df_signals.index[-1])):
                
                self.df_performance.at[row-1, ma_column] = myMonies
                
                previous_signal = self.df_signals.at[row - 1, ma_column]
                current_signal = self.df_signals.at[row, ma_column]       
         
                previous_price = self.df_prices.at[row - 1, self.price_column]
                current_price = self.df_prices.at[row, self.price_column]
                
                # Win will be for price of tomorrow compared to today
                next_price = self.df_prices.at[row + 1, self.price_column]
                delta  = float(next_price) / float(current_price)
    
                if not self.shorting: 

                    # Crossing UP --> Buy
                    if previous_signal == False and current_signal == True:
                         myMonies = (myMonies * delta) * (1 - self.trading_fee - self.spread_percentage)
                         if ma_column not in self.buy_count.keys():
                             self.buy_count[ma_column] = 1
                         else:
                             self.buy_count[ma_column] += 1
                         
                    # Continued UPTREND --> remain invested, do nothing
                    elif previous_signal == True and current_signal == True:
                         myMonies = myMonies * delta
                         if ma_column not in self.pass_count.keys():
                             self.pass_count[ma_column] = 1
                         else:
                             self.pass_count[ma_column] += 1
                    
                    # Crossing DOWN --> Sell
                    elif previous_signal == True and current_signal == False:
                         myMonies = (myMonies * delta) * (1 - self.trading_fee - self.spread_percentage)
                         if ma_column not in self.sell_count.keys():
                             self.sell_count[ma_column] = 1
                         else:
                             self.sell_count[ma_column] += 1
                         
                    # Continued DOWNTREND --> remain out, do nothing
                    elif previous_signal == False and current_signal == False:
                         if ma_column not in self.pass_count.keys():
                             self.pass_count[ma_column] = 1
                         else:
                             self.pass_count[ma_column] += 1
                            
                
                if self.shorting:
                    
                    # Continued UPTREND --> remain invested, do nothing
                    if previous_signal == True and current_signal == True:
                         myMonies = (myMonies * delta)
                         if ma_column not in self.pass_count.keys():
                             self.pass_count[ma_column] = 1
                         else:
                             self.pass_count[ma_column] += 1
                         
                    
                    # Crossing DOWN --> Short 
                    if previous_signal == True and current_signal == False:
                         myMonies = (myMonies * 1/delta) * (1 - self.taker_fee - self.spread_percentage)
                         if ma_column not in self.short_count.keys():
                             self.short_count[ma_column] = 1
                         else:
                             self.short_count[ma_column] += 1
                         
                         
                    # Continued DOWNTREND --> remain shorted, do nothing
                    if previous_signal == False and current_signal == False:
                         myMonies = (myMonies * 1/delta)
                         if ma_column not in self.pass_count.keys():
                             self.pass_count[ma_column] = 1
                         else:
                             self.pass_count[ma_column] += 1
            
            
                    # Crossing UP --> Long
                    if previous_signal == False and current_signal != True:
                         myMonies = (myMonies * delta) * (1 - self.taker_fee - self.spread_percentage)
                         if ma_column not in self.long_count.keys():
                             self.long_count[ma_column] = 1
                         else:
                             self.long_count[ma_column] += 1
                             
        return self.df_performance

