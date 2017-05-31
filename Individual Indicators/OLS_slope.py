import os
import math
import pandas as pd
import numpy as np
from scipy import stats
from dataPlot import *
import csv

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def OLS_Slope(pricelist, period):
	OLS_Slope = [0]*(period-1)
	for i in range(period-1,len(pricelist)):
		time_variable = list(range(period))
		OLS_Slope.append(stats.linregress(time_variable,pricelist[i-period+1:i+1]).slope)
	#multi_subPlot(pricelist,'price',OLS_Slope,'OLS_Slope')
	return OLS_Slope

path = '../../data/5 year trending Universe/'
files = os.listdir(path)
for file in files:
	read = pd.read_csv(path + file)
	close = list(read.CLOSE)
	returns = list(read.RETURNS)
	close = close
	returns = returns

	indicator = OLS_Slope(close, 30)

	equity = [0]
	drawdown = [0]
	print(len(indicator),len(returns))
	trades = 0
	old_mutiplier = 0
	multi = [0]
	for i in range(1,len(close)):
		if indicator[i] > 0:
			multiplier = 1
		elif indicator[i] < 0:
			multiplier = -1
		else:
			multiplier = 0
		if multiplier != old_mutiplier:
			trades = trades + 1
		old_mutiplier = multiplier
		if is_number(returns[i]):
			new_equity = equity[-1]+returns[i]*multiplier
		else:
			new_equity = equity[-1]
		equity.append(new_equity)
		drawdown.append(max(equity)-new_equity)
		multi.append(multiplier)
		list1 = [close[i],equity[i],multi[i]]
		with open('./AXIS-14.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(list1)
	print(equity[-1],drawdown[-1])
	
