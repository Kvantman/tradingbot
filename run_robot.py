# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:12:06 2020

@author: JLuca
"""
import time

from robot import Robot

key_path = r"/home/pi/Desktop/api_key.txt"
secret_path = r"/home/pi/Desktop/api_secret.txt"

# Default params
symbol = 'BTCUSDT'
time_resolution = '1d'
fast_period = 9
slow_period = 22

# Create robot
my_robot = Robot(symbol, key_path, secret_path)

# Set strategy
my_robot.set_MACD_strategy(time_resolution, fast_period, slow_period)

my_robot.run()


#while __name__ == 'main':
#    my_robot.run()
#    print(my_robot.ma_slow)
#    time.sleep(86400)
    
