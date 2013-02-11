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
#Separate ML (dataset 1)

ml = []
ug1 = []
for ix in range(0,c):
	n = demdata.columns[ix][0]
	if n == 'm':
		ml.append(demdata.columns[ix])
	else:
		ug1.append(demdata.columns[ix])
	
#  Create list of Mains names and Circuit Names

ml_mains = []
ml_circuits = []
for ix, row in enumerate(ml):
    n = int(row.split('_')[1])
    if n == 0:
        ml_mains.append(ml[ix])
    else:
        ml_circuits.append(ml[ix])

# <codecell>

# Convert to Daily Resolution 

# Sum across hours to make daily resolution 
demdata_day = demdata.resample('D', how='sum')
mainsdf_day = demdata[ml_mains].resample('D', how='sum')
circuitsdf_day = demdata[ml_circuits].resample('D', how='sum')
datelist_day = demdata_day.index.tolist()
# Convert to Monthly Resolution

# Use Daily Average Energy 
demdata_month = demdata_day.resample('M', how='mean')
mainsdf_month = mainsdf_day.resample('M', how='mean')
circuitsdf_month= circuitsdf_day.resample('M', how='mean')
datelist_month = demdata_day.index.tolist()

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

ug2 = []
for ix in range(0,c2):
    n = demdata2.columns[ix][0]
    if n == 'u':
        ug2.append(demdata2.columns[ix])

ug2_mains = []
ug2_circuits = []
for ix, row in enumerate(ug2):
    n = int(row.split('_')[1])
    if n == 0:
        ug2_mains.append(ug2[ix])
    else:
        ug2_circuits.append(ug2[ix])

# <codecell>

# Convert to Daily Resolution 

# Sum across hours to make daily resolution 
demdata2_day = demdata2.resample('D', how='sum')
mainsdf2_day = demdata2[ug2_mains].resample('D', how='sum')
circuitsdf2_day = demdata2[ug2_circuits].resample('D', how='sum')
datelist2_day = demdata2_day.index.tolist()
# Convert to Monthly Resolution

# Use Daily Average Energy 
demdata2_month = demdata2_day.resample('M', how='mean')
mainsdf2_month = mainsdf2_day.resample('M', how='mean')
circuitsdf2_month= circuitsdf2_day.resample('M', how='mean')
datelist2_month = demdata2_day.index.tolist()

# <headingcell level=2>

# Import dataset 3 (1 and 2 merged)

# <codecell>

demdatam = read_csv('allmetersdemandarray_merged.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdatam[demdatam >= 1000] = np.nan
creddatam = read_csv('allmeterscreditarray_merged.csv', delimiter=',',index_col =0,parse_dates = True)
circlistm = demdatam.columns.tolist()
datelistm_hr = demdatam.index.tolist()
rm, cm = np.shape(demdatam)

ugm = []
for ix in range(0,cm):
    n = demdatam.columns[ix][0]
    if n == 'u':
        ugm.append(demdatam.columns[ix])

ugm_mains = []
ugm_circuits = []
for ix, row in enumerate(ugm):
    n = int(row.split('_')[1])
    if n == 0:
        ugm_mains.append(ugm[ix])
    else:
        ugm_circuits.append(ugm[ix])

# <codecell>

# Convert to Daily Resolution 

# Sum across hours to make daily resolution 
demdatam_day = demdatam.resample('D', how='sum')
mainsdfm_day = demdatam[ugm_mains].resample('D', how='sum')
circuitsdfm_day = demdatam[ugm_circuits].resample('D', how='sum')
datelistm_day = demdatam_day.index.tolist()
# Convert to Monthly Resolution

# Use Daily Average Energy 
demdatam_month = demdatam_day.resample('M', how='mean')
mainsdfm_month = mainsdfm_day.resample('M', how='mean')
circuitsdfm_month= circuitsdfm_day.resample('M', how='mean')
datelistm_month = demdatam_day.index.tolist()

# <headingcell level=2>

# Data avaiability plot (Set 1)

# <codecell>


fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
#densityplot.spy(demdata[ml].ix[demdata[ml].index[0]:demdata[ml].index[-1]], aspect = 'auto')
densityplot.spy(demdata[ug1].ix[demdata[ug1].index[8760]:demdata[ug1].index[-1]], aspect = 'auto')
#densityplot.set_xticks(range(0,np.shape(demdata[ml].columns)[0]))
densityplot.set_xticks(range(0,np.shape(demdata[ug1].columns)[0]))
#densityplot.set_xticklabels(ml)
densityplot.set_xticklabels(ug1)
#densityplot.set_yticks(range(0,r,750))
densityplot.set_yticks(range(0,r2,750))

densityplot.set_yticklabels(datelist2_hr[0:r2:750])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution (Set 1)')
plt.show()

# <headingcell level=2>

# Data avaiability plot (Set 2)

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata2, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(ug2)[0]))
densityplot.set_xticklabels(demdata2.columns)
densityplot.set_yticks(range(0,r2,168))
densityplot.set_yticklabels(datelist2_hr[0:r:168])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution (Set 2)')
plt.show()

