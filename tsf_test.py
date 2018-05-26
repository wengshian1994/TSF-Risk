from datetime import datetime

import numpy as np
import pandas as pd
import quandl

def make_returns(data):
    
    for i in range(1,len(data)):
        data.iloc[i-1] = data.iloc[i]/data.iloc[i-1] - 1
    data = data.drop(len(data)-1,0)
    return data

if __name__ == "__main__":
    # read respective files
    positions = pd.read_excel('TSF_Portfolio.xlsx')
    three_year_data = pd.read_csv('three_year_data')
    one_year_data = pd.read_csv('one_year_data')
    three_month_data = pd.read_csv('three_month_data')
    latest_price = three_month_data.iloc[len(three_month_data)-1]
    
    #process data
    # 1. Make returns
    three_year_data = make_returns(three_year_data.drop('date', 1))
    one_year_data = make_returns(one_year_data.drop('date', 1))
    three_month_data = make_returns(three_month_data.drop('date', 1))
    
    # 2. Make cov matrix/ mean returns
    # Cov Matrix
    three_year_cov = three_year_data.cov()
    one_year_cov = one_year_data.cov()
    three_month_cov = three_month_data.cov()
    #Mean vectors
    three_year_mean = np.array(three_year_data.mean(axis=0))
    one_year_mean = np.array(one_year_data.mean(axis=0))
    three_month_mean = np.array(three_month_data.mean(axis=0))
    
    
    # 3. Get the weights
    names = list(positions["Ticker"])
    lots = list(positions["Quantity"])
    sector = list(positions["Industry"])
    weights = list(positions["P_Weight"])
    stock_names = list(three_year_cov)
    portfolio_dict = {}
    for i in range(len(names)):
        portfolio_dict[names[i]] = lots[i], sector[i], weights[i]
    
    #want to order the arrays for cov matrix
    lots = list()
    sectors = list()
    p_weights = list()
    for i in range(len(stock_names)):
        stock = stock_names[i]
        lot , industry, weight = portfolio_dict[stock]
        lots.append(lot)
        sectors.append(industry)
        p_weights.append(weight)
    
        
    
    

#date = { 'gte': str(year-1) + "-" + str(month) + "-" + str(day), 'lte': str(year) + "-" + str(month) + "-" + str(day)}