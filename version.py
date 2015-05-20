#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(host='localhost', port=5432, database='learn_django', user='django', password='django') 
    cur = con.cursor()
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print (ver)    
    

except psycopg2.DatabaseError (e):
    print ('Error to connect %d'%e)    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
