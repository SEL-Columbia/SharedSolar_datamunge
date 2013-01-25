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

# Separate UG and ML (dataset 1)

# <codecell>

#  Create list of Mains names and Circuit Names
ml = []
ug = []
for ix in range(0,c):
    n = demdata.columns[ix][0]
    if n == 'u':
        ug.append(demdata.columns[ix])
    else:
        ml.append(demdata.columns[ix])

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

# <headingcell level=2>

# Data avaiability plot (Set 1)

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata[ug].ix[demdata2.index[0]:demdata2.index[-1]], aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(demdata2.columns)[0]))
densityplot.set_xticklabels(ug)
densityplot.set_yticks(range(0,r2,24))
densityplot.set_yticklabels(datelist2_hr[0:r:24])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution (Dataset 1)')
plt.show()

# <headingcell level=2>

# Data avaiability plot (Set 2)

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata2, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(ug)[0]))
densityplot.set_xticklabels(demdata2.columns)
densityplot.set_yticks(range(0,r2,24))
densityplot.set_yticklabels(datelist2_hr[0:r:24])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution (Dataset 2)')
plt.show()

# <codecell>


