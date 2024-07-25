from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import csv
import os
import subprocess
import sys
from kivy.properties import StringProperty
from formhandler import FormHandler


# Set the window size
Window.size = (1280, 800)

# Calculate the center position
screen_width, screen_height = Window.system_size
window_width, window_height = Window.size
center_x = (screen_width - window_width) / 2
center_y = (screen_height - window_height) / 2

# Set the window position to center
Window.left = center_x
Window.top = center_y



# ----------------------------------------------------------------------------------------------------------------------

# SCREENS

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Set the background color to white
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

class HomePage(BaseScreen):
    pass

class StartPage_Screen(BaseScreen):
    pass

class NewParticipantRegistratin_Screen(BaseScreen):
    pass

class NewControlForm_Screen(BaseScreen):
    pass

# ----------------------------------------------------------------------------------------------------------------------

# Screens for the New Baseline Recording

class NewBaselineRecording_Screen(BaseScreen):
    pass

class NewBaselineRecording_Description_Screen(BaseScreen):
    pass

class NewBaselineRecording_Record_Screen(BaseScreen):
    pass

class NewBaselineRecording_SelfReportedData_Screen(BaseScreen):
    pass

class NewBaselineRecording_Analyze_Screen(BaseScreen):
    pass

class NewBaselineRecording_Results_Screen(BaseScreen):
    pass

    performance_result_baseline = StringProperty('XX.XX%')

    def update_performance_baseline(self, new_result_baseline):
        self.performance_result_baseline = f'{new_result_baseline}'

# ----------------------------------------------------------------------------------------------------------------------

# Screens for the New Task Recording
class NewTaskRecording_Screen(BaseScreen):
    pass

class NewTaskRecording_Description_Screen(BaseScreen):
    pass

class NewTaskRecording_Record_Screen(BaseScreen):
    pass

class NewTaskRecording_SelfReportedData_Screen(BaseScreen):
    pass

class NewTaskRecording_Analyze_Screen(BaseScreen):
    pass
    pass

class NewTaskRecording_Results_Screen(BaseScreen):
    pass

    performance_result_task = StringProperty('XX.XX%')

    def update_performance_task(self, new_result_task):
        self.performance_result_task = f'{new_result_task}'

# ----------------------------------------------------------------------------------------------------------------------

# Screen for New prediction Screen

class NewPrediction_Screen(BaseScreen):
    pass


# ----------------------------------------------------------------------------------------------------------------------

# Screen for Flow Short Scale (FSS) Form

class NewFlowShortScale_1_Screen(BaseScreen):
    pass

class NewFlowShortScale_2_Screen(BaseScreen):
    pass

# ----------------------------------------------------------------------------------------------------------------------

# Define the app
class BehDrumsApp(App):
    def build(self):
        self.form_handler = FormHandler()  # Instantiate FormHandler
        Builder.load_file('behdrums.kv')  # Load the .kv file
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(HomePage(name='home_page'))
        sm.add_widget(StartPage_Screen(name='start_page'))
        sm.add_widget(NewParticipantRegistratin_Screen(name='new_participant_registration'))
        sm.add_widget(NewControlForm_Screen(name='new_control_form'))
        sm.add_widget(NewBaselineRecording_Screen(name='new_baseline_recording'))
        sm.add_widget(NewBaselineRecording_Description_Screen(name='new_baseline_recording_description'))
        sm.add_widget(NewBaselineRecording_Record_Screen(name='new_baseline_recording_record'))
        sm.add_widget(NewBaselineRecording_SelfReportedData_Screen(name='new_baseline_recording_self_reported_data'))
        sm.add_widget(NewBaselineRecording_Analyze_Screen(name='new_baseline_recording_analyze'))
        sm.add_widget(NewBaselineRecording_Results_Screen(name='new_baseline_recording_results'))
        sm.add_widget(NewTaskRecording_Screen(name='new_task_recording'))
        sm.add_widget(NewTaskRecording_Description_Screen(name='new_task_recording_description'))
        sm.add_widget(NewTaskRecording_Record_Screen(name='new_task_recording_record'))
        sm.add_widget(NewTaskRecording_SelfReportedData_Screen(name='new_task_recording_self_reported_data'))
        sm.add_widget(NewTaskRecording_Analyze_Screen(name='new_task_recording_analyze'))
        sm.add_widget(NewTaskRecording_Results_Screen(name='new_task_recording_results'))
        sm.add_widget(NewPrediction_Screen(name='new_prediction'))
        sm.add_widget(NewFlowShortScale_1_Screen(name='new_flow_short_scale_1'))
        sm.add_widget(NewFlowShortScale_2_Screen(name='new_flow_short_scale_2'))
        return sm

