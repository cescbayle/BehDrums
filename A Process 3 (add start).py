import pandas as pd
import os

# Load the csv file
file_path = '160_caltrack.mid_filtered_flam_time&velocity.csv'
df = pd.read_csv(file_path)

# Create a new dataframe with the row you want to add
new_row = pd.DataFrame({'time': [0], 'velocity': [127]})

# Concatenate the new row with the original dataframe
df = pd.concat([new_row, df]).reset_index(drop=True)

# Get the base name and extension of the original file
base_name, extension = os.path.splitext(file_path)

# Create a new file name by appending "_with start" to the base name
new_file_name = f"{base_name}_with start{extension}"

# Save the dataframe back to the new csv file
df.to_csv(new_file_name, index=False)