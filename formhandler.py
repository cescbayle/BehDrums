import json
import os
from threading import Lock

class FormHandler:
    _instance = None
    _lock = Lock()
    _data_file = 'form_data.json'

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(FormHandler, cls).__new__(cls)
                cls._instance.participant_number = None
                cls._instance.session = None
                cls._instance.attempt = None
                cls._instance.tempo = None
                cls._instance.load_data()
        return cls._instance

    def load_data(self):
        try:
            if os.path.exists(self._data_file):
                with open(self._data_file, 'r') as file:
                    data = json.load(file)
                    self.participant_number = data.get('participant_number')
                    self.session = data.get('session')
                    self.attempt = data.get('attempt')
                    self.tempo = data.get('tempo')
            else:
                self.participant_number = None
                self.session = None
                self.tempo = None
                self.attempt = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.participant_number = None
            self.session = None
            self.attempt = None
            self.tempo = None


    def save_data(self):
        data = {
            'participant_number': self.participant_number,
            'session': self.session,
            'attempt': self.attempt,
            'tempo': self.tempo
        }
        try:
            with open(self._data_file, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error saving data: {e}")

    def submit_data_entry_form(self, participant_number, session, tempo, attempt):
        self.participant_number = participant_number
        self.session = session
        self.attempt = attempt
        self.tempo = tempo
        self.save_data()
        print(f"Participant number {participant_number}, session {session}, attempt {attempt}, tempo {tempo}, submitted.")

    def get_participant_number(self):
        return self.participant_number
    
    def get_session(self):
        return self.session
    
    def get_attempt(self):
        return self.attempt

    def get_tempo(self):
        return self.tempo

    def clear_data_entry_form(self, participant_number_input, session_input, tempo_input, attempt_input):
        participant_number_input.text = ''
        session_input.text = ''
        tempo_input.text = ''
        attempt_input.text = ''
