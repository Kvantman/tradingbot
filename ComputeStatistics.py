import pandas as pd
from binance.client import Client 
from KlineInterval import *
import statistics
import quantstats as qs

class ComputeStatistics:
    
    start = 0
    
    def __init__(self):
        self.test = 1
        
    
    def calculate_stats(self, df_performance: pd.DataFrame, periods) -> pd.DataFrame:
        # Calculate Stats DataFrame
        self.df_stats = pd.DataFrame(columns = df_performance.columns)

        for col in df_performance.columns:
            
            series = df_performance[col]
            
            # Variance
            #var = statistics.variance(series)
            #self.df_stats.loc['Variance', col] = "{:.2f}".format(var)
            
            # Portfolio value at beginning
            start_val = df_performance.at[max(periods), col]
            self.df_stats.loc['Value at start', col] = "{:.0f}".format(start_val)
            
            # Portfolio value at end
            end_val = df_performance.at[len(df_performance) + max(periods) - 1,col]
            self.df_stats.loc['Value at end', col] = "{:.0f}".format(end_val)
            
            # Total return
            return_percentage = end_val / (start_val - 1)
            self.df_stats.loc['Return', col] = "{:.0%}".format(return_percentage)
            
            # Standard deviation
            stdev = statistics.stdev(series)
            self.df_stats.loc['Stdev', col] = "{:.0f}".format(stdev)
            
            # Sharpe ratio
            sharpe = qs.stats.sharpe(series)
            self.df_stats.loc['Sharpe', col] = "{:.3f}".format(sharpe)
            
            # Sortino (Funkar ej?)
            #sortino = qs.stats.sharpe(series)
            #self.df_stats.loc['Sortino', col] = "{:.3f}".format(sortino)
            
            # Max drawdown
            maxDD = qs.stats.max_drawdown(series)
            self.df_stats.loc['Max DD', col] = "{:.3%}".format(maxDD)
            
            # Average returns
            avg_returns = qs.stats.avg_return(series)
            self.df_stats.loc['Avg returns (%)', col] = "{:.3%}".format(avg_returns)
            
            # Geometric mean
            geometric_mean = qs.stats.geometric_mean(series)
            self.df_stats.loc['Geometric mean (%)', col] = "{:.3%}".format(geometric_mean)
            
        return self.df_stats
