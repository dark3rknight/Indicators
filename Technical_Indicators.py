import os
import csv
import math
import pandas as pd
import numpy as np
from dataPlot import *

def sma(data, window):
    if len(data) < window:
        return 0
    return sum(data[-window:])/float(window)

def calc_ema(data, window):
    if len(data) <= 2 * window:
        return sma(data[-window:],window)
    multiplier = 2.0 / (window + 1)
    current_ema = sma(data[-window*2:-window], window)
    for value in data[-window:]:
        current_ema = (multiplier * value) + ((1 - multiplier) * current_ema)
    return current_ema

def get_all_EMAs(data, window):
    EMA = [None] * ((window))
    for i in range(window, len(data)):
        EMA.append(calc_ema(data[:i], window))
    return EMA

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
			new_acc = acceleration_factor
		accelation.append(new_acc)
		change.append(accelation[i]*(psar[i]-extreme_point[i]))
	multiplePlots(close,'price',psar,'PSAR')
	return psar,trend

def stochastic(close,high,low,period,fast_smoothening_factor,slow_smoothening_factor):
	fastkArray = [0]*(period-1)
	for i in range(period-1,len(close)):
		fastK = ((close[i]- min(low[i-period+1:i+1]))/(max(high[i-period+1:i+1])-min(low[i-period+1:i+1])))*100
		fastkArray.append(fastK)
	fastdArray = []
	for i in range(len(fastkArray)):
		fastdArray.append(sma(fastkArray[:i],fast_smoothening_factor))
	slowdArray = []
	for i in range(len(fastkArray)):
		slowdArray.append(sma(fastdArray[:i],slow_smoothening_factor))
	multi_subPlot(close,'price',fastkArray,'Fast %K',fastdArray,'Fast %D',slowdArray,'Slow %D')
	return fastdArray

def Relative_Strength_Index(close, period):
    rsi = [None]*(period)
    average_gain = [None]*(period)
    average_loss = [None]*(period)

    for i in range(period,len(close)):
        posSum = 0
        negSum = 0
        if period == i:
            for j in range(period):
                if close[i-j] >= close[i-j-1]:
                    posSum = posSum + close[i-j] - close[i-j-1]
                elif close[i-j] < close[i-j-1]:
                    negSum = negSum + math.fabs(close[i-j] - close[i-j-1])
            posSum = posSum/14
            negSum = negSum/14
        else:
            if close[i-j] >= close[i-j-1]:
                posSum = (average_gain[-1]*13 + (close[i-j] - close[i-j-1]))/14
                negSum = (average_loss[-1]*13)/14
            elif close[i-j] < close[i-j-1]:
                posSum = (average_gain[-1]*13)/14
                negSum = (average_loss[-1]*13 + math.fabs(close[i-j] - close[i-j-1]))/14
        average_gain.append(posSum)
        average_loss.append(negSum)
        
        rs  = average_gain[-1]/average_loss[-1]
        rsiIndic = 100 - (100/(1 + rs))
        rsi.append(rsiIndic)
    multi_subPlot(close,'price',rsi,'rsi')
    return rsi

def Stock_RSI(close,period):
    rsi = Relative_Strength_Index(close,period)
    stochrsi = [None]*(2*period-1)
    for i in range(2*period-1,len(rsi)):
        stochrsi.append((rsi[i] - min(rsi[i-period+1:i+1]))/(max(rsi[i-period+1:i+1])-min(rsi[i-period+1:i+1]))*100)
    multi_subPlot(close,'price',stochrsi,'stoch_rsi')
    return stochrsi

def ema_crossovers(close, period1, period2):
    ema_period = []
    ema_period.append(period1)
    ema_period.append(period2)
    ema_period.sort()
    ema = []
    start_time = ema_period[1]
    for i in range(len(ema_period)):
        ema.append(get_all_EMAs(close,ema_period[i]))
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
    multiAxis_LabeledPlot(close,'price',ema[0],str(ema_period[0])+" ema",ema[1],str(ema_period[1])+" ema",trend,'indicator')
    return trend