# ----------------------------------------------------------------------------------------------------------------------

# NEW PARTICIPANT REGISTRATION FORM

    # Function to create and submit the registration form

    def submit_new_participant_form(self, participant_id_input, name_input, lastname_input, age_input, genre_input, mainhand_input, years_playing_input, trainning_input, practice_hours_input, rudiments_familiarity_input, rudiments_in_routine_input, rudiments_practice_hours_input):
        # Define the output directory
        output_dir = 'BehDrums/participants_registration'
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Get the number of the participant from the input
        participant_number = participant_id_input
        # Define the CSV file name using the participant number
        filename = f'participant_{participant_number}_registration.csv'
        # Construct the full path
        full_path = os.path.join(output_dir, filename)
        # Open the file in write mode ('w') since each participant gets a new file
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Participant ID', 'Name', 'Last Name', 'Age', 'Genre', 'Main Hand', 'Years Playing', 'Formal Training', 'Practise Hours per Week', 'Familiar with Rudiments', 'Rudiments in Practice Routine', 'Rudiments Practise Hours per Week'])
            # Write the participant's data
            writer.writerow([participant_id_input, name_input, lastname_input, age_input, genre_input, mainhand_input, years_playing_input, trainning_input, practice_hours_input, rudiments_familiarity_input, rudiments_in_routine_input, rudiments_practice_hours_input])

    # Function to clear the form
    def clear_new_participant_form(self, participant_id_input, name_input, lastname_input, age_input, genre_input, mainhand_input, years_playing_input, trainning_input, practice_hours_input, rudiments_familiarity_input, rudiments_in_routine_input, rudiments_practice_hours_input):
        participant_id_input.text = ''
        name_input.text = ''
        lastname_input.text = ''
        age_input.text = ''
        genre_input.text = ''
        mainhand_input.text = ''
        years_playing_input.text = ''
        trainning_input.text = ''
        practice_hours_input.text = ''
        rudiments_familiarity_input.text = ''
        rudiments_in_routine_input.text = ''
        rudiments_practice_hours_input.text = ''

# ----------------------------------------------------------------------------------------------------------------------

# NEW CONTROL FORM

    # Function to create and submit the control form

    def submit_control_form(self, participant_input, session_input, physical_state_input, mental_state_input, sleeping_hours_input, physical_pain_input, stress_input, motivation_input, caffeine_today_input, caffeine_specification_input, practise_today_input, practise_today_specification_input, rudiment_practise_input, rudiment_practise_specification_input):
        # Get the number of the participant from the input
        participant = participant_input
        session = session_input
        # Define the output directory
        output_dir = f'BehDrums/control_data/participant_{participant}'
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Define the CSV file name using the participant number
        filename = f'participant{participant}_session{session}_control_form.csv'
        # Construct the full path
        full_path = os.path.join(output_dir, filename)
        # Open the file in write mode ('w') since each participant gets a new file
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Participant', 'Session', 'Physical State', 'Mental State', 'Sleeping Hours', 'Eating in the last 3 hours', 'Physical Pain or Discomfort', 'Stress Level', 'Motivation Level', 'Caffeine Today', 'Caffeine Amount', 'Drums Practise Today', 'Drums Practise Today Hours', 'Task Rudiment Practised', 'Task Rudiment Practised Hours'])
            # Write the participant's data
            writer.writerow([participant_input, session_input, physical_state_input, mental_state_input, sleeping_hours_input, physical_pain_input, stress_input, motivation_input, caffeine_today_input, caffeine_specification_input, practise_today_input, practise_today_specification_input, rudiment_practise_input, rudiment_practise_specification_input])

    # Function to clear the form
    def clear_control_form(self, participant_input, session_input, physical_state_input, mental_state_input, sleeping_hours_input, physical_pain_input, stress_input, motivation_input, caffeine_today_input, caffeine_specification_input, practise_today_input, practise_today_specification_input, rudiment_practise_input, rudiment_practise_specification_input):
        participant_input.text = ''
        session_input.text = ''
        physical_state_input.text = ''
        mental_state_input.text = ''
        sleeping_hours_input.text = ''
        physical_pain_input.text = ''
        stress_input.text = ''
        motivation_input.text = ''
        caffeine_today_input.text = ''
        caffeine_specification_input.text = ''
        practise_today_input.text = ''
        practise_today_specification_input.text = ''
        rudiment_practise_input.text = ''
        rudiment_practise_specification_input.text = ''
        


