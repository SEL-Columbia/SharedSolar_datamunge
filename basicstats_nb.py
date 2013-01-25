# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Basic Analysis of Available SharedSolar Data: By Mitchell Lee

# <codecell>

from pandas import *
import numpy as np
import re
import matplotlib
import matplotlib.pyplot as plt
import dateutil.parser as dp

# <codecell>

#cd "C:/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database"

# <headingcell level=2>

# Import csv file as dataframe

# <codecell>

demdata = read_csv('allmetersdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdata[demdata >= 1000] = np.nan
demdatacum = read_csv('allmeterscumdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
creddata  = read_csv('allmeterscreditarray.csv', delimiter=',',index_col =0,parse_dates = True)
circlist = demdata.columns.tolist()
datelist_hr = demdata.index.tolist()
r, c = np.shape(demdata)

# <headingcell level=2>

# Separate Circuit and Mains Data

# <codecell>

#  Create list of Mains names and Circuit Names
mains = []
circuits = []
for ix in range(0,c):
    m_c = int(demdata.columns[ix].split('_')[1])
    if m_c == 0:
        mains.append(demdata.columns[ix])
    else:
        circuits.append(demdata.columns[ix])
# Create separate dataframe of mains and circuits 
mainsdf = demdata[mains]
circuitsdf = demdata[circuits]

# <headingcell level=2>

# Convert to daily resolution

# <codecell>

# Sum across hours to make daily resolution 
demdata_day = demdata.resample('D', how='sum')
mainsdf_day = mainsdf.resample('D', how='sum')
circuitsdf_day = circuitsdf.resample('D', how='sum')
datelist_day = demdata_day.index.tolist()

# <headingcell level=2>

# Convert to monthly resoulution

# <codecell>

# Use Daily Average Energy 
demdata_month = demdata_day.resample('M', how='mean')
mainsdf_month = mainsdf_day.resample('M', how='mean')
circuitsdf_month= circuitsdf_day.resample('M', how='mean')
datelist_month = demdata_day.index.tolist()

# <headingcell level=2>

# Plot the sparseness of the shared solar data HOURLY RESOLUTION

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata, aspect = 'auto')
densityplot.set_xticks(range(0,c))
densityplot.set_xticklabels(circlist)
#densityplot.set_yticks(datelist_hr[0:r:1000])
#densityplot.set_yticklabels(datelist_hr[0:r:1000])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution')
plt.show()
"""
# <headingcell level=2>

# Plot the sparsenesss of the shared solar data MONTHLY RESOLUTION

# <codecell>

fig = plt.figure()
densitymonthplot = fig.add_subplot(1,1,1)
pic = densitymonthplot.imshow(demdata_month, aspect = 'auto')
densitymonthplot.set_xticks(range(0,c))
densitymonthplot.set_xticklabels(circlist)
densitymonthplot.set_yticks(range(0,np.shape(demdata_month)[0]))
densitymonthplot.set_yticklabels(period_range(datelist_day[0],datelist_day[-1],freq='M'))
densitymonthplot.set_xlabel('Mains and Circuits')
densitymonthplot.set_ylabel('Date and Time')
densitymonthplot.set_title('Average Daily Energy Use: BY COLOR (Wh)')
fig.colorbar(pic)
pic.set_interpolation('nearest')
plt.show()

# <headingcell level=2>

# Average daily energy use of Mains

# <codecell>

demdata_day_mean = demdata_day.mean()
demdata_day_std = demdata_day.std()

fig = plt.figure()
meandaybar = fig.add_subplot(1,1,1)
# show std as error bars
meandaybar.bar(range(0,np.shape(mains)[0]),demdata_day_mean[mains])#, yerr = demdata_day_std,ecolor='black') 
meandaybar.set_xticks(range(0,np.shape(mains)[0]))
meandaybar.set_xticklabels(circlist)
meandaybar.set_xlabel('Mains')
meandaybar.set_ylabel('Average Daily Energy Demand (Wh)')
meandaybar.set_title('Average Daily Demand for Mains')
plt.show()

# <headingcell level=2>

# Typical daily profile for each circuit and mains

# <codecell>

dayprofarray = np.zeros((24, c))
for ix in range(0,24):
    hour = demdata.index.hour
    selector = (hour == ix)
    dayprofarray[ix,:] = demdata[selector].mean()

alldayprof = DataFrame(dayprofarray, columns = demdata.columns)
mdayprof = alldayprof[mains]
cdayprof = alldayprof[circuits]

# <headingcell level=2>

# COLORMAP OF DAILY PROFILE FOR MAINS ONLY 

# <codecell>

fig = plt.figure()
mavedayplot = fig.add_subplot(1,1,1)
pic = mavedayplot.imshow(mdayprof, aspect = 'auto')
mavedayplot.set_xticks(range(0,np.shape(mdayprof)[-1]))
mavedayplot.set_xticklabels(mdayprof.columns)
mavedayplot.set_yticks(range(0,24))
mavedayplot.set_yticklabels(range(0,24))
mavedayplot.set_xlabel('Mains')
mavedayplot.set_ylabel('Time')
mavedayplot.set_title('Average Hourly Energy Usage')
pic.set_interpolation('nearest')
fig.colorbar(pic)
plt.show()

# <headingcell level=2>

# Historgram of Mean Daily Energy Usage subplot mains and circuits

# <codecell>

# remove circuitdemdata_day_mean
circdf_month_nonnan = circuitsdf_month.mean().dropna()
mainsdf_month_nonnan = mainsdf_month.mean().dropna()

# <headingcell level=3>

# Circuits

# <codecell>

fig = plt.figure()
cdemhisto =  fig.add_subplot(1,1,1)
cdemhisto.hist(circdf_month_nonnan ,bins = 20, histtype='bar',range = (0,500))
cdemhisto.set_xlabel('Average Daily Energy Consumption (Wh)')
cdemhisto.set_ylabel('Number of Consumer Circuits')
cdemhisto.set_title('Histogram of Consumers by Daily Energy Consumption (Wh)')
plt.show()

# <headingcell level=3>

# Mains

# <codecell>

fig = plt.figure()
cdemhisto =  fig.add_subplot(1,1,1)
cdemhisto.hist(mainsdf_month_nonnan ,bins = 5, histtype='bar',range = (0,2500))
cdemhisto.set_xlabel('Average Daily Energy Consumption (Wh)')
cdemhisto.set_ylabel('Number of Mains')
cdemhisto.set_title('Histogram of Mains by Daily Energy Consumption (Wh)')
plt.show()

# <headingcell level=2>
"""
# Plot timeseries of Arbitrary Main or Circuit

# <codecell>

ts = Series(demdata['ml08_0'])   #.dropna())
fig = plt.figure()
tsplt =  fig.add_subplot(1,1,1)

ts.plot()
#tsplt.set_xticks(range(0,np.shape(ts)[-1]))
#tsplt.set_xticklabels(ts.index)
tsplt.set_xlabel('Time Series')
tsplt.set_ylabel('Energy (Wh)')
plt.show()
# <codecell>


# <codecell>


# <codecell>


