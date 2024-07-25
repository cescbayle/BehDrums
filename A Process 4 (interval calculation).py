import pandas as pd
import os

# Original file path
original_file_path = '160_caltrack.mid_filtered_flam_time&velocity_with start.csv'

# Load the csv file into a DataFrame
df = pd.read_csv(original_file_path)

# Calculate the intervals between 'time' values
df['time_interval'] = df['time'].diff()

# Fill the NaN value in the 'time_interval' column with the first 'time' value
df['time_interval'].fillna(df['time'].iloc[0], inplace=True)

# Save the DataFrame with the new 'time_interval' column to a new csv file
new_filename = os.path.splitext(original_file_path)[0] + " and intervals.csv"
df.to_csv(new_filename, index=False)