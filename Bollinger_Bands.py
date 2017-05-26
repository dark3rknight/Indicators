import os
import csv
import math
import pandas as pd
import numpy as np
from dataPlot import *
from Moving_Averages import *

def bollinger(pricelist,period,number_sigma):
	middle = [pricelist[0]]*(period-1)
	upper_band = [pricelist[0]]*(period-1)
	lower_band = [pricelist[0]]*(period-1)
	for i in range(period-1,len(pricelist)):
		current_sma = sma(pricelist[:i+1],period)
		middle.append(current_sma)
		upper_band.append(current_sma + number_sigma*np.std(pricelist[i-period+1:i+1]))
		lower_band.append(current_sma - number_sigma*np.std(pricelist[i-period+1:i+1]))
	multiplePlots(pricelist,'price',middle,str(period)+' sma',upper_band,None,lower_band)

read = pd.read_csv('./RTD_test.csv')
pricelist = list(read.CLOSE)
bollinger(pricelist[-500:],20,2)

