import os
import math
import pandas as pd
from dataPlot import *

def Relative_Strength_Index(pricelist, period):
    rsi = [None]*(period)
    average_gain = [None]*(period)
    average_loss = [None]*(period)

    for i in range(period,len(pricelist)):
        posSum = 0
        negSum = 0
        if period == i:
            for j in range(period):
                if pricelist[i-j] >= pricelist[i-j-1]:
                    posSum = posSum + pricelist[i-j] - pricelist[i-j-1]
                elif pricelist[i-j] < pricelist[i-j-1]:
                    negSum = negSum + math.fabs(pricelist[i-j] - pricelist[i-j-1])
            posSum = posSum/14
            negSum = negSum/14
        else:
            if pricelist[i-j] >= pricelist[i-j-1]:
                posSum = (average_gain[-1]*13 + (pricelist[i-j] - pricelist[i-j-1]))/14
                negSum = (average_loss[-1]*13)/14
            elif pricelist[i-j] < pricelist[i-j-1]:
                posSum = (average_gain[-1]*13)/14
                negSum = (average_loss[-1]*13 + math.fabs(pricelist[i-j] - pricelist[i-j-1]))/14
        average_gain.append(posSum)
        average_loss.append(negSum)
        
        rs  = average_gain[-1]/average_loss[-1]
        rsiIndic = 100 - (100/(1 + rs))
        rsi.append(rsiIndic)
    multi_subPlot(pricelist,'price',rsi,'rsi')
    return rsi

path = './RTD_test.csv'
read = pd.read_csv(path)
close = list(read.CLOSE)
indicator = Relative_Strength_Index(close[-500:], 30)