import os
import csv
import math
import pandas as pd
from dataPlot import *
from Moving_Averages import *

def stochastic(pricelist,high,low,period,fast_smoothening_factor,slow_smoothening_factor):
	fastkArray = [0]*(period-1)
	for i in range(period-1,len(pricelist)):
		fastK = ((pricelist[i]- min(low[i-period+1:i+1]))/(max(high[i-period+1:i+1])-min(low[i-period+1:i+1])))*100
		fastkArray.append(fastK)
	fastdArray = []
	for i in range(len(fastkArray)):
		fastdArray.append(sma(fastkArray[:i],fast_smoothening_factor))
	slowdArray = []
	for i in range(len(fastkArray)):
		slowdArray.append(sma(fastdArray[:i],slow_smoothening_factor))
	multi_subPlot(pricelist,'price',fastkArray,'Fast %K',fastdArray,'Fast %D',slowdArray,'Slow %D')
	return fastdArray

read = pd.read_csv('../RTD_test.csv')
pricelist = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)
oscillator = stochastic(pricelist[-500:],high[-500:],low[-500:], 14,3,5)

