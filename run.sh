#!/bin/bash

DATE=$1

py combine_data_lim.py $DATE
py tsf_var.py
