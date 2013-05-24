import os
import datetime
import time
import sqlite3
import csv

in_path = '/home/mitchell/Documents/SharedSolar/SD_11_2012/db_files'
out_path = '/home/mitchell/Documents/SharedSolar/SD_11_2012/flat_files_yearly'

if __name__=="__main__":
	#for (dirpath,dirnames,filenames) in os.walk('C:\Users\Mitchell\Documents\Shared_Solar\Shared_Solar_database\sqllite'):
	for (dirpath,dirnames,filenames) in os.walk(in_path):
		for _file in filenames:

				if _file.find(".db") != -1:
					cktstart=_file.find("_")
					cktend=_file.rfind("_")
					site=_file[0:cktstart]
					#print "site="+site
					ckt=_file[cktstart+1:cktend]
					#print "circuit="+ckt
					print site +"_"+ ckt
					'''
					tableend=_file.rfind(".db")
					_table=_file[0:tableend]
					#print "tablename="+_table
					'''
					_table = "hour_res_watthours"		
					year =  _file.strip(".db").split("_")[-1]
					csvname = out_path+"/"+site+"_"+ckt+"_"+year+".csv"
					#print csvname
					fcsv = open(csvname,'a')
					wcsv = csv.writer(fcsv)
					conn=sqlite3.connect(dirpath+"/"+_file)
					c=conn.cursor()
					qry="select ts, wh from "+_table+" order by ts"

					for (ts, wh)  in c.execute(qry):
						#print str(ts)+";"+str(w)+";"+str(wh)+";"+str(cr)
						wcsv.writerow([str(ts)+";"+str(wh)])

					fcsv.close()
					conn.close()
					conn=None



