# Evaluate

import os
import numpy as np
import pandas as pd

from sklearn.metrics import r2_score

month_df = pd.read_csv('data/ground_truth.csv')                # Reading the ground_truth.csv
extracted_averages = month_df.iloc[:,2:].to_numpy()            # Getting the extracted monthly averages in the form of                                                                        2D numpy array
extracted_averages = extracted_averages.flatten('F')           # Flattening the array along the column 


daily_df = pd.read_csv('data/computed_monthly_averages.csv')   # Reading the computed_monthly_averages.csv
computed_averages = daily_df.iloc[:,2:].to_numpy()             # Getting the computed monthly averages in the form of                                                                         2D numpy array 
computed_averages = computed_averages.flatten('F')             # Flattening the array along the column


R_squared = r2_score(extracted_averages, computed_averages)    # Computing R-squared score using sklearn's r2_score


print("The R-squared score is ",R_squared)

if R_squared >= 0.9:
    print("The data is Consistent(C)")
else:
    print("The data is inconsistent")