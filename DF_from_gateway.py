"""
Take Whr and credit Gateway Data from All meters and circuits
and put it into two pandas DataFrames.
One DF for credit and another for energy

Shared Solar 
By: Mitchell Lee
Begun: February 19, 2013
"""

import matplotlib.pyplot as pdlt
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy as sa
import sys

sys.path.append('/home/mitchell/Documents/SharedSolar/ss_sql_views/python')
import offline_gateway as gw


date_start = '2010-01-01'
date_end = '2013-12-31'
d0 = dt.datetime(2010,1,1,0)
d1 = dt.datetime(2013,12,31,23)
datelist = pd.date_range(d0,d1,freq='1h')

cl = gw.get_circuit_list()
circ_list = []#list of circuit names as strings
circ_dict = {} #dictionary circuit name string as key, with number equavilent 
wh_DF = pd.DataFrame(index = datelist)
cred_DF = pd.DataFrame(index = datelist)

# Populate the list of all circuits and mains
# AND populate dictionary to translate string name to number name
for ix, row in enumerate(cl):
	circ_list.append(row[1].encode('ascii')+'_'+str(int(row[2][-2:])))
	circ_dict[circ_list[ix]] = row[0]

# Create a DataFrame of Wh for each main or site
for ix, row in enumerate(circ_list):
	wh_col = gw.get_watthours_for_circuit_id(circ_dict[row], date_start, date_end)[0].apply(np.float32)
	wh_col.resample('H', how = np.max) # resample options sum, mean, std, max, min, median, first, last, ohlc.
	wh_col = pd.Series(wh_col, name = row)
	wh_DF = wh_DF.join(wh_col)

	cred_col = gw.get_credit_for_circuit_id(circ_dict[row], date_start, date_end).apply(np.float32)
	cred_col.resample('H', how = np.min)
	cred_col = pd.Series(cred_col, name = row)
	cred_DF = cred_DF.join(cred_col)	
	print row

wh_DF.to_csv('gw_wh.csv', index_label = 'dates' )
cred_DF.to_csv('gw_cred.csv',index_label = 'dates' )








