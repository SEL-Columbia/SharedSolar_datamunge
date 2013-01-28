# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Comparing UG Data Before and After Update: Mitchell Lee

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

# Import dataset 1

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

# Separate ML (dataset 1)

ml = []
for ix in range(0,c):
    n = demdata.columns[ix][0]
    if n == 'm':
        ml.append(demdata.columns[ix])

# <codecell>

#  Create list of Mains names and Circuit Names

ml_mains = []
ml_circuits = []
for ix, row in enumerate(ml):
    n = int(row.split('_')[1])
    if n == 0:
        ml_mains.append(ml[ix])
    else:
        ml_circuits.append(ml[ix])


        

# <headingcell level=2>

# Import dataset 2

# <codecell>

demdata2 = read_csv('allmetersdemandarray2.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdata2[demdata2 >= 1000] = np.nan
demdatacum2 = read_csv('allmeterscumdemandarray2.csv', delimiter=',',index_col =0,parse_dates = True)
creddata2  = read_csv('allmeterscreditarray2.csv', delimiter=',',index_col =0,parse_dates = True)
circlist2 = demdata2.columns.tolist()
datelist2_hr = demdata2.index.tolist()
r2, c2 = np.shape(demdata2)

ug = []
for ix in range(0,c2):
    n = demdata2.columns[ix][0]
    if n == 'u':
        ug.append(demdata2.columns[ix])

ug_mains = []
ug_circuits = []
for ix, row in enumerate(ug):
    n = int(row.split('_')[1])
    if n == 0:
        ug_mains.append(ug[ix])
    else:
        ug_circuits.append(ug[ix])


# <headingcell level=2>

# Data avaiability plot (Set 1)

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata[ml].ix[demdata[ml].index[0]:demdata[ml].index[-1]], aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(demdata[ml].columns)[0]))
densityplot.set_xticklabels(ml)
densityplot.set_yticks(range(0,r,750))
densityplot.set_yticklabels(datelist_hr[0:r:750])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution (Mali)')
plt.show()

# <headingcell level=2>

# Data avaiability plot (Set 2)

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata2, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(ug)[0]))
densityplot.set_xticklabels(demdata2.columns)
densityplot.set_yticks(range(0,r2,168))
densityplot.set_yticklabels(datelist2_hr[0:r:168])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution')
plt.show()

# <codecell>

# Historgram of Mean Daily Energy Usage subplot circuits

demdata_day_ml = demdata[ml].resample('D', how='sum')
demdata_day_ug = demdata2[ug].resample('D', how='sum')

# Mali 
fig = plt.figure()
cdemhisto =  fig.add_subplot(1,1,1)
cdemhisto.hist(demdata_day_ml.mean(),bins = 20, histtype='bar',range = (0,500))
cdemhisto.set_xlabel('Average Daily Energy Consumption (Wh)')
cdemhisto.set_ylabel('Number of Consumer Circuits')
cdemhisto.set_title('Histogram of Consumers by Mean Daily Energy Consumption (Mali)')
plt.show()


# Uganda
fig = plt.figure()
cdemhisto =  fig.add_subplot(1,1,1)
cdemhisto.hist(demdata_day_ug.mean(),bins = 20, histtype='bar',range = (0,500))
cdemhisto.set_xlabel('Average Daily Energy Consumption (Wh)')
cdemhisto.set_ylabel('Number of Consumer Circuits')
cdemhisto.set_title('Histogram of Consumers by Mean Daily Energy Consumption (Uganda)')
plt.show()


