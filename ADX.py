import os
import csv
import math
import pandas as pd
from dataPlot import *

def adx(pricelist,high,low,smoothening_factor):
	DM_pos = [None]
	DM_neg = [None]
	ATR = [None]
	for i in range(1,len(pricelist)):
		if high[i] > high[i-1]:
			DM_pos.append(high[i] - high[i-1])
		else:
			DM_pos.append(0)
		if low[i-1] > low[i]:
			DM_neg.append(low[i-1] - low[i])
		else:
			DM_neg.append(0)
		ATR.append(max(math.fabs(high[i]-low[i]),math.fabs(high[i]-pricelist[i-1]),math.fabs(low[i]-pricelist[i-1])))
	Smoothened_ATR = [0]*(smoothening_factor+1)
	Smoothened_DM_pos = [0]*(smoothening_factor+1)
	Smoothened_DM_neg = [0]*(smoothening_factor+1)
	DI_pos = [None]*(smoothening_factor+1)
	DI_neg = [None]*(smoothening_factor+1)
	Current_ADX = [None]*(smoothening_factor+1)
	for i in range(smoothening_factor+1,len(ATR)):
		if i == smoothening_factor + 1:
			Current_smooth_ATR = sum(ATR[-smoothening_factor+i:i],0.0)/len(ATR[i-smoothening_factor:i])
			Current_smooth_DM_pos = sum(DM_pos[-smoothening_factor+i:i],0.0)/len(DM_pos[i-smoothening_factor:i])
			Current_smooth_DM_neg = sum(DM_neg[-smoothening_factor+i:i],0.0)/len(DM_neg[i-smoothening_factor:i])
		else:
			Current_smooth_ATR = (smoothening_factor-1)*Smoothened_ATR[-1]/smoothening_factor + ATR[i]
			Current_smooth_DM_pos = (smoothening_factor-1)*Smoothened_DM_pos[-1]/smoothening_factor + DM_pos[i]
			Current_smooth_DM_neg = (smoothening_factor-1)*Smoothened_DM_neg[-1]/smoothening_factor + DM_neg[i]
		Smoothened_ATR.append(Current_smooth_ATR)
		Smoothened_DM_pos.append(Current_smooth_DM_pos)
		Smoothened_DM_neg.append(Current_smooth_DM_neg)
		Current_DI_pos = Current_smooth_DM_pos/Current_smooth_ATR*100
		Current_DI_neg = Current_smooth_DM_neg/Current_smooth_ATR*100
		DI_pos.append(Current_DI_pos)
		DI_neg.append(Current_DI_neg)
		if DI_neg == 0  and DI_pos == 0:
			Current_ADX.append(0)
		else:
			Current_ADX.append(math.fabs((Current_DI_pos - Current_DI_neg))/(Current_DI_pos + Current_DI_neg)*100)
	ADX = [None]*(2*smoothening_factor + 1)
	for i in range(2*smoothening_factor + 1, len(Current_ADX)):
		if i == 2*smoothening_factor + 1:
			ADX.append(sum(Current_ADX[-smoothening_factor+i:i],0.0)/len(Current_ADX[-smoothening_factor+i:i]))
		else:
			ADX.append(((smoothening_factor-1)*ADX[-1] + Current_ADX[i])/smoothening_factor)
	multi_subPlot(pricelist,'price',DI_pos,'+DI',DI_neg,'-DI',ADX,'ADX')
	return ADX

read = pd.read_csv('./RTD_test.csv')
pricelist = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)
ADX = adx(pricelist[-500:],high[-500:],low[-500:], 10)

