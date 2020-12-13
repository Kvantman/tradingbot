# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:12:06 2020

@author: JLuca
"""
import time

from robot import Robot

key_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_key.txt'
secret_path = r'C:\Users\JLuca\Documents\repos\TradingBot/API_secret.txt'

# Create robot
my_robot = Robot(symbol = 'BTCUSDT', api_key_path = key_path, api_secret_path = secret_path)

# Set strategy
my_robot.set_MACD_strategy(time_resolution = '1d', fast_period = 9, slow_period = 22)


while __name__ == 'main':
    my_robot.run_robot()
    time.sleep(86400)
    
