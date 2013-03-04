"""
gw_data_stats
SharedSolar
By: Mitchell Lee
Began on February 22, 2013
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd


# Open GW and SD data
def open_SSdata():
	'''Open gw_wh, gw_cred, SD_wh, SD_cred: in that order'''
	gw_wh = pd.read_csv('gw_wh_fix.csv', delimiter = ',', index_col = 0, parse_dates = True)	
	gw_cred = pd.read_csv('gw_cred.csv', delimiter = ',', index_col = 0, parse_dates = True)
	SD_wh = pd.read_csv('SD_wh_merged.csv', delimiter = ',', index_col = 0, parse_dates = True)
	SD_cred = pd.read_csv('SD_cred_merged.csv', delimiter = ',', index_col = 0, parse_dates = True)
	return gw_wh, gw_cred, SD_wh, SD_cred

# Datamap of any DataFrame
def data_map(wh,color):

	cmap = colors.ListedColormap(['white', color])
	fig = plt.figure()
	densityplot = fig.add_subplot(1,1,1)
	densityplot.spy(wh, aspect = 'auto', cmap = cmap)
	densityplot.set_xticks(range(0,np.shape(wh)[1]))	
	densityplot.set_xticklabels(wh.columns)
	densityplot.set_yticks(range(0,np.shape(wh)[0],750))
	densityplot.set_yticklabels(wh.index[0:np.shape(wh)[0]:750])
	densityplot.set_xlabel('Mains and Circuits')
	densityplot.set_ylabel('Date and Time')
	densityplot.set_title('GW Data map')
	plt.show()

#	Datamap of to DFs to show overlap
def data_map_comp(wh,demdata,color1,color2):
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib import colors
	import pandas as pd
	cols  = list(np.sort(list(set(wh.columns) | set(demdata.columns))))
	demdata = pd.DataFrame(demdata, index = wh.index,columns = cols)
	wh = pd.DataFrame(wh, index = wh.index,columns = cols)
	cmap1 = colors.ListedColormap(['white', color1])
	cmap2 = colors.ListedColormap(['white', color2])
	fig = plt.figure()
	densityplot = fig.add_subplot(1,1,1)
	densityplot.spy(demdata, aspect = 'auto',cmap = cmap2)		
	densityplot.spy(wh, aspect = 'auto', cmap = cmap1, alpha = 0.5)
	densityplot.set_xticks(range(0,np.shape(wh)[1]))	
	densityplot.set_xticklabels(wh.columns)
	densityplot.set_yticks(range(0,np.shape(wh)[0],750))
	densityplot.set_yticklabels(wh.index[0:np.shape(wh)[0]:750])
	densityplot.set_xlabel('Mains and Circuits')
	densityplot.set_ylabel('Date and Time')
	densityplot.set_title('GW Data map')
	plt.show()

def make_m_from_h(hour_data):
	month_data = hour_data.resample('D', how = 'sum').resample('M',how = 'mean')
	return month_data,
	
def make_month_bplot(month_data):
	months = month_data.index.month
	years = month_data.index.year
	month_names = []
	for ix in range(0,np.shape(month_data.index)[0]):
		month_names.append( str(months[ix]) +'-'+ str(years[ix]))
	fig = plt.figure()
	month_plot = fig.add_subplot(1,1,1)
	month_plot.set_xticks(range(0,np.shape(month_names)[0]))
	month_plot.set_xticklabels(month_names,rotation = 90)
	month_plot.set_title('Average Daily Energy Usage (Wh/Day)', fontsize =18)
	month_plot.set_xlabel('Month',fontsize =18)
	month_plot.set_ylabel('Average Daily Energy Usage (Wh/Day)',fontsize =18)
	month_plot.bar(range(0,48), month_data, align = 'center')
	return month_plot, month_names

