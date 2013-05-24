"""
Mitchell Lee
SharedSolar: Combine hourly watthour table views (initially from apan3)
that were converted into single year csv's using writeToCSV 
into single csv file from each site + circuit combination

May 23, 2013
"""

import os
import numpy as np
import pandas as pd
import csv


in_path = "/home/mitchell/Documents/SharedSolar/SD_5_2013/flat_files_yearly"
out_path = "/home/mitchell/Documents/SharedSolar/SD_5_2013/flat_files_combined"
walk_path = "/home/mitchell/Documents/SharedSolar/SD_5_2013"
file_list = []



for (dirpath,dirnames,filenames) in os.walk(walk_path):
		for _file in filenames:
			if dirpath == in_path:
				file_list.append(_file)

file_list = list(np.sort(file_list))

"""
for ix, _file in enumerate(file_list):
		
	new_file = _file.split('_')
	new_file = new_file[0] +'_' + new_file[1]+".csv"
	fi_csv = open(in_path + "/" + _file,'r')
	fo_csv = open(out_path + "/" + new_file,'a')
	rcsv = csv.reader(fi_csv)
	wcsv = csv.writer(fo_csv)

	for jx, row in enumerate(rcsv):
		year = pd.to_datetime(str(row[0]).split(';')[0]).year
		if year < 2014:
			wcsv.writerow(row)

	fi_csv.close()
	fo_csv.close()

"""
# Combine DataFrame 
file_list = []
for (dirpath,dirnames,filenames) in os.walk(walk_path):
		for _file in filenames:
			if dirpath == out_path:
				file_list.append(_file)

file_list = list(np.sort(file_list))
for ix, _file in enumerate(file_list):
	if ix == 0:
		dates = pd.date_range('1-1-2010 00:00:00','12-31-2013 23:00:00', freq = "h")
		_file = _file.strip('.csv')		
		col_head = _file.split('_')[0]+"_"+_file.split('_')[1]
		first_col = pd.read_csv(out_path + "/"+ _file+".csv", index_col = 0, parse_dates = True, delimiter = ';',names= [col_head])
		Wh_DF = pd.DataFrame(first_col, index = dates)
	else:
		_file = _file.strip('.csv')				
		col_head = _file.split('_')[0]+"_"+_file.split('_')[1]
		next_col = pd.read_csv(out_path + "/"+ _file+".csv", index_col = 0, parse_dates = True, delimiter = ';',names= [col_head])
		next_col = pd.DataFrame(next_col, index = dates)
		Wh_DF = Wh_DF.join(next_col)

Wh_DF.to_csv('SD_wh_5_2013.csv', header = True,index = True)


