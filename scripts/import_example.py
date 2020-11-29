from hdbcli import dbapi
import numpy as np
import pandas as pd
import time

connection = dbapi.connect('192.168.56.101', 39041, 'SYSTEM', 'Password1')
cursor = connection.cursor()


chapterDf = pd.read_csv("/media/sf_Shared/Git/data/GutenbergGenres.csv")
print(len(chapterDf))

"""
sqlMetacontent = 'insert into "SYSTEM"."ZA_METACONTENT" (DOCUMENT_ID, TITLE, AUTHOR) VALUES (?,?,?)'
sqlLabel = 'insert into "SYSTEM"."ZA_LABEL" (DOCUMENT_ID, LABEL_NAME) VALUES (?,?)'
sqlContent = 'insert into "SYSTEM"."ZA_CHAPTER" (DOCUMENT_ID, FULLTEXT) VALUES (?,?)'


for index, row in chapterDf.iterrows():
    print(index)
    cursor.execute(sqlMetacontent, (int(index), str(row['title'])[0:97], str(row['author'])))
    cursor.execute(sqlLabel, (index, row['genre']))
    cursor.execute(sqlContent, (index, str(row['chapter'])))
    time.sleep(0.1)
"""

#cursor.execute('select count(distinct (DOCUMENT_ID)) from "SYSTEM"."ZA_METACONTENT"')
#print(cursor.fetchall())

#cursor.execute('select top 10 * from SYSTEM.CMPL100K')
#for row in cursor:
#    print(row[1])