# <headingcell level=2>

# Data avaiability plot Uganda Merged (Set 3)

# <codecell>

fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdatam, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(ugm)[0]))
densityplot.set_xticklabels(demdatam.columns)
densityplot.set_yticks(range(0,rm,24))
densityplot.set_yticklabels(datelistm_hr[0:r:24])
densityplot.set_xlabel('Mains and Circuits')
densityplot.set_ylabel('Date and Time')
densityplot.set_title('Data Availablity at Hourly Resolution (Merged)')
plt.show()

# <headingcell level=2>

# Monthly Data Availability Maps

# <codecell>

# Mali Mains
mdateaxis = []
for ix, name in enumerate(circuitsdf_month.index):
    mdateaxis.append(name.strftime("%m-%Y"))


fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
densityplot.spy(mainsdf_month, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(mainsdf_month.columns)[0]))
densityplot.set_xticklabels(mainsdf_month.columns)
densityplot.set_yticks(range(0,np.shape(mainsdf_month.index)[0]))
densityplot.set_yticklabels(mdateaxis)
densityplot.plot()

# Mali Circuits (Part 1)
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
densityplot.spy(circuitsdf_month[ml_circuits[12:92]], aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(ml_circuits[12:92])[0]))
densityplot.set_xticklabels(ml_circuits[12:92],rotation = 'vertical')
densityplot.tick_params(axis='x', which='major', labelsize=12)
densityplot.set_yticks(range(0,np.shape(circuitsdf_month.index)[0]))
densityplot.set_yticklabels(mdateaxis)
densityplot.plot()


# Mali Circuits (Part 2)
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
densityplot.spy(circuitsdf_month[ml_circuits[92:]], aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(ml_circuits[92:])[0]))
densityplot.set_xticklabels(ml_circuits[92:],rotation = 'vertical')
densityplot.tick_params(axis='x', which='major', labelsize=12)
densityplot.set_yticks(range(0,np.shape(circuitsdf_month.index)[0]))
densityplot.set_yticklabels(mdateaxis)
densityplot.plot()




# Uganda Mains

udateaxis = []
for ix, name in enumerate(circuitsdfm_month.index):
    udateaxis.append(name.strftime("%m-%Y"))


fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
densityplot.spy(mainsdfm_month, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(mainsdfm_month.columns)[0]))
densityplot.set_xticklabels(mainsdfm_month.columns)
densityplot.set_yticks(range(0,np.shape(mainsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.plot()

# Uganda Circuits
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
densityplot.spy(circuitsdfm_month, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(circuitsdfm_month.columns)[0]))
densityplot.set_xticklabels(circuitsdfm_month.columns,rotation='vertical')
densityplot.set_yticks(range(0,np.shape(circuitsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.plot()


# <codecell>


# <codecell>


# <codecell>


# <codecell>


# <codecell>