# ----------------------------------------------------------------------------------------------------------------------

# NEW BASELINE RECORDING

    # ----- RECORDING SCREEN --------------------------------------------------------------------------------------------

    # Function to run the recording script (baseline)
    def run_recording_script_baseline(file_path):
        file_path = 'BehDrums/recording_script_baseline.py'
        try:
            # Path to the virtual environment's Python interpreter
            venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
            
            # Execute the script using the virtual environment's Python interpreter
            result = subprocess.run([venv_python, file_path], check=True, text=True, capture_output=True)
            
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred while running script:", e.stderr)


    # ----- PERFORMANCE SELF-REPORTED DATA SCREEN -----------------------------------------------------------------------

    # Function to create and submit the performance self-reported data form (baseline)

    def submit_performance_self_reported_data_form_baseline(self, comfort, control, focus, challenge, satisfaction):
        # Define the output directory
        output_dir = 'BehDrums/recording_performance_self_reported_data'
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Get the number of the participant from the form input ("FormHandler"
        form_handler = FormHandler()
        participant = form_handler.get_participant_number()
        tempo = form_handler.get_tempo()
        attempt = form_handler.get_attempt()
        # Define the CSV file name using the participant number
        filename = f'participant_{participant}_sessionbaseline_attempt{attempt}_{tempo}bpm_performance_self_reported_data.csv'
        # Construct the full path
        full_path = os.path.join(output_dir, filename)
        # Open the file in write mode ('w') since each participant gets a new file
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Comfort', 'Control', 'Focus', 'Challenge', 'Satisfaction'])
            writer.writerow([comfort, control, focus, challenge, satisfaction])
        print(f"Self-reported data form submitted for participant {participant}, session baseline, attempt {attempt}, {tempo} bpm.")

    # Function to clear the form (baseline)
    def clear_performance_self_reported_data_form_baseline(self, comfort_input, control_input, focus_input, challenge_input, satisfaction_input):
        comfort_input.text = ''
        control_input.text = ''
        focus_input.text = ''
        challenge_input.text = ''
        satisfaction_input.text = ''


    # ----- PERFORMANCE ANALYSIS SCREEN -------------------------------------------------------------------------------------

    # NewBaselineRecording_Analyze_Screen

    # Function to run the analysis script
    def run_analysis_script_paradiddle(file_path):
        file_path = 'BehDrums/analysis_script_paradiddle.py'
        try:
            # Path to the virtual environment's Python interpreter
            venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
            
            # Execute the script using the virtual environment's Python interpreter
            result = subprocess.run([venv_python, file_path], check=True, text=True, capture_output=True)
            
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred while running script:", e.stderr)


    # ----- PERFORMANCE RESULTS SCREEN -------------------------------------------------------------------------------------

    # Functions to show the overall accuracy result in "Performance results"

    def get_score_percentage_from_csv_baseline(self):
        form_handler = FormHandler()
        participant = form_handler.get_participant_number()
        attempt = form_handler.get_attempt()
        tempo = form_handler.get_tempo()
        results_file_path = f'BehDrums/recording_results/participant{participant}_sessionbaseline_attempt{attempt}_{tempo}bpm_paradiddle_recording_results.csv'
        
        if not os.path.exists(results_file_path):
            print(f"File '{results_file_path}' does not exist yet. It will be created later.")
            return None  # Or return a default value that makes sense in your application
        
        with open(results_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            # Assuming 0-based indexing: row 5 and column 4 is row index 4 and column index 3
            score_result = rows[4][3]
        
        print("Overall Count Percentage:", score_result)
        return score_result

    def show_results_baseline(self):
        overall_count_percentage = self.get_score_percentage_from_csv_baseline()
        if overall_count_percentage is not None:
            self.performance_result_baseline = f'{overall_count_percentage}%'
            results_screen_baseline = self.root.get_screen('new_baseline_recording_results')
            overall_count_percentage = self.get_score_percentage_from_csv_baseline()
            results_screen_baseline.update_performance_baseline(overall_count_percentage)
        else:
            self.performance_result_baseline = 'Data not available yet'


# ----------------------------------------------------------------------------------------------------------------------

# NEW TASK RECORDING

    # ----- RECORDING SCREEN --------------------------------------------------------------------------------------------

    # Function to run the recording script (task)
    def run_recording_script_task(file_path):
        file_path = 'BehDrums/recording_script_task.py'
        try:
            # Path to the virtual environment's Python interpreter
            venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
            
            # Execute the script using the virtual environment's Python interpreter
            result = subprocess.run([venv_python, file_path], check=True, text=True, capture_output=True)
            
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred while running script:", e.stderr)

    # ----- PERFORMANCE SELF-REPORTED DATA SCREEN -----------------------------------------------------------------------

    # Function to create and submit the performance self-reported data form (task)

    def submit_performance_self_reported_data_form_task(self, comfort, control, focus, challenge, satisfaction):
        # Define the output directory
        output_dir = 'BehDrums/recording_performance_self_reported_data'
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Get the number of the participant from the form input ("FormHandler"
        form_handler = FormHandler()
        participant = form_handler.get_participant_number()
        session = form_handler.get_session()
        tempo = form_handler.get_tempo()
        attempt = form_handler.get_attempt()
        # Define the CSV file name using the participant number
        filename = f'participant_{participant}_session{session}_attempt{attempt}_{tempo}bpm_performance_self_reported_data.csv'
        # Construct the full path
        full_path = os.path.join(output_dir, filename)
        # Open the file in write mode ('w') since each participant gets a new file
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Comfort', 'Control', 'Focus', 'Challenge', 'Satisfaction'])
            writer.writerow([comfort, control, focus, challenge, satisfaction])
        print(f"Self-reported data form submitted for participant {participant}, session {session}, attempt {attempt}, {tempo} bpm.")

    # Function to clear the form (baseline)
    def clear_performance_self_reported_data_form_task(self, comfort_input, control_input, focus_input, challenge_input, satisfaction_input):
        comfort_input.text = ''
        control_input.text = ''
        focus_input.text = ''
        challenge_input.text = ''
        satisfaction_input.text = ''


    # ----- PERFORMANCE ANALYSIS SCREEN -------------------------------------------------------------------------------------

    # NewTaskRecording_Analyze_Screen

    # Function to run the analysis script
    def run_analysis_script_flamparadiddle(file_path):
        file_path = 'BehDrums/analysis_script_flamparadiddle.py'
        try:
            # Path to the virtual environment's Python interpreter
            venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
            
            # Execute the script using the virtual environment's Python interpreter
            result = subprocess.run([venv_python, file_path], check=True, text=True, capture_output=True)
            
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred while running script:", e.stderr)


    # ----- PERFORMANCE RESULTS SCREEN -------------------------------------------------------------------------------------

    # TASK RECORDING

    # Functions to show the overall accuracy result in "Performance results"

    def get_score_percentage_from_csv_task(self):
        form_handler = FormHandler()
        participant = form_handler.get_participant_number()
        session = form_handler.get_session()
        attempt = form_handler.get_attempt()
        tempo = form_handler.get_tempo()
        results_file_path = f'BehDrums/recording_results/participant{participant}_session{session}_attempt{attempt}_{tempo}bpm_flamparadiddle_recording_results.csv'
        
        if not os.path.exists(results_file_path):
            print(f"File '{results_file_path}' does not exist yet. It will be created later.")
            return None  # Or return a default value that makes sense in your application
        
        with open(results_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            # Assuming 0-based indexing: row 7 and column 4 is row index 6 and column index 3
            score_result = rows[6][3] #UPDATE FOR FLAM PARADIDDLE OUTPUT .CSV
        
        print("Overall Count Percentage:", score_result)
        return score_result

    def show_results_task(self):
        overall_count_with_flams_percentage = self.get_score_percentage_from_csv_task()
        if overall_count_with_flams_percentage is not None:
            self.performance_result_task = f'{overall_count_with_flams_percentage}%'
            results_screen_task = self.root.get_screen('new_task_recording_results')
            overall_count_with_flams_percentage = self.get_score_percentage_from_csv_task()
            results_screen_task.update_performance_task(overall_count_with_flams_percentage)
        else:
            self.performance_result_task = 'Data not available yet'



    # ----- PREDICTION SCREEN --------------------------------------------------------------------------------------------

    def submit_prediction_form(self, prediction):
        # Define the output directory
        output_dir = 'BehDrums/recording_performance_prediction'
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Get the number of the participant from the input
        form_handler = FormHandler()
        participant = form_handler.get_participant_number()
        session = form_handler.get_session()
        tempo = form_handler.get_tempo()
        attempt = form_handler.get_attempt()
        # Define the CSV file name using the participant number
        filename = f'participant{participant}_session{session}_attempt{attempt}_{tempo}bpm_performance_prediction.csv'
        # Construct the full path
        full_path = os.path.join(output_dir, filename)
        # Open the file in write mode ('w') since each participant gets a new file
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Score Prediction'])
            writer.writerow([prediction])
        print(f"Prediction form submitted for participant {participant}, session {session}, attempt {attempt}, {tempo} bpm. Value entered: {prediction}%")


    # Function to clear the form
    def clear_prediction_form(self, prediction_input):
        prediction_input.text = ''

# ----------------------------------------------------------------------------------------------------------------------

# FLOW SHORT SCALE FORM

    # ----- PERFORMANCE SELF-REPORTED DATA SCREEN -----------------------------------------------------------------------

    # Function to create and submit the performance self-reported data form (baseline)

    def submit_fss_form(self):
        # Define the output directory
        output_dir = 'BehDrums/flow_short_scale_data'
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Get the number of the participant from the form input ("FormHandler")
        form_handler = FormHandler()
        participant = form_handler.get_participant_number()
        session = form_handler.get_session()
        block = form_handler.get_block()
        # Define the CSV file name using the participant number
        filename = f'participant_{participant}_session{session}_block{block}_fss_report.csv'
        # Construct the full path
        full_path = os.path.join(output_dir, filename)

        # Get the root widget
        root = self.root

        # Collect values from the first screen
        screen1 = root.get_screen('new_flow_short_scale_1')
        question_1_input = screen1.ids.question_1_input.text
        question_2_input = screen1.ids.question_2_input.text
        question_3_input = screen1.ids.question_3_input.text
        question_4_input = screen1.ids.question_4_input.text
        question_5_input = screen1.ids.question_5_input.text
        question_6_input = screen1.ids.question_6_input.text
        question_7_input = screen1.ids.question_7_input.text
        question_8_input = screen1.ids.question_8_input.text

        # Collect values from the second screen
        screen2 = root.get_screen('new_flow_short_scale_2')
        question_9_input = screen2.ids.question_9_input.text
        question_10_input = screen2.ids.question_10_input.text
        question_11_input = screen2.ids.question_11_input.text
        question_12_input = screen2.ids.question_12_input.text
        question_13_input = screen2.ids.question_13_input.text
        question_14_input = screen2.ids.question_14_input.text
        question_15_input = screen2.ids.question_15_input.text
        question_16_input = screen2.ids.question_16_input.text

        # Open the file in write mode ('w') since each participant gets a new file
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow([
                'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5',
                'Question 6', 'Question 7', 'Question 8', 'Question 9', 'Question 10',
                'Question 11', 'Question 12', 'Question 13', 'Question 14', 'Question 15', 'Question 16'
            ])
            # Write the answers
            writer.writerow([
                question_1_input, question_2_input, question_3_input, question_4_input,
                question_5_input, question_6_input, question_7_input, question_8_input,
                question_9_input, question_10_input, question_11_input, question_12_input,
                question_13_input, question_14_input, question_15_input, question_16_input
            ])
        
        print(f"Flow Short Scale form submitted for participant {participant}, session {session}, block {block}")

    # Function to clear the form (baseline)
    def clear_fss_form(self):
        # Get the root widget
        root = self.root

        # Clear values from the first screen
        screen1 = root.get_screen('new_flow_short_scale_1')
        screen1.ids.question_1_input.text = ''
        screen1.ids.question_2_input.text = ''
        screen1.ids.question_3_input.text = ''
        screen1.ids.question_4_input.text = ''
        screen1.ids.question_5_input.text = ''
        screen1.ids.question_6_input.text = ''
        screen1.ids.question_7_input.text = ''
        screen1.ids.question_8_input.text = ''

        # Clear values from the second screen
        screen2 = root.get_screen('new_flow_short_scale_2')
        screen2.ids.question_9_input.text = ''
        screen2.ids.question_10_input.text = ''
        screen2.ids.question_11_input.text = ''
        screen2.ids.question_12_input.text = ''
        screen2.ids.question_13_input.text = ''
        screen2.ids.question_14_input.text = ''
        screen2.ids.question_15_input.text = ''
        screen2.ids.question_16_input.text = ''





# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    BehDrumsApp().run()
