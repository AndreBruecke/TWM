from hdbcli import dbapi
import numpy as np
import pandas as pd
import time

#connection = dbapi.connect('192.168.56.102', 39041, 'SYSTEM', 'Password1')
#cursor = connection.cursor()

#cursor.execute('select count(distinct (DOCUMENT_ID)) from "SYSTEM"."ZA_METACONTENT"')
#print(cursor.fetchall())

#chapterDf = pd.read_csv("/media/sf_Shared/Git/data/GutenbergGenres.csv")
#chapterDf = chapterDf[(chapterDf.genre != "Natur, Wissen und Reise") & (chapterDf.genre != "Kultur und Kunst")]

#print(len(chapterDf))
#print(chapterDf.head())

hana = pd.read_csv("/media/sf_Shared/Git/data/hana/data_100.csv")
print(hana.head(10))
