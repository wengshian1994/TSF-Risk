#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:12:55 2018

@author: wengshian
"""

fetch_data.py:
To fetch the data from quandl. However, quandl has some data problems.

tsf_test.py:
Create a csv var file of 95%,99% (3M, 1Y, 3Y). Using parameric VaR method.
Aim to create a csv file and then use RMarkdown to take the data.

combine_test.py:
Fetch data from stooq (to overcome the quandl data problems). Download the
stock data files from stooq and then save it into a csv file.

Order to run the scripts:
1. combine_data.py
2. tsf_test.py
3. TSF Risk.Rmd

#### Next files descriptions are for monthly data
combine_data_lim.py:
Save data and separate them to three years, one year and 3 months data prior to limit date argument(exclusive)

tsf_var.py:
Create a csv var file of 95%,99% (3M, 1Y, 3Y). Using parameric VaR method.
Aim to create a csv file and then use RMarkdown to take the data.

TSF_Risk_Monthly:
Plot the change in VaR every month using data from 3 years, one year and 3 months prior to limit date


To run using bash script(Mac or Linux):
chmod +x run.sh #if never done before
./run.sh [date limit in format yyyy-mm-dd (exclusive)]
e.g. If want to analyze data up to June 2018, then :
./run.sh 2018-07-01 - This will run usig data up to 30th June

To run using powershell (Windows):
./run.ps1 [date limit in format yyyy-mm-dd (exclusive)]
e.g. If want to analyze data up to June 2018, then :
./run.ps1 2018-07-01 - This will run usig data up to 30th June


These will
