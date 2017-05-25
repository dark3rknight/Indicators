import os
import math
import matplotlib.pyplot as plt
import pandas as pd

def sma(data, window):
        if len(data) < window:
            return None
        return sum(data[-window:]) / float(window)

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

def ma_crossovers(pricelist, period1, period2):
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
    plotData(pricelist,ema[0],ema[1],trend)

def plotData(vals1, vals2, vals3, vals4 = None):
    plt.close()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(vals1, color = 'darkred', linewidth = 0.6)
    ax1.plot(vals2, color = 'blue', linewidth = 0.6)
    ax1.plot(vals3, color = 'green', linewidth = 0.6)
    ax4 = ax1.twinx()
    ax4.plot(vals4, color = 'salmon', linewidth = 0.6)
    plt.show()

path = '../WMstraddle/banknifty 25-01 15.csv'
read = pd.read_csv(path)
close = list(read.CLOSE)
ma_crossovers(close[-500:-200],14,28)