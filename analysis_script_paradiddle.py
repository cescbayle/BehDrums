import pandas as pd
import os
from formhandler import FormHandler

#--------------------------------------------

# FILE PATHS

# Access the singleton instance
form_handler = FormHandler()

# Define recording file information
participant = form_handler.get_participant_number()
session = 'baseline'
attempt = form_handler.get_attempt()
tempo = form_handler.get_tempo()
rudiment = 'paradiddle' # "paradiddle" or "flamparadiddle"

# Specify the CSV file of the recording.
csv_file_path = f'BehDrums/recording_data/participant{participant}_session{session}_attempt{attempt}_{tempo}bpm_{rudiment}_recording.csv'

# Load the CSV file
df_raw = pd.read_csv(csv_file_path)

#--------------------------------------------

# 1 FILTERING

# Filter out 'note_off' rows
filtering = df_raw[df_raw['type'] != 'note_off']

# Convert the results to a DataFrame
df_filtered = pd.DataFrame(filtering)

#--------------------------------------------

# 2 ISOLATION

# Isolate "time" values
isolation = df_filtered['time']

# Convert the results to a DataFrame
df_isolated = pd.DataFrame(isolation)

#--------------------------------------------

#3 ALIGNMENT

# Path for the intervals' file
intervals_path = f'BehDrums/Interval tracks/{rudiment}/{tempo}_{rudiment}_intervals.csv'

df_intervals = pd.read_csv(intervals_path)

# Sort the intervals
df_intervals = df_intervals.sort_values('start')

alignement = []

times_set = set(df_isolated['time'])

# For each interval, find the time that falls into it
for _, interval in df_intervals.iterrows():
    interval_dict = interval.to_dict()
    performance_times = [time for time in times_set if interval['start'] <= time <= interval['end']]
    if performance_times:
        for time in performance_times:
            interval_dict['performance'] = time
            alignement.append(interval_dict.copy())
    else:
        interval_dict['performance'] = 'N/A'
        alignement.append(interval_dict.copy())

# Convert the results to a DataFrame
df_aligned = pd.DataFrame(alignement)

#--------------------------------------------

# 4 GROUPING

# Function to determine interval group with continuous naming across "b" values
def determine_continuous_interval_group(interval):
    # Extract "b" value and "i" value
    b_value, i_value = map(int, interval[1:].split('i'))
    # Calculate the overall sequence number (assuming 32 intervals per "b" value, adjust as needed)
    overall_sequence_num = (b_value - 1) * 32 + i_value
    # Determine the note number based on the overall sequence
    note_num = (overall_sequence_num + 1) // 2
    return f"group {note_num}"

# Define the list of accurate intervals
accurate_intervals = ['i1', 'i3', 'i5', 'i7', 'i9', 'i11', 'i13', 'i15', 'i17', 'i19', 'i21', 'i23', 'i25', 'i27', 'i29', 'i31']

# Function to determine interval type
def determine_interval_type(interval):
    # Extract the numeric part after "i" from the interval identifier
    interval_num = int(interval.split('i')[-1])
    # Determine if the interval is accurate or non-accurate based on whether the number is odd (accurate) or even (non-accurate)
    return "accurate" if interval_num % 2 != 0 else "non-accurate"

# Apply the functions to create the new columns

df_aligned['interval type'] = df_aligned['interval'].apply(determine_interval_type)
df_aligned['interval group'] = df_aligned['interval'].apply(determine_continuous_interval_group)

grouping = df_aligned

# Convert the results to a DataFrame
df_grouped = pd.DataFrame(grouping)

#--------------------------------------------

# 5 COUNTING

#OVERALL SEQUENCE PERFORMANCE

# Initialize counters
accurate_count = 0
non_accurate_count = 0

accurate_groups = {}  # Track groups with accurate performance

# Initialize sets to track counted interval names
counted_accurate_intervals = set()
counted_non_accurate_intervals = set()

