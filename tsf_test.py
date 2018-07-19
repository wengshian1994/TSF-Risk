from datetime import datetime
from scipy.stats import norm

import sys
import math
import numpy as np
import pandas as pd
import quandl
import matplotlib.pyplot as plt

def make_returns(data):
    for i in range(1,len(data)):
        data.iloc[i-1] = np.log(data.iloc[i]/data.iloc[i-1])
    data = data[:len(data)-2]
    return data

def make_arrays(stock_names, portfolio_dict):
    lots = list()
    sectors = list()
    p_weights = list()
    for i in range(len(stock_names)):
        stock = stock_names[i]
        lot , industry, weight = portfolio_dict[stock]
        lots.append(lot)
        sectors.append(industry)
        p_weights.append(weight)
    return lots, sectors, p_weights


if __name__ == "__main__":
    # read respective files
    save_into = sys.argv[1]
    print(save_into)

    positions = pd.read_excel('TSF_Portfolio.xlsx')
    three_year_data = pd.read_csv('three_year_data')
    one_year_data = pd.read_csv('one_year_data')
    three_month_data = pd.read_csv('three_month_data')
    latest_price = three_month_data.iloc[len(three_month_data)-1]
    #remove the NANs and replace it with column means

    three_year_data= three_year_data.fillna(three_year_data.mean())
    one_year_data= one_year_data.fillna(one_year_data.mean())
    three_month_data= three_month_data.fillna(three_month_data.mean())

    #create weekly data (every 5 days)
    three_year_weekly = three_year_data.iloc[::5, :]
    one_year_weekly = one_year_data.iloc[::5, :]
    three_month_weekly = three_month_data.iloc[::5, :]

    #process data
    # 1. Make returns
    three_year_data = make_returns(three_year_data.drop('Date', 1))
    one_year_data = make_returns(one_year_data.drop('Date', 1))
    three_month_data = make_returns(three_month_data.drop('Date', 1))

    three_year_weekly = make_returns(three_year_weekly.drop('Date', 1))
    one_year_weekly = make_returns(one_year_weekly.drop('Date', 1))
    three_month_weekly = make_returns(three_month_weekly.drop('Date', 1))

    # 2. Make cov matrix/ mean returns
    # Cov Matrix
    three_year_cov = three_year_data.cov()
    one_year_cov = one_year_data.cov()
    three_month_cov = three_month_data.cov()

    three_year_weekly_cov = three_year_weekly.cov()
    one_year_weekly_cov = one_year_weekly.cov()
    three_month_weekly_cov = three_month_weekly.cov()

    #Mean vectors
    three_year_mean = np.array(three_year_data.mean(axis=0))
    one_year_mean = np.array(one_year_data.mean(axis=0))
    three_month_mean = np.array(three_month_data.mean(axis=0))

    three_year_weekly_mean = np.array(three_year_weekly.mean(axis=0))
    one_year_weekly_mean = np.array(one_year_weekly.mean(axis=0))
    three_month_weekly_mean = np.array(three_month_weekly.mean(axis=0))


    # 3. Get the weights
    names = list(positions["Ticker"])
    lots = list(positions["Quantity"])
    sector = list(positions["Industry"])
    weights = list(positions["P_Weight"])
    stock_names_three_year = list(three_year_cov)
    stock_names_one_year = list(one_year_cov)
    stock_names_three_month = list(three_month_cov)
    portfolio_dict = {}
    for i in range(len(names)):
        portfolio_dict[names[i]] = lots[i], sector[i], weights[i]

    print(portfolio_dict)

    #want to order the arrays for cov matrix
    three_year_lots, three_year_sectors, three_year_p_weights = make_arrays(stock_names_three_year,portfolio_dict)
    one_year_lots, one_year_sectors, one_year_p_weights = make_arrays(stock_names_one_year,portfolio_dict)
    three_month_lots, three_month_sectors, three_month_p_weights = make_arrays(stock_names_three_month,portfolio_dict)
    #rescale weights (can remove this later on)
    #three_year_p_weights = np.array(three_year_p_weights)/sum(three_year_p_weights)
    #one_year_p_weights = np.array(one_year_p_weights)/sum(one_year_p_weights)
    #three_month_p_weights = np.array(three_month_p_weights)/sum(three_month_p_weights)

    # 4. Get respective means and sigmas
    three_year_mu = (1+np.dot(three_year_p_weights,three_year_mean))**5 -1
    three_year_sigma = math.sqrt(np.dot(np.dot(three_year_p_weights,three_year_cov).transpose(),three_year_p_weights))*math.sqrt(5)

    one_year_mu = (1+np.dot(one_year_p_weights,one_year_mean))**5 - 1
    one_year_sigma = math.sqrt(np.dot(np.dot(one_year_p_weights,one_year_cov).transpose(),one_year_p_weights))*math.sqrt(5)

    three_month_mu = (1+np.dot(three_month_p_weights,three_month_mean))**5 - 1
    three_month_sigma = math.sqrt(np.dot(np.dot(three_month_p_weights,three_month_cov).transpose(),three_month_p_weights))*math.sqrt(5)

    #weekly
    three_year_weekly_mu = (np.dot(three_year_p_weights,three_year_weekly_mean)) -1
    three_year_weekly_sigma = math.sqrt(np.dot(np.dot(three_year_p_weights,three_year_weekly_cov).transpose(),three_year_p_weights))

    one_year_weekly_mu = (np.dot(one_year_p_weights,one_year_weekly_mean)) -1
    one_year_weekly_sigma = math.sqrt(np.dot(np.dot(one_year_p_weights,one_year_weekly_cov).transpose(),one_year_p_weights))

    three_month_weekly_mu = (np.dot(three_month_p_weights,three_month_weekly_mean)) -1
    three_month_weekly_sigma = math.sqrt(np.dot(np.dot(three_month_p_weights,three_month_weekly_cov).transpose(),three_month_p_weights))

    # 5. Calculate VaR (Assume log normal distribution of returns)
    ninety_five_VaR_Three_Year = norm.ppf(0.05,loc=three_year_mu,scale=three_year_sigma)
    ninety_nine_VaR_Three_Year = norm.ppf(0.01,loc=three_year_mu,scale=three_year_sigma)

    ninety_five_VaR_One_Year = norm.ppf(0.05,loc=one_year_mu,scale=one_year_sigma)
    ninety_nine_VaR_One_Year = norm.ppf(0.01,loc=one_year_mu,scale=one_year_sigma)

    ninety_five_VaR_Three_Month = norm.ppf(0.05,loc=three_month_mu,scale=three_month_sigma)
    ninety_nine_VaR_Three_Month = norm.ppf(0.01,loc=three_month_mu,scale=three_month_sigma)
    VaR_array = np.array([ninety_five_VaR_Three_Year,ninety_nine_VaR_Three_Year,ninety_five_VaR_One_Year,ninety_nine_VaR_One_Year,ninety_five_VaR_Three_Month,ninety_nine_VaR_Three_Month])

    #Weekly VaR
    ninety_five_weekly_VaR_Three_Year = norm.ppf(0.05,loc=three_year_weekly_mu,scale=three_year_weekly_sigma)
    ninety_nine_weekly_VaR_Three_Year = norm.ppf(0.01,loc=three_year_weekly_mu,scale=three_year_weekly_sigma)

    ninety_five_weekly_VaR_One_Year = norm.ppf(0.05,loc=one_year_weekly_mu,scale=one_year_weekly_sigma)
    ninety_nine_weekly_VaR_One_Year = norm.ppf(0.01,loc=one_year_weekly_mu,scale=one_year_weekly_sigma)

    ninety_five_weekly_VaR_Three_Month = norm.ppf(0.05,loc=three_month_weekly_mu,scale=three_month_weekly_sigma)
    ninety_nine_weekly_VaR_Three_Month = norm.ppf(0.01,loc=three_month_weekly_mu,scale=three_month_weekly_sigma)
    Weekly_VaR_array = np.array([ninety_five_weekly_VaR_Three_Year,ninety_nine_weekly_VaR_Three_Year,ninety_five_weekly_VaR_One_Year,ninety_nine_weekly_VaR_One_Year,ninety_five_weekly_VaR_Three_Month,ninety_nine_weekly_VaR_Three_Month])


    #Save dataframe into excel sheet
    VaR_dataframe = pd.DataFrame()
    VaR_dataframe["VaR"] = np.power(math.e,VaR_array)-1
    VaR_dataframe.rename(index={0:'95 % VaR (Three Years)',1:'99 % VaR (Three Years)',2:'95 % VaR (One Year)',\
                                3:'99 % VaR (One Year)',4:'95 % VaR (Three Months)',5:'99 % VaR (Three Months)'}, inplace=True)
    VaR_dataframe.to_csv("VaR_Numbers", sep='\t')

    #make weekly dataframe
    Weekly_VaR_dataframe = pd.DataFrame()
    Weekly_VaR_dataframe["VaR"] = np.power(math.e,Weekly_VaR_array)-1
    Weekly_VaR_dataframe.rename(index={0:'95 % VaR (Three Years)',1:'99 % VaR (Three Years)',2:'95 % VaR (One Year)',\
                                3:'99 % VaR (One Year)',4:'95 % VaR (Three Months)',5:'99 % VaR (Three Months)'}, inplace=True)
    Weekly_VaR_dataframe.to_csv("VaR_Numbers(weekly)", sep='\t')

    #portfolio history (Making it weekly returns)
    three_year_port_history = pd.DataFrame((1+np.dot(three_year_p_weights,three_year_data.transpose()))**5 - 1)
    one_year_port_history = pd.DataFrame((1+np.dot(one_year_p_weights,one_year_data.transpose()))**5 - 1)
    three_month_port_history = pd.DataFrame((1+np.dot(three_month_p_weights,three_month_data.transpose()))**5 - 1)

    #Save portfolio history into excel sheet
    three_year_port_history.to_csv("Three_Year_Port_History", sep='\t')
    one_year_port_history.to_csv("One_Year_Port_History", sep='\t')
    three_month_port_history.to_csv("Three_Month_Port_History", sep='\t')

    #6. Get names of stocks not in analysis
    not_in_list = names
    for name in list(three_year_data):
        not_in_list.remove(name)
    not_in_list = pd.DataFrame(np.array(not_in_list))
    not_in_list.to_csv("Not_In",sep='\t')
