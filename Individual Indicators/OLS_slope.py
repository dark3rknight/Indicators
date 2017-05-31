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
	except:
		return False

def OLS_Slope(pricelist, period):
	OLS_Slope = [0]*(period)
	for i in range(period,len(pricelist)):
		time_variable = list(range(period))
		OLS_Slope.append(stats.linregress(time_variable,pricelist[i-period:i]).slope)
	#multi_subPlot(pricelist,'price',OLS_Slope,'OLS_Slope')
	return OLS_Slope

path = '../slope_test/'
files = os.listdir(path)
for file in files:
	read = pd.read_csv(path + file)
	try:
		close = list(read.CLOSE)
		returns = list(read.RETURNS)
		
		indicator = OLS_Slope(close, 30)

		equity = [0]
		drawdown = [0]
		trades = 0
		old_mutiplier = 0
		multi = [0]
		for i in range(1,len(close)-1):
			if indicator[i] > 0:
				multiplier = 1
			elif indicator[i] < 0:
				multiplier = -1
			else:
				multiplier = 0
			if multiplier != old_mutiplier:
				trades = trades + 1
			old_mutiplier = multiplier
			multi.append(multiplier)
			if is_number(returns[i]):
				new_equity = equity[-1]+returns[i]*multi[i]
			else:
				new_equity = equity[-1]
			equity.append(new_equity)
			drawdown.append(max(equity)-new_equity)
			list1 = [close[i],equity[i],multi[i]]
			
			with open('../slope_results/'+file, 'a') as f:
				writer = csv.writer(f)
				writer.writerow(list1)
		list1 = [file,equity[-1],max(drawdown)]
		with open('../slope_results.csv','a') as f:
			writer = csv.writer(f)
			writer.writerow(list1)
		print(file,equity[-1],max(drawdown))
	except:
		print(path+file)	