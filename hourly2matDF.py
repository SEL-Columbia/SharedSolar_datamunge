# Mitchell Lee
# Shared Solar 
# Read all houlry flat csv files and write them to a single .mat file
# Began Script on November 29, 2012

# list all csv files

import os
import numpy as np
import datetime
import dateutil.parser as dp
import string as st
import csv
import pandas as pd


outpath = '/home/mitchell/Documents/SharedSolar/SharedSolar_datamunge'
flist = []
csv_files_flat_hourly = '/home/mitchell/Documents/SharedSolar/data/csv_flat_files_hourly'
## find files containing hourly demand and credit data for all meters
for (dirpath,dirnames,filenames) in os.walk('/home/mitchell/Documents/SharedSolar/data'):
    if dirpath == csv_files_flat_hourly:
        for _file in filenames:
            flist.append(_file) 

r = np.shape(flist)

## generate the list of dates for timeseries index
d0 = datetime.datetime(2010,1,1,0)
d1 = datetime.datetime(2012,12,31,23)
datelist = pd.date_range(d0,d1,freq='1h')
dr =  int((d1 - d0).days)*24 +24.

## generate column headers for DataFrame

loclist = []
for jdx, row in enumerate(range(0,r[0])):
    loc = st.rstrip(st.lstrip(flist[jdx],'hourl'),'.csv')
    loc = st.lstrip(loc,'y')
    loclist.append(loc)

## create empty arrays for cummulative demand and credit timeseries
demmatcum = np.zeros((r[0],dr)); demmatcum[:] = np.nan
credmat = np.zeros((r[0],dr)); credmat[:] = np.nan
    
for jdx, filnum in enumerate(range(0,r[-1])):
    f1 = open(csv_files_flat_hourly+ "/" + flist[filnum],'r')
    f1reader = csv.reader(f1, delimiter = ';')

    for idx, row in enumerate(f1reader):
        date = dp.parse(row[0])
        diff = date - d0
        k = int(date.hour)
   	c = int(diff.days)*24 + k
        demmatcum[filnum,c] = float(row[1])
        credmat[filnum,c] = float(row[2])
    print filnum
    f1.close()
demmatcum = demmatcum.T
credmat = credmat.T


## make accumulative demand and non accumulative demand
r,c = np.shape(demmatcum) # Appropriately rename rows and columns
demmat= np.zeros((r,c)); demmat[:] = np.nan

for jx in range(0,c):
    for ix in range(0,r):
        if ix == 0:
            demmat[ix,jx] = demmatcum[ix,jx]
            lastreal = 0
        else:
            nancheck = np.isnan(demmatcum[ix,jx])
            if nancheck == 1:
                demmat[ix,jx] = demmatcum[ix,jx]
            else:
                demmat[ix,jx] = demmatcum[ix,jx]-lastreal
                lastreal = demmatcum[ix,jx]


## Put together DataFrames
demDFcum   = pd.DataFrame(demmatcum,index = pd.DatetimeIndex(datelist), columns = loclist)
demDF  = pd.DataFrame(demmat,index = pd.DatetimeIndex(datelist), columns = loclist)
credDF = pd.DataFrame(credmat,index = pd.DatetimeIndex(datelist), columns = loclist)

## Alphabetize Columns

demDFcum   = demDFcum.reindex_axis(sorted(demDFcum.columns), axis=1)
demDF  = demDF.reindex_axis(sorted(demDF.columns), axis=1)
credDF  = credDF.reindex_axis(sorted(credDF.columns), axis=1)

## Back up DataFrames as csv 
demDF.to_csv('allmetersdemandarray.csv', index_label = 'dates' )
demDFcum.to_csv('allmeterscumdemandarray.csv', index_label = 'dates' )
credDF.to_csv('allmeterscreditarray.csv',index_label = 'dates' )

