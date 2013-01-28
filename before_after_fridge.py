# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Compare ML06 and ML08 Before and After Refrigerator Installation

# <headingcell level=2>

# By: Mitchell Lee

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

# Plot entire ML06 or ML08 timeseries

# <codecell>
"""
ts = Series(demdata['ml08_0'].dropna())
fig = plt.figure()
tsplt =  fig.add_subplot(1,1,1)

ts.plot()
#tsplt.set_xticks(range(0,np.shape(ts)[-1]))
#tsplt.set_xticklabels(ts.index)
tsplt.set_xlabel('Time Series')
tsplt.set_ylabel('Energy (Wh)')
"""
# <headingcell level=2>

# Separate Before and After Refrigerator Installation

# <codecell>

#location of interest 
mains = 'ml06_0'
# Before Refrigerator
demdataBef = demdata[mains].truncate(after = '12/31/2011 23:00:00')
# After Refrigerator
demdataAft = demdata[mains].truncate(before = '01/01/2012 00:00:00')

# <headingcell level=2>

# Make Mean Daily Profile for Before and After Refrigerator Installation

# <codecell>

profBef = np.zeros(24)
profAft = np.zeros(24)
hourBef = demdataBef.index.hour
hourAft = demdataAft.index.hour

for ix in range(0,24):
    selectorBef = (hourBef == ix)
    selectorAft = (hourAft == ix)
    profBef[ix] = demdataBef[selectorBef].mean()
    profAft[ix] = demdataAft[selectorAft].mean()

# <codecell>

plt.plot(profAft)
plt.plot(profBef)
plt.xlabel('Hour of Day')
plt.ylabel('Energy (Whr)')
plt.title('ML06: Daily Profile Before and After Freezer Installation')
plt.legend(['After','Before'],loc = 'best')
plt.show()

# <codecell>


# <codecell>


