# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# SharedSolar Operational Data Analysis: Creating Load Duration Curves

# <headingcell level=2>

# Mitchell Lee 

# <codecell>

import pandas as pd
import numpy as np
import re
import matplotlib
import matplotlib.pyplot as plt
import dateutil.parser as dp
pd.set_option('display.notebook_repr_html', False)

# <codecell>

#cd "C:/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database"

# <headingcell level=2>

# Import csv file as dataframe

# <codecell>

demdata = pd.read_csv('allmetersdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdata[demdata >= 1000] = np.nan
demdatacum = pd.read_csv('allmeterscumdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
creddata  = pd.read_csv('allmeterscreditarray.csv', delimiter=',',index_col =0,parse_dates = True)
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

# Plot the Load Duration Curve for any Main

# <codecell>

main2plot = demdata['ug01_0'].dropna()
main2plot = pd.Series.order(main2plot, ascending = False)
length = np.shape(main2plot)[0]

bar_color = []

for ix,val in enumerate(main2plot):
    dateck = main2plot.index[ix].hour
    if  7 < dateck < 19:
        bar_color.append('r')
    else:
        bar_color.append('b')
            
plt.bar(range(0,length),main2plot, color = bar_color)
plt.ylabel('Hourly Energy (Wh)')
plt.title('Load Duration Curve (Blue = Night, Red = Day)')




