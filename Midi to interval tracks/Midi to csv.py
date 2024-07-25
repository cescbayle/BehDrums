import os
import csv
from mido import MidiFile, MidiTrack, MetaMessage

def ticks_to_seconds(ticks, tempo, ticks_per_beat):
    """Convert ticks to seconds using the given tempo and ticks per beat."""
    # tempo is in microseconds per beat, so 1,000,000 / tempo gives beats per second
    # multiplying by ticks and dividing by ticks_per_beat gives seconds
    return ticks * (tempo / 1_000_000.0) / ticks_per_beat

def midi_to_csv(midi_file_path, csv_file_path):
    """Convert a MIDI file to a CSV file."""
    mid = MidiFile(midi_file_path)

    ticks_per_beat = mid.ticks_per_beat
    current_tempo = 500000  # Default tempo is 500,000 microseconds per beat (120 BPM)

    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['track', 'time', 'type', 'channel', 'note', 'velocity'])  # Header row

        for i, track in enumerate(mid.tracks):
            cumulative_ticks = 0
            cumulative_seconds = 0.0

            for msg in track:
                cumulative_ticks += msg.time
                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo

                if msg.type in ['note_on', 'note_off']:
                    delta_seconds = ticks_to_seconds(msg.time, current_tempo, ticks_per_beat)
                    cumulative_seconds += delta_seconds
                    csvwriter.writerow([
                        i, cumulative_seconds, msg.type, msg.channel, msg.note, msg.velocity
                    ])
                else:
                    delta_seconds = ticks_to_seconds(msg.time, current_tempo, ticks_per_beat)
                    cumulative_seconds += delta_seconds

def convert_folder_to_csv(folder_path):
    """Convert all MIDI files in the specified folder to CSV files."""
    for filename in os.listdir(folder_path):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            midi_file_path = os.path.join(folder_path, filename)
            csv_file_path = os.path.join(folder_path, filename + '.csv')
            midi_to_csv(midi_file_path, csv_file_path)
            print(f'Converted {midi_file_path} to {csv_file_path}')

# Replace 'your_folder_path' with the path to your folder containing MIDI files
folder_path = 'Midi files'
convert_folder_to_csv(folder_path)
