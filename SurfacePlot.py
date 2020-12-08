# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 22:52:51 2020

@author: JLuca
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

class SurfacePlot:
    
    def __init__(self, df_stats: pd.DataFrame):
        self.df_stats = df_stats
        self.y_return = df_stats.loc['Return',:]
        self.y_sharpe = df_stats.loc['Sharpe',:]
        self.y_Max_DD = df_stats.loc['Max DD',:]
    
    def _plot(self, series):
        x=series
        y=
    
    

x = np.outer(np.linspace(-2, 2, 30), np.ones(30))
y = x.copy().T # transpose
z = np.cos(x ** 2 + y ** 2)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(x, y, z,cmap='viridis', edgecolor='none')
ax.set_title('Surface plot')
plt.show()