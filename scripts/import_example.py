from hdbcli import dbapi
import numpy as np
import pandas as pd
import time

connection = dbapi.connect('192.168.56.102', 39041, 'SYSTEM', 'Password1')
cursor = connection.cursor()


chapterDf = pd.read_csv("/media/sf_Shared/Git/data/GutenbergGenres.csv")
print(len(chapterDf))

sqlMetacontent = 'insert into "SYSTEM"."ZA_METACONTENT" (DOCUMENT_ID, TITLE, AUTHOR) VALUES (?,?,?)'
sqlLabel = 'insert into "SYSTEM"."ZA_LABEL" (DOCUMENT_ID, LABEL_NAME) VALUES (?,?)'
sqlContent = 'insert into "SYSTEM"."ZA_CHAPTER" (DOCUMENT_ID, FULLTEXT) VALUES (?,?)'


for index, row in chapterDf.iterrows():
    cursor.execute(sqlMetacontent, (int(index), str(row['title'])[0:97], str(row['author'])))
    cursor.execute(sqlLabel, (index, row['genre']))
    cursor.execute(sqlContent, (index, str(row['chapter'])))
    time.sleep(0.1)
