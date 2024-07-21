import mido
import keyboard
import time
import simpleaudio as sa
import csv
import wave
import os
from formhandler import FormHandler


# Access the singleton instance
form_handler = FormHandler()
 
# User-defined parameters
participant = form_handler.get_participant_number()
session = "baseline" # Session number (1-10) or "baseline"
attempt = form_handler.get_attempt()
tempo = form_handler.get_tempo()  # Tempo of the metronome track (levels: 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160)

#Type of rudiment recorded
rudiment = "paradiddle" #"paradiddle" for baseline assessment session or "flamparadiddle" for the rest of the sessions

# Generate the filename based on the parameters
csv_filename = f"participant{participant}_session{session}_attempt{attempt}_{tempo}bpm_{rudiment}_recording.csv"

# Output directory
output_directory = "BehDrums/recording_data"

full_csv_path = os.path.join(output_directory, csv_filename)


#RECORDING SCRIPT

# Get the name of the first available input port
input_port_name = mido.get_input_names()[0]

# Load .wav file
wave_obj = sa.WaveObject.from_wave_file(f"BehDrums/Metronome tracks - wav/{tempo}_metronome.wav")
 
# Get the duration of the .wav file
with wave.open(f"BehDrums/Metronome tracks - wav/{tempo}_metronome.wav", "rb") as wave_file:
    duration = wave_file.getnframes() / wave_file.getframerate()

# Prepare a list to store the recorded data
recorded_data = []

# Open the input port
with mido.open_input(input_port_name) as inport:
    print(f"Recording on {input_port_name}. Press space to stop.")

    # Play .wav file
    play_obj = wave_obj.play()

    # Get the current time at the start of the recording
    start_time = time.time()

    # Loop until the space bar is pressed or the duration has passed
    while time.time() - start_time < duration:
        # If space bar is pressed, break the loop
        if keyboard.is_pressed('space'):
            print("Stopping recording.")
            break

        # Poll for a MIDI message
        msg = inport.poll()

        # If a MIDI message was received
        if msg is not None: 
            # Check if the message is a 'note_on' or 'note_off' message
            if msg.type in ['note_on', 'note_off']:
                # If it's a 'note_on' message with velocity 0, create a new 'note_off' message
                if msg.type == 'note_on' and msg.velocity == 0:
                    msg = mido.Message('note_off', note=msg.note, velocity=0, time=msg.time, channel=msg.channel)
                # Calculate the elapsed time since the start of the recording
                elapsed_time = time.time() - start_time

                # Store the MIDI message and the elapsed time
                recorded_data.append([1, elapsed_time, msg.type, msg.channel, msg.note, msg.velocity])

    # Print the message after the loop ends
    print("Recording stopped.")

# Write the recorded data to a .csv file
with open(full_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["track", "time", "type", "channel", "note", "velocity"])
    writer.writerows(recorded_data)

print(f"Data saved to {full_csv_path}")
