import pandas as pd
import numpy as np
from binance.client import Client 
from KlineInterval import *

#from datetime import date

class BackTest:
    
    symbol = "BTCUSDT"
    start_date = "1 Jan, 2020"
    end_date = "1 Dec, 2020"
    kline_interval = KlineInterval.ONE_DAY
    periods_fast = [6]
    periods_slow = [9,15,21,30]
    price_column = "Close"
    indicator = "SMA"
    column_names = ['Open time', 'Open', 'High', 'Low',
                             'Close', 'Volume', 'Close time',
                             'Quote asset volume',' Number of trades',
                             'Taker buy base asset volume', 
                             'Taker buy qoute asset volume', 'Ignore']
    
    
    def __init__(self, api_key_path, api_secret_path):
        self.api_key_path = api_key_path
        self.api_secret_path = api_secret_path
        with open(api_key_path) as f:
            self.api_key = f.read()
        with open(api_secret_path) as f:
            self.api_secret = f.read()
            

    def initialize_client(self) -> None:      
        self.client = Client(self.api_key, self.api_secret)
        self.fetch_data()
        self.create_price_df()
        self.create_ma_df()
        self.create_signals()
        

    def fetch_data(self) -> None:
        self.df_data = self.client.get_historical_klines(self.symbol, self.kline_interval, self.start_date, self.end_date)
    

    def create_price_df(self) -> None:
        self.df_prices = pd.DataFrame(self.df_data)
        self.df_prices.columns = self.column_names
    
    
    def create_ma_df(self) -> None:
        self.periods = set(self.periods_slow + self.periods_fast)
        
        if self.indicator == "SMA":
            self.create_sma_df()
        elif self.indicator == "EMA":
            self.create_ema_df()
        elif self.indicator == "WMA":
            self.create_wma_df()
            
        
    def create_sma_df(self) -> None:
        self.df_sma = pd.DataFrame()
        
        for period in self.periods:
            self.df_sma["SMA"+str(period)] = self.df_prices["Close"].rolling(period).mean()
            
        self.df_sma = self.remove_rows(self.df_sma, max(self.periods))
        
        
    def create_wma_df(self) -> None:
        self.df_wma = pd.DataFrame()
        
        for period in self.periods:
            weights = np.arange(1, period + 1)
            self.df_wma["WMA"+str(period)] = self.df_prices["Close"].rolling(period).apply(lambda prices: np.dot(weights, prices)/weights.sum(), raw = True)
        
        self.df_wma = self.remove_rows(self.df_wma, max(self.periods))
    
    
    def create_ema_df(self) -> None:
        self.df_ema = pd.DataFrame()
        
        for period in self.periods:
            self.df_ema["EMA"+str(period)] = self.df_prices["Close"].ewm(span = period).mean()
        
        self.df_ema = self.remove_rows(self.df_ema, max(self.periods))
    
        
    def remove_rows(self, dataframe: pd.DataFrame, numRows: int) -> pd.DataFrame:
        start = numRows
        df_removed_rows = dataframe[start:]
        return df_removed_rows
        
    
    def create_signals(self) -> None:
        self.df_signals = pd.DataFrame()
        for a in self.periods_fast:
            for b in self.periods_slow:
                if a != b and a < b:
                    if self.indicator == "SMA":
                        sma_name=f"SMA({a},{b})"
                        self.df_signals[sma_name] = self.df_sma[f"SMA{a}"] > self.df_sma[f"SMA{b}"]
                    elif self.indicator == "WMA":
                        wma_name=f"WMA({a},{b})"
                        self.df_signals[wma_name] = self.df_wma[f"WMA{a}"] > self.df_wma[f"WMA{b}"]  
                    elif self.indicator == "EMA":
                        ema_name=f"EMA({a},{b})"
                        self.df_signals[ema_name] = self.df_ema[f"EMA{a}"] > self.df_ema[f"EMA{b}"]  

        
        
            