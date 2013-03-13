
def gw_data_stats():
	''' 
	gw_data_stats
	SharedSolar
	By: Mitchell Lee
	Began on February 22, 2013


	A group of functions used to analyze gateway, SD card, and merged 
	consumption and credit history using pandas. Included functions are: 
		open_SSdata()
		data_avl_perc(gw_wh,SD_wh,SDgw_wh)
		data_map(wh,color)
		data_map_comp(wh,demdata,color1,color2):
		data_map_mag(DF, vmin, vmax):
		make_m_from_h(hour_data):		
		make_maxday(SDgw_wh):
		make_month_bplot(month_data)
		make_purch_rec(cred_DF):
		make_site_dict(DF)
		make_typday(SDgw_wh):
		sort_country(DF)
		sort_mains(DF)
	'''



import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd


# Open GW and SD data
def open_SSdata():
	'''Open gw_wh, gw_cred, SD_wh, SD_cred, SDgw_wh, SDgw_cred: in that order'''
	gw_wh = pd.read_csv('gw_wh_fix.csv', delimiter = ',', index_col = 0, parse_dates = True)	
	gw_cred = pd.read_csv('gw_cred.csv', delimiter = ',', index_col = 0, parse_dates = True)
	SD_wh = pd.read_csv('SD_wh_merged.csv', delimiter = ',', index_col = 0, parse_dates = True)
	SD_cred = pd.read_csv('SD_cred_merged.csv', delimiter = ',', index_col = 0, parse_dates = True)
	SDgw_wh = pd.read_csv('SDgw_wh.csv', delimiter = ',', index_col = 0, parse_dates = True)
	SDgw_cred = pd.read_csv('SDgw_cred.csv', delimiter = ',', index_col = 0, parse_dates = True)
	return gw_wh, gw_cred, SD_wh, SD_cred, SDgw_wh, SDgw_cred



def data_avl_perc(gw_wh,SD_wh,SDgw_wh):
	'''Import all of the SharedSolar gw, SD, and merged SDgw data. Determine
	The percentage of all data that we have for SD cards, the gateway,
	the union of these sets, and the intersection of these sets. '''

	start_date = '2010-12-01 00:00:00'        
	end_date = '2013-02-09 00:00:00'
	gw_wh.ix[:start_date] = np.nan; SD_wh.ix[:start_date] = np.nan; SDgw_wh.ix[:start_date] = np.nan
	keep = []
	toss = []
	cols  = list(np.sort(list(set(gw_wh.columns) | set(SD_wh.columns) | set(SDgw_wh.columns))))
	gw_wh = pd.DataFrame(gw_wh, index = gw_wh.index,columns = cols)
	SD_wh = pd.DataFrame(SD_wh, index = SD_wh.index,columns = cols)
	SDgw_wh = pd.DataFrame(SDgw_wh, index = SDgw_wh.index,columns = cols)
	for ix, col in enumerate(gw_wh.columns):
			n = col[0:4]
			if n == 'ug00':
			        toss.append(col)
			else:
			        keep.append(col)
	start_dict = {}
	for ix, col in enumerate(keep):
			start_dict[col] = [str(SDgw_wh[col].dropna().index[0])]

	all_dat = {}
	gw = {}
	SD = {}
	union = {}
	intersect = {}

	for ix, col in enumerate(SDgw_wh[keep].columns):
			all_dat[col] = np.shape(SDgw_wh[col][start_dict[col][0]:end_date])[0]
			gw[col] = np.shape(gw_wh[col].dropna())[0]
			SD[col] = np.shape(SD_wh[col].dropna())[0]
			union[col] =  np.shape(SDgw_wh[col].dropna())[0]
			intersect[col] = np.shape(list(set(SD_wh[col].dropna().index) & set(gw_wh[col].dropna().index)))[0]

	all_dat = pd.DataFrame(pd.Series(all_dat), columns = ['all_data'])
	gw =   pd.DataFrame(pd.Series(gw), columns = ['gw'], dtype = float)
	SD =   pd.DataFrame(pd.Series(SD), columns = ['SD'], dtype = float)
	union =  pd.DataFrame(pd.Series(union), columns = ['union'], dtype = float)
	intersect =   pd.DataFrame(pd.Series(intersect), columns = ['intersection'], dtype = float)
	perc_avl = all_dat.join(gw).join(SD).join(union).join(intersect).sum()   
	return perc_avl  



# Datamap of any DataFrame
def data_map(wh,color):
	''' data_map(DF,color):
	Import a DataFrame and make a map of data availability.'''
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
	'''data_map(DF1,color1,DF2,color2):
	Import two DataFrames and plot their overlap'''
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
	densityplot.spy(wh, aspect = 'auto', cmap = cmap1, alpha = 0.6)
	densityplot.set_xticks(range(0,np.shape(wh)[1]))	
	densityplot.set_xticklabels(wh.columns)
	densityplot.set_yticks(range(0,np.shape(wh)[0],750))
	densityplot.set_yticklabels(wh.index[0:np.shape(wh)[0]:750])
	densityplot.set_xlabel('Mains and Circuits')
	densityplot.set_ylabel('Date and Time')
	densityplot.set_title('Data Map (GW = Red, SD = Green, Both = Brown)')
	plt.show()

