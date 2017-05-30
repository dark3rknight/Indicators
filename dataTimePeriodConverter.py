import math
import pandas as pd
import csv

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def data_cleaning(tValue,date,time,popen,high,low,close):
	date.reverse()
	time.reverse()
	close.reverse()
	previous_date = date[0]
	formatted_open = []
	formatted_high = []
	formatted_low = []
	formatted_close = []
	formatted_date = []
	formatted_time =[]
	
	logreturns =[0]
	returns =[0]
	counter = 0
	for i in range(len(date)-tValue):
		if i == counter:
			formatted_open.append(popen[i])
			flag = 0
			maximum = high[i]
			minimum = low[i]
			for j in range(tValue):
				maximum = max(close[i+j],maximum)
				minimum = min(close[i+j],minimum)
				flag = flag + 1
			counter = i + flag
			formatted_date.append(date[counter - 1])
			formatted_time.append(time[counter - 1])
			formatted_close.append(close[counter - 1])
			formatted_high.append(maximum)
			formatted_low.append(minimum)
	for i in range(1,len(formatted_close)):
		ret = (float(formatted_close[i]) - float(formatted_close[i-1]))/float(formatted_close[i-1])
		returns.append(ret)
		logreturns.append(math.log(1+ret))
	rows = zip(formatted_date,formatted_time,formatted_open,formatted_high,formatted_low,formatted_close,returns,logreturns)
	with open('RTD_test_EICHER.csv', 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(['DATE','TIME','OPEN','HIGH','LOW','CLOSE','RETURNS','LOGRETURNS'])
		writer.writerows(rows)

read = pd.read_csv('./NSE EICHERMOT EQ.csv')
	
data_cleaning(30,list(read.DATE),list(read.TIME),list(read.OPEN),list(read.HIGH),list(read.LOW),list(read.CLOSE))