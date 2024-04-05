# Prepare
import os
import numpy as np
import pandas as pd

cwd = os.getcwd()
data_dir = os.path.join(cwd,'data','climate_data')

# Dictionary containing the mapping between monthly average fields and their correspoinding daily measurement fields and only these fields are considered
mapping = {'MonthlyMeanTemperature':'DailyAverageDryBulbTemperature',
           'MonthlySeaLevelPressure':'DailyAverageSeaLevelPressure',
           'MonthlyStationPressure':'DailyAverageStationPressure',
           'MonthlyDewpointTemperature':'DailyAverageDewPointTemperature',
           'MonthlyAverageRH':'DailyAverageRelativeHumidity',
           'AWND':'DailyAverageWindSpeed'}

monthly_fields = set(mapping.keys())

files = os.listdir(data_dir)
for f in files:
    if f.endswith('.csv'):
        df = pd.read_csv(os.path.join('data','climate_data',f))          # Reading the csv
        
        for key in mapping.keys():
            if df[key].count() < 12 or df[mapping[key]].count() == 0:    # Discarding the Field if monthly averages not 
                monthly_fields.discard(key)                              # present for 12 months or daily data not present  
            
monthly_fields = list(monthly_fields)
daily_fields = []
for x in monthly_fields:
    daily_fields.append(mapping[x])

final_df = pd.DataFrame(columns = ['STATION','Month']+monthly_fields) # DataFrame to concatinate data from all the csv files

for f in files:
    if f.endswith('.csv'):
        df = pd.read_csv(os.path.join('data','climate_data',f))         # Reading the csv      
        df['DATE'] = pd.to_datetime(df['DATE'])                         # Converting the dtype to datetime to extract month 
        df['Month'] = df['DATE'].dt.month                               # Adding month from DATE
        df = df[['STATION','Month']+monthly_fields].dropna()            # Extracting the monthly averages
        final_df = pd.concat([final_df,df])                             # Concatinating the dataframes
    
final_df.to_csv('data/ground_truth.csv',index=False)                    # Saving the csv

with open('data/List_of_Fields.npy','wb') as outfile:
    np.save(outfile,np.array(daily_fields))                             # Saving the List of Fields as .npy file
