#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:20:58 2018

@author: wengshian
"""
import os.path
import os, glob, string
import numpy as np
import pandas as pd
import itertools
import csv
import urllib
import urllib.request
import requests

from scipy import stats


#Download all stock files
#save_path = '/stock_data'
'''
positions = pd.read_excel('TSF_Portfolio.xlsx')
names = list(positions["Ticker"])

for i in range(len(names)):
    print(i)
    ticker = names[i]
    url = 'https://stooq.com/q/d/l/?s=' + ticker + ".US&i=d"
    r = requests.get(url, allow_redirects=True)
    open(ticker, 'wb').write(r.content)
'''

    
# 1. Load stock data into a dataframe and prepare for analysis


#1.1 Load close prices
# Set the directory to the directory where the stock data is stored
os.chdir("/Users/wengshian/Documents/GitHub/TSF-Risk/stock_data")

# prepare the fileList and dataframe for stock data
fileList = []
df = pd.DataFrame()

# set number of past days to load into dataframe
dataSetSize = 100

# read all file names
for files in glob.glob("*.txts"):
    print(files)
    #ignore empty files
    if os.path.getsize(files) == 0:
        continue

    filename = os.path.basename(files).partition('.')[0]
    fileList.append(filename)

# iterate through files and take close values
for file in glob.glob("*.txt"):

    #ignore empty files
    if os.path.getsize(file) == 0:
        continue

    frame = pd.read_table(file, header = 0, sep = ',', index_col = 0)['Close'].tail(dataSetSize)
    print(frame)
    df = df.append(frame)

# change row names to stock ticker symbols
df.index = fileList


print('Close prices loaded. Now loading open prices.')