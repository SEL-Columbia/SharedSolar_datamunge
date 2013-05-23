import os
import datetime
import time
import sqlite3
import csv


if __name__=="__main__":
   for (dirpath,dirnames,filenames) in os.walk('C:\Users\Mitchell\Documents\Shared_Solar\Shared_Solar_database\sqllite'):
      
      for _file in filenames:
         print _file
         prev="0123456789z"
         curr=""
         
         if _file.find("_ts.db")==-1:
           cktstart=_file.find("_")
           cktend=_file.rfind("_")
           site=_file[0:cktstart]
           #print "site="+site
           ckt=_file[cktstart+1:cktend]
           #print "circuit="+ckt
           tableend=_file.rfind(".db")
           _table=_file[0:tableend]
           #print "tablename="+_table
           csvname = site+"_"+ckt+".csv"
           print csvname
           fcsv = open(csvname,'a')
           wcsv = csv.writer(fcsv)
           conn=sqlite3.connect(dirpath+"/"+_file)
           c=conn.cursor()
           qry="select timestamp,watts,watthourssc20,credit from "+_table+" order by timestamp"
   
           for (ts,w,wh,cr)  in c.execute(qry):
              #print str(ts)+";"+str(w)+";"+str(wh)+";"+str(cr)
              wcsv.writerow([str(ts)+";"+str(w)+";"+str(wh)+";"+str(cr)])

           fcsv.close()
           conn.close()
           conn=None
         

      
