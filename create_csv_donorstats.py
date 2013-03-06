"""
Mitchell Lee
SharedSolar
Create csv Files for Report to Donor
"""

import numpy as np
import pandas as pd

execfile('gw_data_stats.py')

# Create DataFrames to Manipulate
gw_wh, gw_cred, SD_wh, SD_cred, SDgw_wh, SDgw_cred = open_SSdata()

#Typical Duirnal Day 

make_typday(SDgw_wh.ix['2011-9-14 00:00:00':'2012-10-01 00:00:00'])['ug01_6'].to_csv('ug01_6typday.csv')

make_typday(SDgw_wh.ix['2011-11-1 00:00:00':'2013-01-31 23:59:00'])['ml01_13'].to_csv('ml01_13typday.csv')

make_typday(SDgw_wh.ix['2011-06-01 00:00:00':'2013-01-31 23:59:00'])['ug02_6'].to_csv('ug02_6typday.csv')

make_typday(SDgw_wh.ix['2012-03-01 00:00:00':'2012-06-01 00:00:00'])['ml08_16'].to_csv('ml08_16typday.csv')

make_typday(SDgw_wh.ix['2011-10-01 00:00:00':'2013-01-01 00:00:00'])['ug03_2'].to_csv('ug03_2typday.csv')


#Maximum Duirnal Day

make_maxday(SDgw_wh.ix['2011-9-14 00:00:00':'2012-10-01 00:00:00'])['ug01_6'].to_csv('ug01_6maxday.csv')

make_maxday(SDgw_wh.ix['2011-11-1 00:00:00':'2013-01-31 23:59:00'])['ml01_13'].to_csv('ml01_13tmaxday.csv')

make_maxday(SDgw_wh.ix['2011-06-01 00:00:00':'2013-01-31 23:59:00'])['ug02_6'].to_csv('ug02_6maxday.csv')

make_maxday(SDgw_wh.ix['2012-03-01 00:00:00':'2012-06-1 00:00:00'])['ml08_16'].to_csv('ml08_16maxday.csv')

make_maxday(SDgw_wh.ix['2011-10-01 00:00:00':'2013-01-01 00:00:00'])['ug03_2'].to_csv('ug03_2maxday.csv')


#Average Daily Total

make_m_from_h(SDgw_wh.ix['2011-9-14 00:00:00':'2012-10-01 00:00:00'])[0]['ug01_6'].to_csv('ug01_6dayen.csv')

make_m_from_h(SDgw_wh.ix['2011-11-1 00:00:00':'2013-01-31 23:59:00'])[0]['ml01_13'].to_csv('ml01_13dayen.csv')

make_m_from_h(SDgw_wh.ix['2011-06-01 00:00:00':'2013-01-31 23:59:00'])[0]['ug02_6'].to_csv('ug02_6dayen.csv')

make_m_from_h(SDgw_wh.ix['2012-03-01 00:00:00':'2012-06-1 00:00:00'])[0]['ml08_16'].to_csv('ml08_16dayen.csv')

make_m_from_h(SDgw_wh.ix['2011-10-01 00:00:00':'2013-01-01 00:00:00'])[0]['ug03_2'].to_csv('ug03_2dayen.csv')


#Peak Power

SDgw_wh['2011-09-14 00:00:00':'2012-10-01 00:00:00'].resample('M', how = 'max')['ug01_6'].dropna().to_csv('ug01_6_day_peakpow.csv')

SDgw_wh['2011-11-01 00:00:00':'2012-02-01 00:00:00'].resample('M', how = 'max')['ml01_13'].dropna().to_csv('ml01_13_day_peakpow.csv')

SDgw_wh['2011-01-01 00:00:00':'2012-02-01 00:00:00'].resample('M', how = 'max')['ug02_6'].dropna().to_csv('ug02_6_day_peakpow.csv')

SDgw_wh['2012-03-01 00:00:00':'2012-06-01 00:00:00'].resample('M', how = 'max')['ml08_16'].dropna().to_csv('ml08_16_day_peakpow.csv')

SDgw_wh['2011-10-01 00:00:00':'2013-01-01 00:00:00'].resample('M', how = 'max')['ug03_2'].dropna().to_csv('ug03_2_day_peakpow.csv')



#Total Electricity Payments by Month

purch_rec = make_purch_rec(SDgw_wh)

purch_rec['2011-9-14 00:00:00':'2012-10-01 00:00:00'].resample('M', how = 'sum')['ug01_6'].dropna().to_csv('ug01_6_day_purchrec.csv')

purch_rec['2011-11-01 00:00:00':'2012-02-01 00:00:00'].resample('M', how = 'sum')['ml01_13'].dropna().to_csv('ml01_13_day_purchrec.csv')

purch_rec['2011-01-01 00:00:00':'2012-02-01 00:00:00'].resample('M', how = 'sum')['ug02_6'].dropna().to_csv('ug02_6_day_purchrec.csv')

purch_rec['2012-03-01 00:00:00':'2012-6-01 00:00:00'].resample('M', how = 'sum')['ml08_16'].dropna().to_csv('ml08_16_day_purchrec.csv')

purch_rec['2011-10-01 00:00:00':'2013-01-01 00:00:00'].resample('M', how = 'sum')['ug03_2'].dropna().to_csv('ug03_2_day_purchrec.csv')



