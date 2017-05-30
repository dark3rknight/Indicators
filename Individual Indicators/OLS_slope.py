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
	print(len(OLS_Slope))
	multi_subPlot(pricelist,'price',OLS_Slope,'OLS_Slope')

path = '../RTD_test.csv'
read = pd.read_csv(path)
close = list(read.CLOSE)
indicator = OLS_Slope(close[200:1000], 30)
