import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import os
import string

def open_power_ts(circuit):
	'''open a plot of mains or circuits timeseries of power data in watts. When in Ubuntu change
	path to appropriate location'''
	
	'''
	#While in windows
	ts_path = 'C:/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database/csv_flat_files_minute/DFlist/'
	'''
	#While in Ubuntu
	ts_path = '/media/mountpoint/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database/csv_flat_files_minute/DFlist/'

	ts = pd.read_csv(ts_path + circuit + '_min.csv', delimiter = ';', index_col = 0, parse_dates = True)
	ts[ts > ts.std()*5. + ts.mean()] = np.nan
	return ts

def make_max_day_DF():
	import gw_data_stats
	#ts = pd.read_csv(ts_path + circuit + '_min.csv', delimiter = ';', index_col = 0, parse_dates = True)
	#ts[ts > ts.std()*5. + ts.mean()] = np.nan
	flist = []
	DFlist = '/media/mountpoint/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database/csv_flat_files_minute/DFlist'
	#for (dirpath,dirnames,filenames) in os.walk('C:\Users\Mitchell\Documents\Shared_Solar\Shared_Solar_database'):
	for (dirpath,dirnames,filenames) in os.walk('/media/mountpoint/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database/csv_flat_files_minute'):
		print dirpath
		if dirpath == DFlist:
			for _file in filenames:
				flist.append(_file)

	max_day_ary = pd.DataFrame(index = range(0,24))
	for ix, fname in enumerate(flist):
		x = pd.read_csv(DFlist +'/' + fname, delimiter = ';', index_col = 0, parse_dates = True)
		x[x > x.std()*5. + x.mean()] = np.nan
		x = x.dropna()
		col_head = string.rsplit(fname,'_',1)[0]
		col = pd.DataFrame(gw_data_stats.make_maxday(x))
		col.columns = [col_head]
		max_day_ary = max_day_ary.join(pd.DataFrame(col))
		
		print col_head
	return max_day_DF

def make_ldf(site, max_day_DF):	
	import gw_data_stats
	'''make load diversity factor'''
	site_dict = gw_data_stats.make_site_dict(max_day_DF)
	circuits = site_dict[site]	
	mains = site + '_0'
	ldf = max_day_DF[circuits].sum(axis = 1)/max_day_DF[mains]
	return ldf
	
	



