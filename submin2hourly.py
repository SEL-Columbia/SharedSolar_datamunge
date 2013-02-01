# Mitchell Lee
# Shared Solar 
# Read all flat csv files and convert them into hourly resolution
# Also write two matlab arrays. One with the demand data from all 
# circuits and an array with consumer credit at the beginning of each hour
# Script began on Nov 20, 2012

# list all csv files

import os
import numpy as np
import datetime
import dateutil.parser as dp
import csv

#outpath = 'C:\Users\Mitchell\Documents\Shared_Solar\Shared_Solar_database\csv_flat_files_hourly3'

outpath = '/home/mitchell/Documents/SharedSolar'
flist = []

#csv_files_flat = 'C:\Users\Mitchell\Documents\Shared_Solar\Shared_Solar_database\csv_flat_files2'
csv_files_flat = '/media/Windows7_OS/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database/csv_flat_files2'


#'C:\Users\Mitchell\Documents\Shared_Solar\Shared_Solar_database'
for (dirpath,dirnames,filenames) in os.walk('/media/Windows7_OS/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database'):
    if dirpath == csv_files_flat:
        for _file in filenames:
            flist.append(_file) 
         
n = np.shape(flist)

for jdx, r in enumerate(range(54,55)):#n[-1])):
    f1 = open(csv_files_flat+ "/" + flist[r],'r')
    fhr = open(outpath+ "/hourly" + flist[r],'wb')
    f1reader = csv.reader(f1, delimiter = ';')
    fhrwriter = csv.writer(fhr, delimiter = ';')

    Ercd = 0.
    E1 = 0.
    E2 = 0.
    for idx, row in enumerate(f1reader):
		date2 = dp.parse(row[0])
		if idx == 0:
			date1 = datetime.datetime(1,1,1,1,1,1)

		if date2 != date1:
			year = date2.year; month = date2.month; day = date2.day
			hour = date2.hour; minute = date2.minute; second = date2.second

			E2 = float(row[2])
			# logic to get rid of duplicate time stamps
			# automatically takes first stamp
			diff = (date2 - date1).seconds
			if E2 >= E1:
				# If there is a energy reading that is too big
				# dump the reading
				pwr = (E2-E1)/(diff/3600.)
				if 0 <=pwr <=750:
					Ercd = Ercd + E2 - E1                    
							  
			else:
				"""
				delta_E = E1-E2
				if delta_E > 1:
					pwr = E2/(diff/3600.)
					if  0<= pwr <=1000:
						Ercd = Ercd + E2
						#print Ercd
						print E2, delta_E
				"""		
			E1 = E2
                    
			if idx == 0:
				oldhour = hour
				credithrly = float(row[3]) #write credit for the beginning of the first
            
			if oldhour != hour:
				#Append hourly text file 
				datehrly = datetime.datetime(oldyear,oldmonth,oldday,oldhour) #form date stamp
				fhrwriter.writerow([datehrly,Ercd_old,credithrly])
                #print np.array([datehrly,Ercd,credithrly])
				credithrly = float(row[3]) #write credit for the beginning of the next hour
		Ercd_old = Ercd 		
		date1 = date2
		oldhour = hour
		oldday = day
		oldmonth = month
		oldyear = year
    print flist[r]
    f1.close()
    fhr.close()

    
