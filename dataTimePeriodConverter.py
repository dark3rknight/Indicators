import math
import pandas as pd
import csv
import os

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def data_cleaning(file,tValue,date,time,close):
	previous_date = date[0]
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
			flag = 0
			maximum = close[i]
			minimum = close[i]
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
	rows = zip(formatted_date,formatted_time,formatted_high,formatted_low,formatted_close,returns,logreturns)
	with open('./AXIS14', 'w+') as f:
		writer = csv.writer(f)
		writer.writerow(['DATE','TIME','HIGH','LOW','CLOSE','RETURNS','LOGRETURNS'])
		writer.writerows(rows)

path = "./AXISBANK.csv"
#files = os.listdir(path)
#print(len(files))
#for file in files:
file = path
read = pd.read_csv(file)
print(file)
data_cleaning(file,6,list(read.DATE),list(read.TIME),list(read.CLOSE))