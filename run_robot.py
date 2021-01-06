# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:12:06 2020

@author: JLuca
"""
import time
import pandas as pd

from robot import Robot

key_path = r"/home/pi/Desktop/api_key.txt"
secret_path = r"/home/pi/Desktop/api_secret.txt"

#key_path = r"C:\Users\JLuca\Documents\repos\TradingBot\api_key.txt"
#secret_path = r"C:\Users\JLuca\Documents\repos\TradingBot\api_secret.txt"

# Default params
symbol_pair = 'LTCUSDT'
time_resolution = '1d'
fast_period = 9
slow_period = 22

# Create robot
my_robot = Robot(symbol_pair, key_path, secret_path)

# Set strategy
my_robot.set_MACD_strategy(time_resolution, fast_period, slow_period)

# Run!
my_robot.run()

# symbol info
info = my_robot.client.get_symbol_info('LTCUSDT')
print(info)


# SYMBOL info
#info = client.get_symbol_info('ETHUSDT')
#print(info)

# Test check
#info = pd.DataFrame([my_robot.client.get_account()])

#asset_balance = pd.DataFrame([my_robot.client.get_asset_balance])


#while __name__ == 'main':
#    my_robot.run()
#    print(my_robot.ma_slow)
#    time.sleep(86400)
    
