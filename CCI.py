import os
import csv
import math
import pandas as pd
import numpy as np
from dataPlot import *
from Moving_Averages import *

def cci(pricelist,high,low,period,number_sigma):
	TP = []
	for i in range(len(pricelist)):
		TP.append((high[i] + low[i] + pricelist[i])/3)
	CCI = [pricelist[0]]*(period)
	for i in range(period,len(pricelist)):
		current_sma = sma(pricelist[:i+1],period)
		TPsum = 0
		for j in range(period):
			TPsum = TPsum + math.fabs(TP[i-j]-current_sma)
		Deviation = TPsum/period
		print(Deviation)
		CCI.append((TP[i]-current_sma)/(0.015*Deviation))
	print(len(CCI))
	multi_subPlot(pricelist,'price',CCI,'CCI')

read = pd.read_csv('./RTD_test.csv')
pricelist = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)
cci(pricelist[-500:],high[-500:],low[-500:],20,2)

