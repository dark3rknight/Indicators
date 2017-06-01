import os
import math
import pandas as pd
import numpy as np
from scipy import stats
from dataPlot import *
import csv

from Moving_Averages import *

def ema_crossovers(pricelist, period1, period2):
    ema_period = []
    ema_period.append(period1)
    ema_period.append(period2)
    ema_period.sort()
    ema = []
    start_time = ema_period[1]
    for i in range(len(ema_period)):
        ema.append(get_all_EMAs(pricelist,ema_period[i]))
    trend = []
    for i in range(len(ema[0])):
        if ema[0][i] == None or ema[-1][i] == None:
            trend.append(0) 
        elif ema[0][i] > ema[-1][i]:
            trend.append(1)
        elif ema[0][i] < ema[-1][i]:
            trend.append(-1)
        else:
            trend.append(0)
    #multiAxis_LabeledPlot(pricelist,'price',ema[0],str(ema_period[0])+" ema",ema[1],str(ema_period[1])+" ema",trend,'indicator')
    return trend

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
		
		slope = OLS_Slope(close, 15)
		crossover1 = ema_crossovers(close,10,20)
		crossover2 = ema_crossovers(close,20,50)
		crossover_and = []
		for i in range(len(crossover2)):
			if crossover2[i] == 1 or crossover1[i] == 1:
				crossover_and.append(1)
			elif crossover2[i] == -1 or crossover1[i] == -1:
				crossover_and.append(-1)
			else:
				crossover_and.append(0)
		#ndicator2 = OLS_Slope(close, 60)
		print(len(close),len(slope),len(crossover_and))
		equity = [0]
		drawdown = [0]
		trades = 0
		old_mutiplier = 0
		multi = [0]

		for i in range(1,len(close)):
			if slope[i] > 0 and crossover_and[i] > 0 : # and indicator2[i] > 0:
				multiplier = 1
			elif slope[i] < 0 and crossover_and[i] < 0  : # and indicator2[i] < 0 :
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
			list1 = [close[i],equity[i],multi[i],slope[i],crossover1[i],crossover2[i],crossover_and[i]]
			
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