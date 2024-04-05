# Process

import os
import numpy as np
import pandas as pd

cwd = os.getcwd()
data_dir = os.path.join(cwd,'data','climate_data')

with open('data/List_of_Fields.npy','rb') as f:
    daily_fields = np.load(f).tolist()                              # Getting the Daily fields from List_of_Fields.npy

files = os.listdir(data_dir)

final_df = pd.DataFrame(columns = ['STATION','Month']+daily_fields) # DataFrame to concatinate data from all the csv files

for f in files:
    if f.endswith('.csv'):
        df = pd.read_csv(os.path.join('data','climate_data',f))     # Reading the csv 
        for field in daily_fields:
            df[field] = pd.to_numeric(df[field],errors= 'coerce')   # Converting the dtype to float (strings to nan)
        df['DATE'] = pd.to_datetime(df['DATE'])                     # Converting the dtype to datetime to extract month
        df['Month'] = df['DATE'].dt.month                           # Adding month from DATE
        df = df.groupby(['Month'])[['STATION','Month']+daily_fields].mean()  # Calculating monthly averages from daily values
        df['STATION'] = df['STATION'].astype(int)
        df['Month'] = df['Month'].astype(int)
    
        final_df = pd.concat([final_df,df])                         # Concatinating the dataframes

final_df.to_csv('data/computed_monthly_averages.csv',index=False)   # Saving the csv
