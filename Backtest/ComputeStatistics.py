import pandas as pd
from binance.client import Client 
from KlineInterval import *
import statistics
import quantstats as qs

class ComputeStatistics:
    
    start = 0
    
    def __init__(self):
        self.test = 1
        
    
    def calculate_stats(self, df_performance, periods) -> pd.DataFrame:
        # Calculate Stats DataFrame
        self.df_stats = pd.DataFrame(columns = df_performance.columns)

        for col in df_performance.columns:
            
            series = df_performance[col]
            
            # Portfolio value at beginning
            start_val = df_performance.at[max(periods), col]
            self.df_stats.loc['Value at start', col] = float("{:.3f}".format(start_val))
            
            # Portfolio value at end
            end_val = df_performance.at[len(df_performance) + max(periods) - 1,col]
            self.df_stats.loc['Value at end', col] = float("{:.3f}".format(end_val))
            
            # Return
            return_percentage = ( (end_val/start_val) - 1 )
            self.df_stats.loc['Return', col] = float("{:.3f}".format(return_percentage))
            
            # Standard deviation
            stdev = statistics.stdev(series)
            self.df_stats.loc['Stdev', col] = float("{:.3f}".format(stdev))
            
            # Variance
            #var = statistics.variance(series)
            #self.df_stats.loc['Variance', col] = "{:.2f}".format(var)
            
            # Sharpe ratio
            sharpe = qs.stats.sharpe(series)
            self.df_stats.loc['Sharpe', col] = float("{:.3f}".format(sharpe))
            
            # Max drawdown
            maxDD = qs.stats.max_drawdown(series)
            self.df_stats.loc['Max DD', col] = float("{:.3f}".format(maxDD))
            
            
        return self.df_stats