# Iterate through each row
for index, row in df_grouped.iterrows():
    group = row['interval group']  # Extract the interval group
    # Check if group is in the format "group X" where X is 1 to 32 or equals "group 417"
    if group in [f"group {i}" for i in range(1, 33)] or group == "group 417":
        continue  # Skip this row and continue with the next iteration

    if pd.notnull(row['performance']) and row['performance'] != "N/A": # Check if 'performance' is not "N/A" and not null
        interval_name = row['interval']  # Assuming there's an 'interval' column

        if row['interval type'] == 'accurate':
            if interval_name not in counted_accurate_intervals:
                counted_accurate_intervals.add(interval_name)
                accurate_count += 1
                accurate_groups[group] = True  # Mark this group as having an accurate performance
        elif row['interval type'] == 'non-accurate':
            if interval_name not in counted_non_accurate_intervals and group not in accurate_groups:
                counted_non_accurate_intervals.add(interval_name)
                non_accurate_count += 1


# PEAK TEMPO PERFORMANCE ("CLOSE" SECTION)

# Initialize counters
accurate_count_peaktempo = 0
non_accurate_count_peaktempo = 0
accurate_groups_peaktempo = {}  # Track groups with accurate performance

# Initialize sets to track counted interval names
counted_accurate_intervals_peaktempo = set()
counted_non_accurate_intervals_peaktempo = set()

# Iterate through each row
for index, row in df_grouped.iterrows():
    group = row['interval group']  # Extract the interval group
    # Check if group is in the format "group X" where X is 1 to 32 or equals "group 417"
    if group in [f"group {i}" for i in range(1, 161)] or group in [f"group {i}" for i in range(289, 417)] or group == "group 417":
        continue  # Skip this row and continue with the next iteration

    if pd.notnull(row['performance']) and row['performance'] != "N/A": # Check if 'performance' is not "N/A" and not null
        interval_name = row['interval']  # Assuming there's an 'interval' column

        if row['interval type'] == 'accurate':
            if interval_name not in counted_accurate_intervals_peaktempo:
                counted_accurate_intervals_peaktempo.add(interval_name)
                accurate_count_peaktempo += 1
                accurate_groups_peaktempo[group] = True  # Mark this group as having an accurate performance
        elif row['interval type'] == 'non-accurate':
            if interval_name not in counted_non_accurate_intervals_peaktempo and group not in accurate_groups_peaktempo:
                counted_non_accurate_intervals_peaktempo.add(interval_name)
                non_accurate_count_peaktempo += 1



#Set the score for non-accurate intervals
non_accurate_score = 0.2 # Non-accurate intervals are counted as 0.2

#Set total amount of intervals
total_intervals = 384
total_intervals_peaktempo = total_intervals // 3
total_non_accurate_intervals_weighted = total_intervals * non_accurate_score
total_non_accurate_intervals_peaktempo_weighted = total_intervals_peaktempo * non_accurate_score

# Calculate overall count
non_accurate_count_weighted = non_accurate_count * non_accurate_score
overall_count = accurate_count + non_accurate_count_weighted

# Percentages
accurate_count_percentage = (accurate_count / total_intervals) * 100
non_accurate_count_percentage = (non_accurate_count / total_intervals) * 100
non_accurate_count_weighted_percentage = (non_accurate_count_weighted / total_non_accurate_intervals_weighted) * 100
overall_count_percentage = ((overall_count)/ total_intervals) * 100


# Calculate overall count for peak tempo
non_accurate_count_peaktempo_weighted = non_accurate_count_peaktempo * non_accurate_score
overall_count_peaktempo = accurate_count_peaktempo + non_accurate_count_peaktempo_weighted

# Percentages
accurate_count_peaktempo_percentage = (accurate_count_peaktempo / total_intervals_peaktempo) * 100
non_accurate_count_peaktempo_percentage = (non_accurate_count_peaktempo / total_intervals_peaktempo) * 100
non_accurate_count_peaktempo_weighted_percentage = (non_accurate_count_peaktempo_weighted / total_non_accurate_intervals_weighted) * 100
overall_count_peaktempo_percentage = ((overall_count_peaktempo)/ total_intervals_peaktempo) * 100
overall_percentage_peaktempo_global = ((overall_count_peaktempo)/ total_intervals) * 100


