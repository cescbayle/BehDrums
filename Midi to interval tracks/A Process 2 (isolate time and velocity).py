import pandas as pd
import os

# Original file path
original_file_path = '160_caltrack.mid_filtered_flam.csv'

# Load the csv file into a DataFrame
df = pd.read_csv(original_file_path)

# Select only the 'time' and 'velocity' columns
new_df = df[['time', 'velocity']]

# Extract the original filename without extension
original_filename = os.path.splitext(original_file_path)[0]

# Create new filename by appending "_time&velocity" to the original filename
new_filename = original_filename + "_time&velocity.csv"

# Save the new DataFrame to a new csv file
new_df.to_csv(new_filename, index=False)