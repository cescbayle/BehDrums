import pandas as pd
import numpy as np
import os

# Load the csv file
file_path = '160_caltrack.mid_filtered_time&velocity_with start and intervals.csv'
df = pd.read_csv(file_path)

# Calculate the group and interval indices
group_indices = np.ceil((df.index + 1) / 32).astype(int)
interval_indices = ((df.index % 32) + 1).astype(int)

# Create the interval names
interval_names = ['b' + str(group) + 'i' + str(interval) for group, interval in zip(group_indices, interval_indices)]

# Add the interval names to the dataframe
df['interval_name'] = interval_names

# Get the base name and extension of the original file
base_name, extension = os.path.splitext(file_path)

# Create a new file name by appending "_with interval names" to the base name
new_file_name = f"{base_name}_with interval names{extension}"

# Save the dataframe back to the new csv file
df.to_csv(new_file_name, index=False)