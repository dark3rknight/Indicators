import os
import math
import pandas as pd
from Moving_Averages import *
from dataPlot import *

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
    multiAxis_LabeledPlot(pricelist,'price',ema[0],str(ema_period[0])+" ema",ema[1],str(ema_period[1])+" ema",trend,'indicator')
    return trend

path = './RTD_test.csv'
read = pd.read_csv(path)
close = list(read.CLOSE)
indicator = ema_crossovers(close[-500:],13,48)