# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:12:06 2020

@author: JLuca
"""
import time
from datetime import date, datetime
import pandas as pd
import numpy as np

from robot import Robot

#key_path = r"/home/pi/Desktop/api_key.txt"
#secret_path = r"/home/pi/Desktop/api_secret.txt"

# API key
key_path = r"C:\Users\JLuca\Documents\repos\TradingBot\api_key.txt"
secret_path = r"C:\Users\JLuca\Documents\repos\TradingBot\api_secret.txt"

# Default params
symbol_pair = 'LTCUSDT'
time_resolution = '1d'
fast_period = 9
slow_period = 22

# Create robot
my_robot = Robot(symbol_pair, key_path, secret_path)

# Set strategy
my_robot.set_MACD_strategy(time_resolution, fast_period, slow_period)

# Create a log_book
log_book = pd.DataFrame([])

# Index runs
ind = 0

# Run continously
while True:
    
    # Run robot
    my_robot.run()
    print("robot is run")
    
    ## RECORD KEEPING ##
    
    # Create a temporary DataFrame to store todays values
    temp = pd.DataFrame([])
    
    # Add index
    ind_df = pd.DataFrame(np.array([ind]), columns=['index'])
    temp = temp.append(ind_df)

    # Add timestamp
    #today = date.today().strftime("%B %d, %Y")
    now = datetime.timestamp(datetime.now())
    now_df = pd.DataFrame(np.array([now]), columns=['timestamp'])
    temp = temp.join(now_df)
    
    # Record account_balance
    account_balance = my_robot.account_balance
    account_balance_df = pd.DataFrame(data=account_balance, index = [ind])
    temp = temp.join(account_balance_df)
    
    # Stack DataFrame to record_book
    log_book = pd.concat([log_book, temp], axis = 0) # Horizontical stacking DataFrames
    print(log_book)
    
    # add trades....
    
    # Update index
    
    ind += 1
    
    # Sleep robot
    time.sleep(8.6400)


    
