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
from datetime import datetime


#Download all stock files
#save_path = '/stock_data'

positions = pd.read_excel('TSF_Portfolio.xlsx')
names = list(positions["Ticker"])

for i in range(len(names)):
    print(i)
    ticker = names[i]
    url = 'https://stooq.com/q/d/l/?s=' + ticker + ".US&i=d"
    r = requests.get(url, allow_redirects=True)
    open("stock_data/" + ticker + ".txt", 'wb').write(r.content)

# 1. Load stock data into a dataframe and prepare for analysis


#1.1 Load close prices
# Set the directory to the directory where the stock data is stored
os.chdir("stock_data")

# prepare the fileList and dataframe for stock data
fileList = []
df = pd.DataFrame()
three_month_df = pd.DataFrame()
one_year_df = pd.DataFrame()
three_year_df = pd.DataFrame()

# set number of past days to load into dataframe

three_year_days = 252*3
one_year_days = 252
three_month_days = 63

# read all file names
for files in glob.glob("*.txt"):
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
    ticker = file[:-4]
    frame_three_year = pd.read_table(file, sep = ',', index_col = 0).tail(three_year_days)
    frame_one_year = pd.read_table(file, sep = ',', index_col = 0).tail(one_year_days)
    frame_three_month = pd.read_table(file, sep = ',', index_col = 0).tail(three_month_days)
    #print(frame)
    if len(frame_three_month) == 0:
        continue
    three_month_df[ticker] = frame_three_year["Close"]
    one_year_df[ticker] = frame_one_year["Close"]
    three_year_df[ticker] = frame_three_month["Close"]

# change row names to stock ticker symbols
#df.index = fileList


print('Close prices loaded. Now loading open prices.')
