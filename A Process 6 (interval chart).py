import pandas as pd

# Read the original CSV file into a DataFrame
df = pd.read_csv('160_caltrack.mid_filtered_flam_time&velocity_with start and intervals_with interval names.csv')

# Create a new DataFrame with the 'interval_name' and 'time' columns
new_df = df[['interval_name', 'time']].copy()

# Rename the columns to 'interval' and 'start'
new_df.columns = ['interval', 'start']

# Add a new 'end' column, which is the 'start' column shifted up by one
new_df['end'] = new_df['start'].shift(-1)

# Write the new DataFrame to a new CSV file
new_df.to_csv('160_intervals_flam.csv', index=False)