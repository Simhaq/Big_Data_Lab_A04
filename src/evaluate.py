# Evaluate

import os
import numpy as np
import pandas as pd

import json

from sklearn.metrics import r2_score

month_df = pd.read_csv('data/ground_truth.csv')                # Reading the ground_truth.csv
daily_df = pd.read_csv('data/computed_monthly_averages.csv')   # Reading the computed_monthly_averages.csv

n_fields = len(month_df.axes[1])                               # Getting total no of columns in month_df
total_df = pd.concat([month_df,daily_df.iloc[:,2:]],axis = 1)  # Contatenating monthly and daily data to handle missing values in 
total_df = total_df.dropna()                                   # daily data 


extracted_averages = total_df.iloc[:,2:n_fields].to_numpy()    # Getting the extracted monthly averages in the form of
                                                               # 2D numpy array
extracted_averages = extracted_averages.flatten('F')           # Flattening the array along the column 



computed_averages = total_df.iloc[:,n_fields:].to_numpy()      # Getting the computed monthly averages in the form of
                                                               # 2D numpy array 
computed_averages = computed_averages.flatten('F')             # Flattening the array along the column


R_squared = r2_score(extracted_averages, computed_averages)    # Computing R-squared score using sklearn's r2_score

metrics = {'R_squared': R_squared}                             # Writing the obtained scores in a json file
with open('scores.json','w') as f:
    json.dump(metrics,f)
    
print("The R-squared score is ",R_squared)

if R_squared >= 0.9:
    print("The data is Consistent(C)")
else:
    print("The data is inconsistent")