# Mitchell Lee
# Shared Solar 
# Read all houlry flat csv files and write them to a single .mat file
# Began Script on November 29, 2012

import numpy as np
import pandas as pd 


# list all csv files


# SD card data
SD_ugdem = pd.read_csv('allmetersdemandarray_merged.csv', delimiter=',',index_col =0,parse_dates = True)
SD_ugcred = pd.read_csv('allmeterscreditarray_merged.csv', delimiter=',',index_col =0,parse_dates = True)
SD_mldem = pd.read_csv('allmetersdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
SD_mlcred = pd.read_csv('allmeterscreditarray.csv', delimiter=',',index_col =0,parse_dates = True)

# Gateway
gw_wh = pd.read_csv('gw_wh_fix.csv', delimiter=',',index_col =0,parse_dates = True)
gw_cred = pd.read_csv('gw_cred.csv', delimiter=',',index_col =0,parse_dates = True)

# Separate ML (dataset 1)

r,c = np.shape(SD_mldem) 

ml = []
ug = []
for ix in range(0,c):
	n = SD_mldem.columns[ix][0]
	if n == 'm':
		ml.append(SD_mldem.columns[ix])
	else:
		ug.append(SD_mldem.columns[ix])

SD_mldem = SD_mldem[ml]
SD_mlcred = SD_mlcred[ml]

# Complete list of columns
col_list = np.sort(list(set(SD_mldem.columns) | set(SD_ugdem.columns) | set(gw_wh)))

# Make column names uniform across all DataFrames 
SD_wh = pd.DataFrame(SD_mldem.join(SD_ugdem), columns = col_list, index = gw_wh.index)
SD_cred = pd.DataFrame(SD_mlcred.join(SD_ugcred), columns = col_list,index = gw_wh.index)
gw_wh = pd.DataFrame(gw_wh, columns = col_list)
gw_cred = pd.DataFrame(gw_cred, columns = col_list)


# Make Array for DataFrame
SDgw_wh = np.zeros([np.shape(gw_wh.index)[0],np.shape(col_list)[0]]); SDgw_wh[:] = np.nan
SDgw_cred = np.zeros([np.shape(gw_wh.index)[0],np.shape(col_list)[0]]); SDgw_cred[:] = np.nan

# Make arrays to read into loop
SD_wh_ary = np.array(SD_wh)
gw_wh_ary = np.array(gw_wh)
SD_cred_ary = np.array(SD_cred)
gw_cred_ary = np.array(gw_cred)

for jx, col in enumerate(col_list):
	print col
	for ix, row in enumerate(gw_wh.index):
		if np.isnan(SD_wh_ary[ix,jx]) == True:
			SDgw_wh[ix,jx] = gw_wh_ary[ix,jx]
		else:
			SDgw_wh[ix,jx] = SD_wh_ary[ix,jx]

		if np.isnan(SD_cred_ary[ix,jx]) == True:
			SDgw_cred[ix,jx] = gw_cred_ary[ix,jx]
		else:
			SDgw_cred[ix,jx] = SD_cred_ary[ix,jx]

SDgw_wh = pd.DataFrame(SDgw_wh, index = gw_wh.index, columns = col_list)
SDgw_cred = pd.DataFrame(SDgw_cred, index = gw_wh.index, columns = col_list)

SDgw_wh .to_csv('SDgw_wh.csv', index_label = 'dates' )
SDgw_cred .to_csv('SDgw_cred.csv', index_label = 'dates' )