def data_map_mag(DF, vmin, vmax):
	'''Import DataFrame and make heatmap of data according to availablity and magnitude.
	Specify minimum and maximum values for scaling of color
	Resolution finer than monthly will crash.	
	'''
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	import matplotlib as mpl
	fig = plt.figure()
	dayuse = fig.add_subplot(1,1,1)
	pic = dayuse.imshow(DF, aspect = 'auto', cmap= mpl.cm.jet, vmin = vmin, vmax= vmax)
	dayuse.set_xticks(range(0,np.shape(DF)[-1]))
	dayuse.set_xticklabels(DF.columns)
	dayuse.set_yticks(range(0,np.shape(DF)[0]))
	dayuse.set_yticklabels(DF.index)
	dayuse.set_title('Average Daily Energy Consumption over Time')
	dayuse.set_xlabel('Location')
	dayuse.set_ylabel('Month')
	pic.set_interpolation('nearest')
	fig.colorbar(pic).set_label('Average Wh Consumed Daily')
	dayuse.plot()

def make_m_from_h(hour_data):
	""" Take in a DataFrame with hourly resolution. Convert to monthly resolution
	by first resample('D',sum) then resample('M',mean) to show the average daily energy
	use in each month"""
	hour_data[hour_data >= 1000] = np.nan
	month_data = hour_data.resample('D', how = 'sum').resample('M',how = 'mean')
	return month_data,


def make_maxday(SDgw_wh):
	'''Import the hourly energy usage of a consumer or mains and create a diurnal 
	day of using the maximum energy consumption at each hour over the entire timeseries'''
	r,c = np.shape(SDgw_wh)
	maxday = np.zeros((24, c))
	for ix in range(0,24):
		hour = SDgw_wh.index.hour
		selector = (hour == ix)
		maxday[ix,:] = SDgw_wh[selector].max()

	maxday = pd.DataFrame(maxday, index = range(0,24), columns = SDgw_wh.columns)
	return maxday


	
def make_month_bplot(month_data):
	'''Import the monthly energy usage of a consumer or mains 
	and make a barplot of average daily energy consumption by month'''
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
	month_plot.bar(range(0,48), month_data.astype(float), align = 'center')
	return month_plot, month_names


def make_purch_rec(cred_DF):
	'''make a timeseries record of purchases for call SharedSolar Consumers
	Constructs consumer history by finding increase in credits for each 
	consumer and rounding up to the nearest increment of 500'''
	cred_ary = np.array(cred_DF);
	r, c = np.shape(cred_ary)
	purch_ary = np.zeros((r,c)); purch_ary[:] = np.nan
	for jx in range(0,c):
		lastreal = 0
		for ix in range(0,r):
			diffs = cred_ary[ix, jx] - lastreal
			if diffs > 0 :
				purch_ary[ix+1,jx] = diffs
			if np.isnan(cred_ary[ix,jx]) == False:
				lastreal = cred_ary[ix,jx]
	purch_ary[purch_ary < 100] = np.nan		
	purch_ary = np.ceil(purch_ary/500.)*500.			
	purch_rec = pd.DataFrame(purch_ary, index = cred_DF.index, columns = cred_DF.columns)
	return purch_rec

def make_site_dict(DF):
	''' import a DataFrame and output a dictionary which includes 
	each site and a list of operational circuits for that site. Will include
	a listing for UG05 regardless of it is needed.'''
	
	import string
	import numpy as np
	import pandas as pd 
	mains = []
	circuits = []
	for jx, column in enumerate(DF.columns):
		n = int(column.split('_')[1])
		if n == 0:
			mains.append(column)
		else:
			circuits.append(column)

	site_dict = {}
	mains.append('ug05_0')
	site_list = np.sort(mains)

	for ix, site in enumerate(site_list):
		site_dict[string.split(site,'_')[0]] = []

	for ix, circ in enumerate(circuits):
		site_dict[string.split(circ,'_')[0]].append(circ)
	
	return site_dict


def make_typday(SDgw_wh):
	'''Import the hourly energy usage of a consumer or mains 	
	and create a typical diurnal day of average energy consumption
	and associated standard deviation'''
	r, c = np.shape(SDgw_wh)
	typday = np.zeros((24, c))
	typday_std = np.zeros((24, c))
	for ix in range(0,24):
		hour = SDgw_wh.index.hour
		selector = (hour == ix)
		typday[ix,:] = SDgw_wh[selector].mean()
		typday_std[ix,:] = SDgw_wh[selector].std()

	typday = pd.DataFrame(typday, index = range(0,24), columns = SDgw_wh.columns)
	typday_std = pd.DataFrame(typday_std, index = range(0,24), columns = SDgw_wh.columns)
	return typday, typday_std


def sort_country(DF):
	''' Sort SharedSolar DF into ml_DF and ug_DF'''
	r, c = np.shape(DF)
	#Separate ML (dataset 1)
	ml = []
	ug = []
	for ix in range(0,c):
		n = DF.columns[ix][0]
		if n == 'm':
			ml.append(DF.columns[ix])
		else:
			ug.append(DF.columns[ix])

	ml_DF = DF[ml]
	ug_DF = DF[ug]

	return ml_DF, ug_DF

def sort_mains(DF):
	''' Retun two DFs one of mains and one of circuits from original DF'''
	mains = []
	circs= []
	for ix, row in enumerate(DF.columns):
		n = int(row.split('_')[1])
		if n == 0:
		  	mains.append(DF.columns[ix])
		else:
		    circs.append(DF.columns[ix])
	mains = DF[mains]
	circs = DF[circs]
	return mains, circs



