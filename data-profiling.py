import pandas as pd
from ydata_profiling import ProfileReport

# Import './data/final_data,csv' to pandas dataframe
df = pd.read_csv('./data/final_data.csv')

# Create pandas report
profile = ProfileReport(df)
profile.to_file('./data/profile_report.html')
