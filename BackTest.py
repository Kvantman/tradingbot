import pandas as pd
from binance.client import Client 
from KlineInterval import *

class BackTest:
    
    def __init__(self, api_key_path, api_secret_path):
        self.api_key_path = api_key_path
        self.api_secret_path = api_secret_path
        with open(api_key_path) as f:
            self.api_key = f.read()
        with open(api_secret_path) as f:
            self.api_secret = f.read()  
     
        
    def initialize_client(self) -> None:      
        self.client = Client(self.api_key, self.api_secret)
    
    
    def fetch_data(self, symbol, kline_interval, start_date, end_date) -> list:
        self.data = self.client.get_historical_klines(symbol, kline_interval, start_date, end_date)
        return self.data
    
    
    def create_price_df(self, inputData) -> pd.DataFrame:
        self.df_prices = pd.DataFrame(inputData)
        self.df_prices.columns = ['Open time', 'Open', 'High', 'Low',
                             'Close', 'Volume', 'Close time',
                             'Quote asset volume',' Number of trades',
                             'Taker buy base asset volume', 
                             'Taker buy qoute asset volume', 'Ignore']
        return self.df_prices
    
    
    #def name_price_columns(self, nameList) -> None:
        #self.df_prices.columns = nameList
    
        
    def create_sma_df(self, fast_periods: list, slow_periods: list) -> pd.DataFrame:
         self.periods = set(slow_periods + fast_periods)
         self.df_sma = pd.DataFrame()
         for period in self.periods:
             self.df_sma["SMA"+str(period)] = self.df_prices["Close"].rolling(period).mean()
         return self.df_sma
     
    # Remove first data rows for SMA to start    
    def remove_rows(self, dataframe: pd.DataFrame, numRows: int) -> pd.DataFrame:
         start = numRows
         dataframe = dataframe[start:]
         return dataframe
    
    def create_signals(self, dataframe: pd.DataFrame, period_fast, period_slow) -> pd.DataFrame:
        self.df_signals = pd.DataFrame()
        for a in period_fast:
            for b in period_slow:
                if a!=b and a<b:
                    sma_name=f"SMA({a},{b})"
                    self.df_signals[sma_name] = self.df_sma[f"SMA{a}"] > self.df_sma[f"SMA{b}"]              
        return self.df_signals


    



            