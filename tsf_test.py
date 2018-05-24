from datetime import datetime

import pandas as pd
import quandl

def make_returns(data):
    
    for i in range(1,len(data)):
        data.iloc[i-1] = data.iloc[i]/data.iloc[i-1] - 1
    data = data.drop(len(data)-1,0)
    return data

if __name__ == "__main__":
    positions = pd.read_excel('TSF_Portfolio.xlsx')
    three_year_data = pd.read_csv('three_year_data')
    one_year_data = pd.read_csv('one_year_data')
    three_month_data = pd.read_csv('three_month_data')
    
    #process data
    three_year_data = make_returns(three_year_data.drop('date', 1))
    one_year_data = make_returns(one_year_data.drop('date', 1))
    three_month_data = make_returns(three_month_data.drop('date', 1))
    
    names = list(positions["Ticker"])
    lots = list(positions["Lots"])
    sector = list(positions["Industry"])
    
    portfolio_dict = {}
    for i in range(len(names)):
        portfolio_dict[names[i]] = lots[i], sector[i]
    

#date = { 'gte': str(year-1) + "-" + str(month) + "-" + str(day), 'lte': str(year) + "-" + str(month) + "-" + str(day)}