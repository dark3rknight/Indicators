import os
from dataPlot import *
import pandas as pd

def aroon_up_down(pricelist,high,low,aroon_period):
	aroon_up = [None]*aroon_period
	aroon_down = [None]*aroon_period
	aroon_oscillator = [None]*aroon_period
	for i in range(aroon_period,len(pricelist)):
		high_tillToday = high[i-aroon_period:i]
		low_tillToday = low[i-aroon_period:i]
		up = ((aroon_period - (high_tillToday.index(max(high_tillToday))+1))/aroon_period)
		down = ((aroon_period - (low_tillToday.index(min(low_tillToday))+1))/aroon_period)
		aroon_up.append(up)
		aroon_down.append(down)
		aroon_oscillator.append(up-down)
	multi_subPlot(pricelist,'price',aroon_up,'AROON_UP',aroon_down,'AROON_DOWN',aroon_oscillator,'AROON_OSCILLATOR')
	return aroon_oscillator
	
read = pd.read_csv('./RTD_test.csv')
pricelist = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)
aroon_oscillator = aroon_up_down(pricelist[-500:],high[-500:],low[-500:], 50)