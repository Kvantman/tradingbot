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
    
    
    def name_price_columns(self, nameList) -> None:
        self.df_prices.columns = nameList
    
        
    def add_sma_columns(self, slow_periods: list, fast_periods: list) -> pd.DataFrame:
         self.periods = set(slow_periods + fast_periods)
         sma_columns = pd.DataFrame([])
         for period in periods:
             sma_columns["SMA"+str(period)] = sma_columns[price_column].rolling(period).mean()
         return sma_columns
     
        
    

    



            