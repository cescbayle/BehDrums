import pandas as pd
import os
import glob

# Specify the folder containing the CSV files
folder_path = 'Midi files'

# Specify the output folder
output_folder = 'Calculus tracks - filtered (Paradiddle)'

# Get a list of all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Loop over the list of files
for file_name in csv_files:
    # Load the CSV file
    df = pd.read_csv(file_name)

    # Filter the DataFrame
    filtered_df = df[df['velocity'] >= 100]

    # Extract the base name and extension from the original file name
    base_name, extension = os.path.splitext(os.path.basename(file_name))

    # Create a new file name by appending "_filtered" to the base name
    new_file_name = f"{base_name}_filtered{extension}"

    # Create a new file path in the output folder
    new_file_path = os.path.join(output_folder, new_file_name)

    # Save the filtered DataFrame to a new CSV file in the output folder
    filtered_df.to_csv(new_file_path, index=False)