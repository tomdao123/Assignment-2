import pandas as pd
import csv 

#read data from csv files
df_dt1 = pd.read_csv("CSV1.csv")
df_dt2 = pd.read_csv("CSV2.csv")
df_dt3 = pd.read_csv("CSV3.csv")
df_dt4 = pd.read_csv("CSV4.csv")

#get exact column name for each csv file        
column_name_dt1 = 'SHORT-TEXT'
column_name_dt2 = 'TEXT'
column_name_dt3 = 'TEXT'
column_name_dt4 = 'TEXT'

#get text from text column
if column_name_dt1 in df_dt1.columns:
    text_column1 = df_dt1[column_name_dt1].dropna()
    
if column_name_dt2 in df_dt2.columns:
    text_column2 = df_dt2[column_name_dt2].dropna()

if column_name_dt3 in df_dt3.columns:
    text_column3 = df_dt3[column_name_dt3].dropna()  

if column_name_dt4 in df_dt4.columns:
    text_column4 = df_dt4[column_name_dt4].dropna()  

#create .txt file and write text from .csv files to .txt file
text_column = (text_column1, text_column2, text_column3, text_column4)    
with open('texts.txt', 'w', encoding='utf-8') as txt_file:
    for text in text_column:
        txt_file.write(str(text) + '\n')