def Chande_Momentum_Oscillator(close, period):
    cmo = [None]*(period)
    for i in range(period,len(close)):
        posSum = 0
        negSum = 0    
        for j in range(period):
            if close[i-j] >= close[i-j-1]:
                posSum = posSum + close[i-j] - close[i-j-1]
            elif close[i-j] < close[i-j-1]:
                negSum = negSum + math.fabs(close[i-j] - close[i-j-1])
        cmoIndic = ((posSum - negSum)/(posSum + negSum))*100
        cmo.append(cmoIndic)
    multi_subPlot(close,'price',cmo,'cmo')
    return cmo


def Commodity_Channel_Index(close,high,low,period,number_sigma):
	TP = []
	for i in range(len(close)):
		TP.append((high[i] + low[i] + close[i])/3)
	CCI = [close[0]]*(period)
	for i in range(period,len(close)):
		current_sma = sma(close[:i+1],period)
		TPsum = 0
		for j in range(period):
			TPsum = TPsum + math.fabs(TP[i-j]-current_sma)
		Deviation = TPsum/period
		CCI.append((TP[i]-current_sma)/(0.015*Deviation))
	multi_subPlot(close,'price',CCI,'CCI')
	return CCI

def bollinger(close,period,number_sigma):
	middle = [close[0]]*(period-1)
	upper_band = [close[0]]*(period-1)
	lower_band = [close[0]]*(period-1)
	for i in range(period-1,len(close)):
		current_sma = sma(close[:i+1],period)
		middle.append(current_sma)
		upper_band.append(current_sma + number_sigma*np.std(close[i-period+1:i+1]))
		lower_band.append(current_sma - number_sigma*np.std(close[i-period+1:i+1]))
	multiplePlots(close,'price',middle,str(period)+' sma',upper_band,None,lower_band)
	return middle

def aroon_up_down(close,high,low,aroon_period):
	aroon_up = [None]*aroon_period
	aroon_down = [None]*aroon_period
	aroon_oscillator = [None]*aroon_period
	for i in range(aroon_period,len(close)):
		high_tillToday = high[i-aroon_period:i]
		low_tillToday = low[i-aroon_period:i]
		up = ((aroon_period - (high_tillToday.index(max(high_tillToday))+1))/aroon_period)
		down = ((aroon_period - (low_tillToday.index(min(low_tillToday))+1))/aroon_period)
		aroon_up.append(up)
		aroon_down.append(down)
		aroon_oscillator.append(up-down)
	multi_subPlot(close,'price',aroon_up,'AROON_UP',aroon_down,'AROON_DOWN',aroon_oscillator,'AROON_OSCILLATOR')
	return aroon_oscillator

def adx(close,high,low,smoothening_factor):
	DM_pos = [None]
	DM_neg = [None]
	ATR = [None]
	for i in range(1,len(close)):
		if high[i] > high[i-1]:
			DM_pos.append(high[i] - high[i-1])
		else:
			DM_pos.append(0)
		if low[i-1] > low[i]:
			DM_neg.append(low[i-1] - low[i])
		else:
			DM_neg.append(0)
		ATR.append(max(math.fabs(high[i]-low[i]),math.fabs(high[i]-close[i-1]),math.fabs(low[i]-close[i-1])))
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
	multi_subPlot(close,'price',DI_pos,'+DI',DI_neg,'-DI',ADX,'ADX')
	return ADX


read = pd.read_csv('./RTD_test.csv')
close = list(read.CLOSE)
high = list(read.HIGH)
low = list(read.LOW)


psar,trend = Parabolic_SAR(close[-500:], high[-500:], low[-500:], 0.02, 0.2)
stochastic_Oscillator = stochastic(close[-500:],high[-500:],low[-500:], 14,3,5)
rsi = Relative_Strength_Index(close[-500:], 30)
stochrsi = Stock_RSI(close[-500:], 30)
ema = ema_crossovers(close[-500:],13,48)
cmo = Chande_Momentum_Oscillator(close[-500:], 30)
cci = Commodity_Channel_Index(close[-500:],high[-500:],low[-500:],20,2)
sma = bollinger(close[-500:],20,2)
aroon = aroon_up_down(close[-500:],high[-500:],low[-500:], 50)
ADX = adx(close[-500:],high[-500:],low[-500:], 10)

