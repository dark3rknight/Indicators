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

def Parabolic_SAR(close, high, low, acceleration_factor, max_acceleration):
	extreme_point = [None,low[1]]
	psar = [None,high[1]]
	trend = [None,"falling"]
	accelation = [None,acceleration_factor]
	change = [None,accelation[1]*(psar[1] - extreme_point[1])]
	initial_psar = [None,None]
	for i in range(2,len(close)):
		if trend[i-1] == "falling":
			ipsar = max(high[i-1],high[i-2],(psar[i-1]-change[i-1]))
		elif trend[i-1] == "rising":
			ipsar = min(low[i-1],low[i-2],(psar[i-1]-change[i-1]))
		initial_psar.append(ipsar)
		if trend[i-1] == "falling":
			if (initial_psar[i] > high[i]):
				newpsar = initial_psar[i]
			else:
				newpsar = extreme_point[i-1]
		if trend[i-1] == "rising":
			if (initial_psar[i] < low[i]):
				newpsar = initial_psar[i]
			else:
				newpsar = extreme_point[i-1]
		psar.append(newpsar)
		if psar[i] > close[i]:
			trend.append("falling")
		else:
			trend.append("rising")
		if trend[i] == "falling":
			extreme_point.append(min(extreme_point[i-1],low[i]))
		else:
			extreme_point.append(max(extreme_point[i-1],high[i]))
		if trend[i] == trend[i-1]:
			if (extreme_point[i] != extreme_point[i-1]) and  (accelation[i-1] < max_acceleration):
				new_acc = accelation[i-1] + acceleration_factor
			else:
				new_acc = accelation[i-1]
		else:
			new_acc = acceleration_factor
		accelation.append(new_acc)
		change.append(accelation[i]*(psar[i]-extreme_point[i]))
	#multiplePlots(close,'price',psar,'PSAR')
	return psar,trend

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

def Technical_Strat():
	path = '../slope_test/'
	files = os.listdir(path)
	list1 = []
	list2 = []
	list3 = []
	list4 = []
	list7 = []
	for i in range(2,len(files)):
		file = files[i]
		read = pd.read_csv(path + file)
		#try:
		close = list(read.CLOSE)
		high =list(read.HIGH)
		low = list(read.LOW)

		returns = list(read.RETURNS)
		slope = OLS_Slope(close, 15)
		psar,psar_trend = Parabolic_SAR(close,high,low,0.02,0.2)
		crossover_1 = ema_crossovers(close,10,20)
		crossover_2 = ema_crossovers(close,20,50)
		crossover_and = []
		for j in range(len(crossover_2)):
			if crossover_2[j] == 1 and crossover_1[j] == 1:
				crossover_and.append(1)
			elif crossover_2[j] == -1 and crossover_1[j] == -1:
				crossover_and.append(-1)
			else:
				crossover_and.append(0)

		counter = 1
		each_trade = []
		each_trade_pl = []
		equity = [0]
		drawdown = [0]
		trades = 0
		old_multiplier = 0
		multi = [0]
		for i in range(1,len(close)):
			if psar_trend[i-1] == 'rising' and slope[i] > 0 and crossover_1[i] > 0: # and indicator2[i] > 0:
				multiplier = 1
			elif psar_trend[i-1] == 'falling' and slope[i] < 0 and crossover_1[i] < 0:
				multiplier = -1
			else:
				multiplier = 0
			cost = 0
			if multiplier != old_multiplier:
				trades = trades + math.fabs(multiplier-old_multiplier)
				cost = math.fabs(multiplier - old_multiplier)*1/10000
			old_multiplier = multiplier
			multi.append(multiplier)
			if is_number(returns[i]):
				new_equity = equity[-1]+returns[i]*multi[i] - cost
			else:
				new_equity = equity[-1] - cost
			equity.append(new_equity)
			drawdown.append(max(equity)-new_equity)
			if psar_trend[i-1] == 'rising':
				psar_tr = 1
			elif psar_trend[i-1] == 'falling':
				psar_tr = -1
			else:
				psar_tr = 0
			if slope[i] > 0:
				slope_tr = 1
			elif slope[i] < 0:
				slope_tr = -1
			else:
				slope_tr = 0
			
			if multi[i] == multi[i-1]:
				counter = counter + 1
			elif (multi[i] != multi[i-1] and multi[i-1] != 0):
				each_trade.append(counter)
				each_trade_pl.append(equity[i-1]-equity[i-counter-1])
				counter = 1
			else:
				counter = 1
			if i == len(close)-1:
				#print('check')
				each_trade.append(counter+1)
				each_trade_pl.append(equity[i]-equity[i-counter-1])

			'''if (len(each_trade_pl)>0):
				list1 = [close[i],equity[i],multi[i],slope_tr,psar_tr,counter,each_trade_pl[-1]]
			else:'''
			#list5 = [high[i],low[i],close[i],multi[i],slope[i],slope_tr,psar[i],psar_tr,crossover_1[i],equity[i],counter]
			#with open('../slope_results/'+file, 'a') as f:
			#	writer = csv.writer(f)
			#	writer.writerow(list5)
		#print(sum(each_trade)/len(each_trade),sum(each_trade_pl),equity[-1],len(each_trade),trades/2)
		number_of_trades = len(each_trade)
		profitable_trades = sum(1 for a in each_trade_pl if a>0)
		loss_trades = sum(1 for a in each_trade_pl if a<0)
		list6 = [file[:-8],equity[-1],max(drawdown),number_of_trades,profitable_trades]
		with open('../slope_results_cost.csv','a') as f:
			writer = csv.writer(f)
			writer.writerow(list6)
		#print(file[:-10],file[-10:-4])
		if file[-10:-4] == '12data':
			list1.append([file[:-10]] + equity)
			print(file[:-8],equity[-1],max(drawdown),len(equity))
		elif file[-10:-4] == '13data':
			list2.append([file[:-10]] + equity)
			print(file[:-8],equity[-1],max(drawdown),len(equity))
		elif file[-10:-4] == '16data':
			list3.append([file[:-10]] + equity)
		list4.append([file[:-8]] + equity)
		list7.append([file[:-8]] + close)
		list7.append([file[:-8]] + equity)
		list7.append([file[:-8]] + multi)
	
	list1 = list(map(list,zip(*list1)))
	for row in list1:
		with open('../12dataresults.csv',"a") as fp:
			wr = csv.writer(fp)
			wr.writerow(row)
	list2 = list(map(list,zip(*list2)))
	for row in list2:
		with open('../13dataresults.csv',"a") as fp:
			wr = csv.writer(fp)
			wr.writerow(row)
'''	list3 = list(map(list,zip(*list3)))
	for row in list3:
		with open('../16dataresults.csv',"a") as fp:
			wr = csv.writer(fp)
			wr.writerow(row)
	list4 = list(map(list,zip(*list4)))
	for row in list4:
		with open('../combined_sloperesults.csv',"a") as fp:
			wr = csv.writer(fp)
			wr.writerow(row)
	list7 = list(map(list,zip(*list7)))		
	for row in list7:
		with open('../make_graph.csv',"a") as fp:
			wr = csv.writer(fp)
			wr.writerow(row)
		#with open('../slope_results.csv','a') as f:
		#	writer = csv.writer(f)
		#	writer.writerow(list1)'''
	#except:
		#	print(path+file)	

Technical_Strat()