# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Comparing UG Data Before and After Update: Mitchell Lee

# <codecell>

import pandas as pd
import numpy as np
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import dateutil.parser as dp
import string


# <codecell>

#cd "C:/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database"

# <headingcell level=2>

# Import dataset 1

# <codecell>

demdata = pd.read_csv('allmetersdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdata[demdata >= 1000] = np.nan
demdatacum = pd.read_csv('allmeterscumdemandarray.csv', delimiter=',',index_col =0,parse_dates = True)
creddata  = pd.read_csv('allmeterscreditarray.csv', delimiter=',',index_col =0,parse_dates = True)
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

demdata2 = pd.read_csv('allmetersdemandarray2.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
demdata2[demdata2 >= 1000] = np.nan
demdatacum2 = pd.read_csv('allmeterscumdemandarray2.csv', delimiter=',',index_col =0,parse_dates = True)
creddata2  = pd.read_csv('allmeterscreditarray2.csv', delimiter=',',index_col =0,parse_dates = True)
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

demdatam = pd.read_csv('allmetersdemandarray_merged.csv', delimiter=',',index_col =0,parse_dates = True)
# If the hourly demand is greater than 1000 Wh replace with nan
#demdatam[demdatam >= 1000] = np.nan
creddatam = pd.read_csv('allmeterscreditarray_merged.csv', delimiter=',',index_col =0,parse_dates = True)
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
datelistm_month = demdatam_month.index.tolist()


# <headingcell level=2>

# Count Circuits

# <codecell>

# Uganda
ugcount_idx = []
for ix, m in enumerate(ugm_circuits):
        ugcount_idx.append(string.split(m,'_')[0])

ugcount_idx = np.sort(list(set(ugcount_idx)))
ugcount = pd.Series(np.zeros(np.shape(ugcount_idx)[0]),index = ugcount_idx)

for ix,circ in enumerate(ugm_circuits):
        ugcount[string.split(circ,'_')[0]] += 1

# Mali
mlcount_idx = []
for ix, m in enumerate(ml_circuits):
        mlcount_idx.append(string.split(m,'_')[0])

mlcount_idx = np.sort(list(set(mlcount_idx)))
mlcount = pd.Series(np.zeros(np.shape(mlcount_idx)[0]),index = mlcount_idx)

for ix,circ in enumerate(ml_circuits):
        mlcount[string.split(circ,'_')[0]] += 1

# <headingcell level=2>

# Create Dictionary of Circuits in Each Main

# <codecell>

site_dict = {}
ugm_mains.append('ug05_0')
site_list = np.sort(ugm_mains)

for ix, site in enumerate(site_list):
	site_dict[string.split(site,'_')[0]] = []

for ix, circ in enumerate(ugm_circuits):
	site_dict[string.split(circ,'_')[0]].append(circ)

site_list = np.sort(site_dict.keys())

# <headingcell level=2>

# Create Mains by summing circuits

# <codecell>

ugm_cirsum = pd.DataFrame(index = datelistm_hr)

for ix, site in enumerate(site_list):
	dftemp = pd.DataFrame(demdatam[site_dict[site]].sum(axis = 1), columns = [site])
	ugm_cirsum = ugm_cirsum.join(dftemp)


ugm_cirsumday = ugm_cirsum.resample('D', how='sum')
ugm_cirsummonth = ugm_cirsumday.resample('M', how='mean')
udateaxis = []
for ix, name in enumerate(circuitsdfm_month.index):
    udateaxis.append(name.strftime("%m-%Y"))

ugm_cirsummonth = ugm_cirsummonth.rename(index = dict(zip(datelistm_month, udateaxis)))

ugm_cirsummonth.plot(kind = 'bar', stacked =True)
plt.title('Net Daily Average Energy Usage')
plt.ylabel('Cumulative Wh')

ugm_cirsummonth2 = np.array(ugm_cirsummonth)

for jx in range(0, np.shape(ugm_cirsummonth2)[1]):
	for ix in range(0, np.shape(ugm_cirsummonth2)[0]):
		if ix!=0 and np.isnan(ugm_cirsummonth2[ix,jx]) == True:
			ugm_cirsummonth2[ix,jx] = ugm_cirsummonth2[ix-1,jx]



ugm_cirsummonth2 = pd.DataFrame(ugm_cirsummonth2, index = udateaxis, columns = ugm_cirsummonth.columns)
ugm_cirsummonth2.plot(kind = 'bar', stacked =True)
plt.title('Net Daily Average Energy Usage (Gaps Filled)')
plt.ylabel('Cumulative Wh')

"""

# <headingcell level=2>

# Data avaiability plot (Set 1)

# <codecell>


fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.spy(demdata[ml].ix[demdata[ml].index[0]:demdata[ml].index[-1]], aspect = 'auto')
#densityplot.spy(demdata[ug1].ix[demdata[ug1].index[8760]:demdata[ug1].index[-1]], aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(demdata[ml].columns)[0]))
#densityplot.set_xticks(range(0,np.shape(demdata[ug1].columns)[0]))
densityplot.set_xticklabels(ml)
#densityplot.set_xticklabels(ug1)
densityplot.set_yticks(range(0,r,750))
#densityplot.set_yticks(range(0,r2,24))
densityplot.set_yticklabels(datelist_hr[0:r:750])
#densityplot.set_yticklabels(datelist2_hr[0:r2:24])
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
densityplot.set_yticks(range(0,r2,24))
densityplot.set_yticklabels(datelist2_hr[0:r:24])
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
densityplot.set_xticklabels(demdatam.columns,rotation = 'vertical')
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
#densityplot.spy(mainsdf_month, aspect = 'auto')
pic = densityplot.imshow(mainsdf_month[ml_mains[1:]], aspect = 'auto', cmap= mpl.cm.jet)
densityplot.set_xticks(range(0,np.shape(ml_mains[1:])[0]))
densityplot.set_xticklabels(ml_mains[1:])
densityplot.set_yticks(range(0,np.shape(mainsdf_month.index)[0]))
densityplot.set_yticklabels(mdateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time')
densityplot.set_xlabel('Mali Location')
densityplot.set_ylabel('Month')
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily')
densityplot.plot()

# Mali Circuits (Part 1)
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(circuitsdf_month[ml_circuits[12:92]], aspect = 'auto')
pic = densityplot.imshow(circuitsdf_month[ml_circuits[12:92]], aspect = 'auto')
pic.set_clim(0.0,150)
densityplot.set_xticks(range(0,np.shape(ml_circuits[12:92])[0]))
densityplot.set_xticklabels(ml_circuits[12:92],rotation = 'vertical')
densityplot.tick_params(axis='x', which='major', labelsize=12)
densityplot.set_yticks(range(0,np.shape(circuitsdf_month.index)[0]))
densityplot.set_yticklabels(mdateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time',fontsize =22)
densityplot.set_xlabel('Mali Circuit',fontsize =22)
densityplot.set_ylabel('Month',fontsize =22)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =22)
densityplot.plot()


# Mali Circuits (Part 2)
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(circuitsdf_month[ml_circuits[92:]], aspect = 'auto')
pic = densityplot.imshow(circuitsdf_month[ml_circuits[92:]], aspect = 'auto')
pic.set_clim(0.0,150)
densityplot.set_xticks(range(0,np.shape(ml_circuits[92:])[0]))
densityplot.set_xticklabels(ml_circuits[92:],rotation = 'vertical')
densityplot.tick_params(axis='x', which='major', labelsize=12)
densityplot.set_yticks(range(0,np.shape(circuitsdf_month.index)[0]))
densityplot.set_yticklabels(mdateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time', fontsize =22)
densityplot.set_xlabel('Mali Circuit',fontsize =22)
densityplot.set_ylabel('Month',fontsize =22)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =22)
densityplot.plot()



# Uganda Mains

udateaxis = []
for ix, name in enumerate(circuitsdfm_month.index):
    udateaxis.append(name.strftime("%m-%Y"))


fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(mainsdfm_month, aspect = 'auto')
pic = densityplot.imshow(mainsdfm_month, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(mainsdfm_month.columns)[0]))
densityplot.set_xticklabels(mainsdfm_month.columns)
densityplot.set_yticks(range(0,np.shape(mainsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time', fontsize =18)
densityplot.set_xlabel('Uganda Mains',fontsize =18)
densityplot.set_ylabel('Month',fontsize =18)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =18)
densityplot.plot()

# Uganda Circuits
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(circuitsdfm_month, aspect = 'auto')
pic = densityplot.imshow(circuitsdfm_month, aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(circuitsdfm_month.columns)[0]))
densityplot.set_xticklabels(circuitsdfm_month.columns,rotation='vertical')
densityplot.set_yticks(range(0,np.shape(circuitsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time', fontsize =18)
densityplot.set_xlabel('Uganda Circuits',fontsize =18)
densityplot.set_ylabel('Month',fontsize =18)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =18)
densityplot.plot()

# Uganda Circuits Lowest Third
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(circuitsdfm_month, aspect = 'auto')
pic = densityplot.imshow(circuitsdfm_month[np.sort(circuitsdfm_day.mean())[0:22].index] , aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(circuitsdfm_month[np.sort(circuitsdfm_day.mean())[0:22].index])[0]))
densityplot.set_xticklabels(np.sort(circuitsdfm_day.mean())[0:22].index,rotation='vertical')
densityplot.set_yticks(range(0,np.shape(circuitsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time (Lowest Third)', fontsize =18)
densityplot.set_xlabel('Uganda Circuits',fontsize =18)
densityplot.set_ylabel('Month',fontsize =18)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =18)
densityplot.plot()

# Uganda Circuits Upper Third
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(circuitsdfm_month, aspect = 'auto')
pic = densityplot.imshow(circuitsdfm_month[np.sort(circuitsdfm_day.mean())[46:67].index] , aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(circuitsdfm_month[np.sort(circuitsdfm_day.mean())[46:67].index])[0]))
densityplot.set_xticklabels(np.sort(circuitsdfm_day.mean())[46:67].index,rotation='vertical')
densityplot.set_yticks(range(0,np.shape(circuitsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time (Upper Third)', fontsize =18)
densityplot.set_xlabel('Uganda Circuits',fontsize =18)
densityplot.set_ylabel('Month',fontsize =18)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =18)
densityplot.plot()

# Uganda Circuits Middle Third
fig = plt.figure()
densityplot = fig.add_subplot(1,1,1)
densityplot.grid(True)
#densityplot.spy(circuitsdfm_month, aspect = 'auto')
pic = densityplot.imshow(circuitsdfm_month[np.sort(circuitsdfm_day.mean())[23:45].index] , aspect = 'auto')
densityplot.set_xticks(range(0,np.shape(circuitsdfm_month[np.sort(circuitsdfm_day.mean())[23:45].index])[0]))
densityplot.set_xticklabels(np.sort(circuitsdfm_day.mean())[23:45].index,rotation='vertical')
densityplot.set_yticks(range(0,np.shape(circuitsdfm_month.index)[0]))
densityplot.set_yticklabels(udateaxis)
densityplot.set_title('Average Daily Energy Consumption over Time (Middle Third)', fontsize =18)
densityplot.set_xlabel('Uganda Circuits',fontsize =18)
densityplot.set_ylabel('Month',fontsize =18)
pic.set_interpolation('nearest')
fig.colorbar(pic).set_label('Average Wh Consumed Daily',fontsize =18)
densityplot.plot()

"""

# <headingcell level=2>

#Show all figures

# <codecell>

plt.show()

