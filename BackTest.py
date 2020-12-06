import pandas as pd
from binance.client import Client 
from KlineInterval import *
#from datetime import date

class BackTest:
    
    symbol = "BTCUSDT"
    start_date = "1 Jan, 2020"
    end_date = "1 Dec, 2020"
    kline_interval = KlineInterval.ONE_DAY
    periods_fast = [1, 2]
    periods_slow = [5, 10, 15]
    price_column = "Close"
    start_capital = 100
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
    
    # Setters
    def set_symbol(self, currency_pair: str) -> None:
        self.symbol = currency_pair
        
        
    def set_start_date(self, start_date: str) -> None:
        self.start_date = start_date
    
    
    def set_end_date(self, end_date: str) -> None:
        self.end_date = end_date
        
    # interval is of what type?
    #def set_kline_interval(self, interval) -> None:
        #self.kline_interval = KlientInterval.interval
        
        
    def set_periods_fast(self, period : list) -> None:
        self.periods_fast = period
        
        
    def set_periods_slow(self, period : list) -> None:
        self.periods_slow = period
        
        
    def set_price_column(self, column_name: str) -> None:
        self.price_column = column_name
        
        
    def set_start_capital(self, capital: float) -> None:
        self.start_capital = capital
        
    
    def set_column_names(self, names: list) -> None:
        self.column_names = names
        

    def initialize_client(self) -> None:      
        self.client = Client(self.api_key, self.api_secret)
        self.fetch_data()
        self.create_price_df()
        self.create_sma_df()
        self.create_signals()
        

    def fetch_data(self) -> None:
        self.df_data = self.client.get_historical_klines(self.symbol, self.kline_interval, self.start_date, self.end_date)
    

    def create_price_df(self) -> None:
        self.df_prices = pd.DataFrame(self.df_data)
        self.df_prices.columns = self.column_names
    
        
    def create_sma_df(self) -> None:
         self.periods = set(self.periods_slow + self.periods_fast)
         self.df_sma = pd.DataFrame()
         for period in self.periods:
             self.df_sma["SMA"+str(period)] = self.df_prices["Close"].rolling(period).mean()
         self.df_sma = self.remove_rows(self.df_sma, max(self.periods))
         
        
    def remove_rows(self, dataframe: pd.DataFrame, numRows: int) -> pd.DataFrame:
         start = numRows
         df_removed_rows = dataframe[start:]
         return df_removed_rows
        
    
    def create_signals(self) -> None:
        self.df_signals = pd.DataFrame()
        for a in self.periods_fast:
            for b in self.periods_slow:
                if a!=b and a<b:
                    sma_name=f"SMA({a},{b})"
                    self.df_signals[sma_name] = self.df_sma[f"SMA{a}"] > self.df_sma[f"SMA{b}"]              

        


            