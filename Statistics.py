import csv
import os
import glob
path1='/home/cse/Documents/csv_data'
stat={}
data=[]


for file_name in sorted(glob.glob(os.path.join(path1,'*.csv'))):
	with open(file_name, 'rb') as inp:
		for row in csv.reader(inp):
			if row[1] in stat:
				stat[row[1]]+=1
			else:
				stat[row[1]]=1

statistics=open('/tmp/statis.csv','w')
csvwriter=csv.writer(statistics)
for iter in stat:
    data=[]
    data.append(iter)
    data.append(stat[iter])
    csvwriter.writerow(data)
statistics.close()

          