# Print the results
print(f"---------------------------------")
print(f"PERFORMANCE: participant {participant}, session {session}, attempt {attempt} - {tempo} bpm, {rudiment}")
print(f"---------------------------------")
print(f"OVERALL PERFORMANCE")
print(f"Accurate intervals hit: {accurate_count} (out of {total_intervals})")
print(f"Non-Accurate intervals hit (missing accurate): {non_accurate_count} (out of {total_intervals})")
print(f"Non-Accurate count weighted ({non_accurate_score}): {non_accurate_count_weighted:.2f} (out of {total_non_accurate_intervals_weighted:.2f})")
print(f"Overall count: {overall_count} (out of {total_intervals})")
print(f"Overall percentage: {overall_count_percentage:.2f}%")
print(f"---------------------------------")
print(f"PEAK TEMPO PERFORMANCE")
print(f"Peak-tempo Accurate intervals hit: {accurate_count_peaktempo} (out of {total_intervals_peaktempo})")
print(f"Peak-tempo Non-Accurate intervals hit (missing accurate): {non_accurate_count_peaktempo} (out of {total_intervals_peaktempo})")
print(f"Non-Accurate count weighted ({non_accurate_score}): {non_accurate_count_peaktempo_weighted:.2f} (out of {total_non_accurate_intervals_weighted:.2f})")
print(f"Peak-tempo count: {overall_count_peaktempo} (out of {total_intervals_peaktempo})")
print(f"Peak-tempo percentage: {overall_count_peaktempo_percentage:.2f}% ({overall_percentage_peaktempo_global:.2f}% of the total)")
print(f"---------------------------------")


#--------------------------------------------

# Save the results to a CSV file

import csv

# Data to be written to the CSV file
data = [
    ["result", "value", "out_of", "percentage"],
    ["overall_accurate_intervals", accurate_count, total_intervals, f"{accurate_count_percentage:.2f}%"],
    ["overall_non_accurate_intervals_missing_accurate", non_accurate_count, total_intervals, f"{non_accurate_count_percentage:.2f}%"],
    ["overall_non_accurate_intervals_missing_accurate_weighted", f"{non_accurate_count_weighted:.2f}", f"{total_non_accurate_intervals_weighted:.2f}", f"{non_accurate_count_weighted_percentage:.2f}%"],
    ["overall count", overall_count, total_intervals, f"{overall_count_percentage:.2f}%"],
    ["peaktempo_accurate_intervals", accurate_count_peaktempo, total_intervals_peaktempo, f"{accurate_count_peaktempo_percentage:.2f}%"],
    ["peaktempo_non_accurate_intervals_missing_accurate", non_accurate_count_peaktempo, total_intervals_peaktempo, f"{non_accurate_count_peaktempo_percentage:.2f}%"],
    ["peaktempo_non_accurate_intervals_missing_accurate_weighted", f"{non_accurate_count_peaktempo_weighted:.2f}", f"{total_non_accurate_intervals_peaktempo_weighted:.2f}", f"{non_accurate_count_peaktempo_weighted_percentage:.2f}%"],
    ["peaktempo_count", overall_count_peaktempo, total_intervals_peaktempo, f"{overall_count_peaktempo_percentage:.2f}%"],
]

# Extract just the file name without the .csv extension
base_name = os.path.basename(csv_file_path).rsplit('.', 1)[0]

# Specify the output folder path
output_folder_path = "BehDrums/recording_results"

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Append "_results.csv" to create the new file name in the specified output folder
new_filename = os.path.join(output_folder_path, f"{base_name}_results.csv")

# Writing to the CSV file in the specified output folder
with open(new_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Writing the fields
    csvwriter.writerow(data[0])
    # Writing the data rows
    csvwriter.writerows(data[1:])


