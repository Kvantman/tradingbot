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
     
        
    def initialize_client(self):      
        self.client = Client(self.api_key, self.api_secret)
    
    
    def fetch_data(self, symbol, kline_interval, start_date, end_date):
        self.data = self.client.get_historical_klines(symbol, kline_interval, start_date, end_date)
        return self.data
    
    
    def create_price_df(self, inputData):
        self.df_prices = pd.DataFrame(inputData)
        self.df_prices.columns = ['Open time', 'Open', 'High', 'Low',
                             'Close', 'Volume', 'Close time',
                             'Quote asset volume',' Number of trades',
                             'Taker buy base asset volume', 
                             'Taker buy qoute asset volume', 'Ignore']
        return self.df_prices
    
    
    def name_price_columns(self, nameList):
        self.df_prices.columns = nameList
    
        
    def add_sma_columns(self, slow_periods: list, fast_periods: list) -> DataFrame:
         periods = set(slow_periods + fast_periods)
         dataframe = pd.DataFrame([])
         for period in periods:
             dataframe["SMA"+str(period)] = dataframe[price_column].rolling(period).mean()
         return dataframe
     
        
     def remove_rows(self, dataframe: DataFrame, numRows: int) -> DataFrame:
         # Remove first data rows for SMA to start  
         start = numRows
         dataframe = dataframe[start:]
         return dataframe
    
 

    

    



            