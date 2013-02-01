# Mitchell Lee
# Shared Solar 
# Read all houlry flat csv files and write them to a single .mat file
# Began Script on November 29, 2012

# list all csv files

import os
import numpy as np
import pandas as pd
import datetime


# Import dataset 1

# corrected so that it has the same time indices at the second dataset
demdata = pd.read_csv('allmetersdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)[8760:]
# If the hourly demand is greater than 1000 Wh replace with nan
demdata[demdata >= 1000] = np.nan
demdatacum = pd.read_csv('allmeterscumdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)[8760:]
creddata  = pd.read_csv('allmeterscreditarray.csv', delimiter=',',index_col =0,parse_dates = True)[8760:]
circlist = demdata.columns.tolist()
datelist_hr = demdata.index.tolist()
r, c = np.shape(demdata)

# Separate ML (dataset 1)

ml = []
ug = []
for ix in range(0,c):
	n = demdata.columns[ix][0]
	if n == 'm':
		ml.append(demdata.columns[ix])
	else:
		ug.append(demdata.columns[ix])

# Import dataset 2


demdata2 = pd.read_csv('allmetersdemandarray2.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdata2[demdata2 >= 1000] = np.nan
demdatacum2 = pd.read_csv('allmeterscumdemandarray2.csv', delimiter=',',index_col =0,parse_dates = True)
creddata2  = pd.read_csv('allmeterscreditarray2.csv', delimiter=',',index_col =0,parse_dates = True)
circlist2 = demdata2.columns.tolist()
datelist2_hr = demdata2.index.tolist()
r2, c2 = np.shape(demdata2)

ug2 = []
for ix in range(0,c2):
    n = demdata2.columns[ix][0]
    if n == 'u':
        ug2.append(demdata2.columns[ix])

# List of all Meters and Circuits 

all_cols = np.sort(list(set(ug+ug2)))
col_num = np.shape(all_cols)[0]

## generate the list of dates for timeseries index
d0 = datetime.datetime(2011,1,1,0)
d1 = datetime.datetime(2012,12,31,23)
datelist = pd.date_range(d0,d1,freq='1h')
dr =  int((d1 - d0).days)*24 +24.

# Make Array for DataFrame
demout_temp = np.zeros([np.shape(datelist)[0],np.shape(all_cols)[0]]); demout_temp[:] = np.nan
credout_temp = np.zeros([np.shape(datelist)[0],np.shape(all_cols)[0]]); credout_temp[:] = np.nan

for jx, site in enumerate(all_cols):
	in1 = site in ug
	in2 = site in ug2
	
	if (in1 == True) and (in2 ==True):		
		dem1_temp = np.array(demdata[site])
		dem2_temp = np.array(demdata2[site])
		cred1_temp = np.array(creddata[site])
		cred2_temp = np.array(creddata2[site])
		
		print 'both', site
		for ix, tim in enumerate(datelist):
			in_time1 = np.isnan(dem1_temp[ix])
			in_time2 = np.isnan(dem2_temp[ix])
			if in_time2 == False:
				demout_temp[ix,jx] = dem2_temp[ix]
				credout_temp[ix,jx] = cred2_temp[ix]
			elif in_time1 == False:
				credout_temp[ix,jx] = cred1_temp[ix]

	elif in1 == True:
		print 'demdata', site
		demout_temp[:,jx] = np.array(demdata[site])
		credout_temp[:,jx] = np.array(creddata[site])
	elif in2 == True:
		print 'demdata2', site
		demout_temp[:,jx] = np.array(demdata2[site])
		credout_temp[:,jx] = np.array(creddata2[site])

demDF  = pd.DataFrame(demout_temp,index = pd.DatetimeIndex(datelist), columns = all_cols)
demDF.to_csv('allmetersdemandarray_merged.csv', index_label = 'dates' )
credDF  = pd.DataFrame(credout_temp,index = pd.DatetimeIndex(datelist), columns = all_cols)
credDF.to_csv('allmeterscreditarray_merged.csv', index_label = 'dates' )



