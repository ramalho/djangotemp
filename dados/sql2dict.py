#!/usr/bin/env python

from pprint import pprint
import MySQLdb
import pickle
db = MySQLdb.connect(host="localhost",user="librarian",passwd="nancy",db="groo")
tables = ('books', 'creators', 'l_book_creator')
catalog = {}
c = db.cursor()
for table in tables:
    c.execute("SELECT * FROM groo_" + table)
    print [d[0] for d in c.description]
    heads = [d[0] for d in c.description]
    c.fetchall()
    data = {}
    for i,row in enumerate(c):
        if table.startswith('l_'):
            key = (row[0],row[1])
        else:
            key = row[0] 
        data[key]= dict(zip(heads,[field for field in row]))
    catalog[table] = data
db.close()
dump = file('groo_catalog.pickle','wb')
pickle.dump(catalog, dump, 2)
dump.close()

