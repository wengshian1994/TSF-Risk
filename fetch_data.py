#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 08:57:46 2018

@author: wengshian
"""

from datetime import datetime

import pandas as pd
import quandl

if __name__ == "__main__":
    
    positions = pd.read_excel('TSF_Portfolio.xlsx')
    names = list(positions["Ticker"])
    quandl.ApiConfig.api_key = 'CQRNKPZPnPS_buGnVfaV'
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    # get the table for daily stock prices and,
    # filter the table for selected tickers, columns within a time range
    # set paginate to True because Quandl limits tables API to 10,000 rows per call
    
    #three year stock data
    three_year_stock_data = quandl.get_table('WIKI/PRICES', ticker = names, qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                            date = { 'gte': str(year-3) + "-" + str(month) + "-" + str(day) , 'lte': str(year) + "-" + str(month) + "-" + str(day) }, 
    paginate=True)
    
    three_year_stock_data = three_year_stock_data.pivot(index= 'date',columns='ticker',values='adj_close')
    three_year_stock_data=three_year_stock_data.dropna(axis=1)
    
    
    #one year stock data
    one_year_stock_data = quandl.get_table('WIKI/PRICES', ticker = names, qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                            date = { 'gte': str(year-1) + "-" + str(month) + "-" + str(day) , 'lte': str(year) + "-" + str(month) + "-" + str(day) }, 
    paginate=True)
    
    one_year_stock_data = one_year_stock_data.pivot(index= 'date',columns='ticker',values='adj_close')
    one_year_stock_data=one_year_stock_data.dropna(axis=1)
    
    #three month stock data
    if month == 1:
        new_month = 10
        new_year = year - 1
    
    elif month == 2:
        new_month = 11
        new_year = year - 1
    
    elif month == 3:
        new_month = 12
        new_year = year - 1
    
    else:
        new_month = month - 3
        new_year = year
        
    three_month_stock_data = quandl.get_table('WIKI/PRICES', ticker = names, qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                            date = { 'gte': str(new_year) + "-" + str(new_month) + "-" + str(day) , 'lte': str(year) + "-" + str(month) + "-" + str(day) }, 
    paginate=True)
    
    three_month_stock_data = three_month_stock_data.pivot(index= 'date',columns='ticker',values='adj_close')
    three_month_stock_data=three_month_stock_data.dropna(axis=1)
    
    #get latest data
    latest_data = quandl.get_table('/PRICES', ticker = names, qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                            date = str(year) + "-" + str(month) + "-" + str(day-1), paginate=True)
    
    latest_data = latest_data.pivot(index= 'date',columns='ticker',values='adj_close')
    
    
    
    three_year_stock_data.to_csv("three_year_data")
    one_year_stock_data.to_csv("one_year_data")
    three_month_stock_data.to_csv("three_month_data")


