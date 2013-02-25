"""
Remove resets from cumulative whr plot, wh_DF

SharedSolar
By: Mitchell Lee
Begun: February 20, 2013

"""

import os
import numpy as np
import datetime
import dateutil.parser as dp
import string as st
import csv
import pandas as pd

wh_DF = pd.read_csv('gw_wh.csv', delimiter=',',index_col =0,parse_dates = True)
wh_ary = np.array(wh_DF)

r,c = np.shape(wh_ary)
wh_ary_cum = np.zeros((r,c))
wh =  np.zeros((r,c))
nukelist = []

for jx in range(0,c):
	print wh_DF.columns[jx]
	for ix in range(0,r-1):
		if ix == 0:
			lastreal = 0			
		cknan1 = np.isnan(wh_ary[ix,jx])
		cknan2 = np.isnan(wh_ary[ix+1,jx])
	
		if cknan1 == 0 and cknan2 == 0:
			if wh_ary[ix+1,jx] >= wh_ary[ix,jx]:
				wh_ary_cum[ix+1,jx] = wh_ary_cum[ix,jx] + wh_ary[ix+1,jx] - wh_ary[ix,jx]
				wh[ix+1,jx] = wh_ary_cum[ix+1,jx] - wh_ary_cum[ix,jx] 
				lastreal = wh_ary[ix+1,jx]
			else:
				wh_ary_cum[ix+1,jx] = wh_ary_cum[ix,jx]# + wh_ary[ix+1,jx]
				nukelist.append([ix+1,jx])						
				wh[ix+1,jx] = np.nan#wh_ary_cum[ix+1,jx] - wh_ary_cum[ix,jx]
				
			lastreal = wh_ary[ix+1,jx]
	
		if cknan2 == 1:
			wh_ary_cum[ix+1,jx] = wh_ary_cum[ix,jx]
			wh[ix+1,jx] = np.nan

		if cknan1 == 1 and cknan2 == 0:
			wh_ary_cum[ix+1,jx] = wh_ary_cum[ix,jx]# + wh_ary[ix+1,jx] -lastreal#jumps will occur if reset is missed
			wh[ix+1,jx] = np.nan
			nukelist.append([ix+1,jx])				
			lastreal = wh_ary[ix+1,jx]

# where wh_ary = nan, wh_ary_cum = nan
wh_ary_cum = np.where(np.isnan(wh_ary) == True, wh_ary,1) * wh_ary_cum
wh_ary_cum[nukelist] = np.nan
wh_DF_cum = pd.DataFrame(wh_ary_cum, index = wh_DF.index, columns =  wh_DF.columns)
wh = pd.DataFrame(wh, index = wh_DF.index, columns =  wh_DF.columns)
wh_DF_cum.to_csv('gw_wh_cum.csv', index_label = 'dates' )
wh.to_csv('gw_wh_fix.csv', index_label = 'dates' )
