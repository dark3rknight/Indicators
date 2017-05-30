import os
import math
import pandas as pd
import numpy as np
from scipy import stats
from dataPlot import *

def OLS_Slope(pricelist, period):
	OLS_Slope = [0]*(period-1)
	for i in range(period-1,len(pricelist)):
		time_variable = list(range(period))
		OLS_Slope.append(stats.linregress(time_variable,pricelist[i-period+1:i+1]).slope)
	multi_subPlot(pricelist,'price',OLS_Slope,'OLS_Slope')
	return OLS_Slope

path = '../RTD_test_EICHER.csv'
read = pd.read_csv(path)
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
	new_equity = equity[-1]+returns[i]*multiplier
	equity.append(new_equity)
	drawdown.append(max(equity)-new_equity)
print(equity[-1],max(drawdown),trades/2)