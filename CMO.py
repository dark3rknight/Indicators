import os
import math
import pandas as pd
from Moving_Averages import *
from dataPlot import *

def Chande_Momentum_Oscillator(pricelist, period):
    cmo = [None]*(period)
    for i in range(period,len(pricelist)):
        posSum = 0
        negSum = 0    
        for j in range(period):
            if pricelist[i-j] >= pricelist[i-j-1]:
                posSum = posSum + pricelist[i-j] - pricelist[i-j-1]
            elif pricelist[i-j] < pricelist[i-j-1]:
                negSum = negSum + math.fabs(pricelist[i-j] - pricelist[i-j-1])
        cmoIndic = ((posSum - negSum)/(posSum + negSum))*100
        cmo.append(cmoIndic)
    print(len(cmo))
    multi_subPlot(pricelist,'price',cmo,'cmo')
    return cmo

path = './RTD_test.csv'
read = pd.read_csv(path)
close = list(read.CLOSE)
indicator = Chande_Momentum_Oscillator(close[-500:], 30)