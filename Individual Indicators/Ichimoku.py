import os
import csv
import math
import pandas as pd
import numpy as np
from dataPlot import *
from Moving_Averages import *

def ichimoku_clouds(close, high, low, period1, period2):
	conversion_line = [None]*(period1-1)
	base_line = [None]*(period2-1)
	Leading_SpanA = [close[0]]*(2*period2-1)
	Leading_SpanB = [close[0]]*(3*period2 - 1)
	lagging_close = [None]*(period2-1)
	for i in range(len(close)):
		if i >= (period1-1):
			highest_high = max(high[i-period1+1:i+1])
			lowest_low = min(low[i-period1+1:i+1])
			add_conversion = (highest_high + lowest_low)/2
			conversion_line.append((highest_high+lowest_low)/2)
		if i >= (period2-1):
			highest_high = max(high[i-period2+1:i+1])
			lowest_low = min(low[i-period2+1:i+1])
			add_base = (highest_high + lowest_low)/2
			base_line.append((highest_high+lowest_low)/2)
			lagging_close.append(close[i-period2+1])
		if i >= (2*period2-1) and len(Leading_SpanA) < len(close):
			Leading_SpanA.append((add_conversion+add_base)/2)
		if i >= (3*period2 - 1):
			highest_high = max(high[i-3*period2+1:i-period2+1])
			lowest_low = min(low[i-3*period2+1:i-period2+1])
			Leading_SpanB.append((highest_high+lowest_low)/2)
	multiple_coloredPlots(close,'price',conversion_line,'conversion_line',base_line,'base_line',Leading_SpanA,'Leading Span A',Leading_SpanB,'Leading Span B',lagging_close,'Lagging Close')

def multiple_coloredPlots(vals1, label1, vals2 = None, label2 = None, vals3 = None, label3 = None, vals4 = None, label4 = None, vals5 = None, label5 = None, vals6 = None, label6 = None):
    plt.close()
    x = list(range(len(vals5)))
    plt.plot(vals1, color = 'black', linewidth = 0.6, label = label1)
    if vals2 != None:
        plt.plot(vals2, color = 'salmon', linewidth = 0.6, label = label2)
    if vals3 != None:
        plt.plot(vals3, color = 'blue', linewidth = 0.6, label = label3)
    if vals4 != None:
        plt.plot(vals4, color = 'green', linewidth = 0.3, label = label4)
    if vals5 !=None:
    	plt.plot(vals5, color = 'darkred', linewidth = 0.3, label = label5)
    if vals6 != None:
    	plt.plot(vals6, color = 'green', linewidth = 0.6, label = label6)
    x = np.array(x)
    vals4 = np.array(vals4)
    vals5 = np.array(vals5)
    plt.fill_between(x,vals4,vals5, where = vals4 > vals5, facecolor = 'green' ,interpolate = True)
    plt.fill_between(x,vals4,vals5, where = vals5 > vals4, facecolor = 'red' ,interpolate = True)
    
    plt.grid(True)
    plt.legend()
    plt.show()

read = pd.read_csv('../RTD_test.csv')
close = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)
signal = ichimoku_clouds(close[-500:],high[-500:],low[-500:], 9 ,26)
