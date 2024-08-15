import streamlit as st
import re
import os
import comtypes
comtypes.CoInitialize()
import pyttsx3

from functions.config_page.visual_system_voice import VisualSyntheticVoice


def split_text_and_code(text):
    # Define a regex pattern for code detection
    pattern = r'(```.*?```)'  # This pattern matches text within triple backticks
    
    # Use regex split to separate text and code
    segments = re.split(pattern, text, flags=re.DOTALL)
    
    return segments

class NarratorVoice:
    def __init__(self, lang):
        self.lang = lang
        self.engine = pyttsx3.init()

    def get_voice_list(self):
        voices = self.engine.getProperty('voices')
        voice_dict = {i: voice for i, voice in enumerate(voices)}
        return voice_dict
    
    def select_voice(self, lang):
        voices = self.get_voice_list()
        voice_names = [''] + [voices[i].name for i in voices]  # Add an empty string to the top of the list
        config_txt_file = "save_config_txt/select_voice.txt"

        st.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

        selected_voice_id = None  # Initialize selected_voice_id as None

        if lang == "Fr":
            selected_voice_name = st.selectbox('Sélectionnez la voix synthétique à utiliser', voice_names, index=0)
        else:
            selected_voice_name = st.selectbox('Select the synthetic voice to use', voice_names, index=0)

        # If the user has not selected a voice, do nothing
        if selected_voice_name == '':
            return None

        selected_voice_id = [voice.id for voice in voices.values() if voice.name == selected_voice_name][0] if selected_voice_name else ''

        # Write the name of the selected voice in a text file
        with open(config_txt_file, 'w') as f:
            f.write(selected_voice_id)

        # Read the content of the text file and display it
        with open(config_txt_file, 'r') as f:
            content = f.read()
            st.markdown("<p style='font-weight: bold; color:#c05bb6;'>ID de la Voix du Narrateur selectionné: " + content + "</p>" if lang == 'Fr' else 
                        "<p style='font-weight: bold; color:#c05bb6;'>Selected Narrator Voice ID: " + content + "</p>", unsafe_allow_html=True)

        return selected_voice_id
        
    def speak(self, text):
        # Split the text into text and code segments
        segments = split_text_and_code(text)
        
        # Read Voice on the .txt file
        filename_voice = 'save_config_txt/select_voice.txt'
        if os.path.exists(filename_voice):
            with open(filename_voice, 'r') as file:
                voice = file.read().strip()
        else:
            st.sidebar.error("Veuillez aller à la page configuration pour choisir une voix." if self.lang == 'Fr' else 
                            "Please go to the configuration page to choose a voice.")
            return

        for segment in segments:
            # Check if the segment is code
            if segment.startswith('```') and segment.endswith('```'):
                st.sidebar.warning("Code détecté, pas lu à haute voix." if self.lang == 'Fr' else "Code detected, not reading out loud.")
            else:   
                # Create the directories if they don't exist
                directory = "functions/config_page/temp_output_voice/"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Create the full file path
                full_path = os.path.join(directory, "voice_output.wav")

                # If the file already exists, remove it
                if os.path.exists(full_path):
                    os.remove(full_path)

                # Set narrator voice
                self.engine.setProperty('voice', voice)

                # Convert text to speech and save it to a file
                self.engine.save_to_file(segment, full_path)

                # Wait for any pending speech to complete
                self.engine.runAndWait()

                # Create an instance of the class and call the play_audio method
                visual_voice = VisualSyntheticVoice()
                visual_voice.play_audio(filename=full_path)
                