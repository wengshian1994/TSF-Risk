#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run this script to fetch data of names not in \stock_data
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

if __name__ == "__main__":
    
    to_add = pd.read_csv("Not_In",sep='\t').iloc[:,1]
    for i in range(len(to_add)):
        print(i)
        ticker = to_add[i]
        url = 'https://stooq.com/q/d/l/?s=' + ticker + ".US&i=d"
        r = requests.get(url, allow_redirects=True)
        open("stock_data/" + ticker + ".txt", 'wb').write(r.content)