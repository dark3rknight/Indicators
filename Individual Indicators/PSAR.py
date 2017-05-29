import os
import csv
import math
import pandas as pd
import numpy as np
from dataPlot import *
from Moving_Averages import *

def Parabolic_SAR(pricelist, high, low, acceleration_factor, max_acceleration):
	extreme_point = [None,low[1]]
	psar = [None,high[1]]
	trend = [None,"falling"]
	accelation = [None,acceleration_factor]
	change = [None,accelation[1]*(psar[1] - extreme_point[1])]
	initial_psar = [None,None]
	for i in range(2,len(pricelist)):
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
		if psar[i] > pricelist[i]:
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
			new_acc = acceleration_factor
		accelation.append(new_acc)
		change.append(accelation[i]*(psar[i]-extreme_point[i]))
	multiplePlots(pricelist,'price',psar,'PSAR')
	return psar,trend


read = pd.read_csv('../RTD_test.csv')
pricelist = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)
psar,trend = Parabolic_SAR(pricelist[-500:], high[-500:], low[-500:], 0.02, 0.2)

