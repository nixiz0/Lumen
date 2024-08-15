import streamlit as st
import os
import json
from functions.config_page.speech_to_text.record import record_audio
from functions.config_page.speech_to_text.speech import SpeechToText


class TextAddCommands:
    def __init__(self, listen, device, language, talk):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk

    def add_text(self):
        filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'
        add_text_keywords = ['lumen ajout de texte', 'lumen ajout de text', 'lumen ajoute texte', 'lumen ajoute texte', 
                             'lumen ajoute du texte', 'lumen text add', 'lumen add text', 'lumen add of text', 'lumen add some text']
        if any(keyword in self.listen for keyword in add_text_keywords):
            dir_path = 'config_json'
            json_app = 'text.json'
            app_path = os.path.join(dir_path, json_app)
            speech_to_text = SpeechToText()
            if not os.path.exists(app_path):
                with open(app_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f) 
            if self.language == 'Fr':
                st.sidebar.warning("Veuillez indiquer le texte déclencheur souhaité")
                self.talk("Veuillez indiquer le texte déclencheur souhaité")
            else: 
                st.sidebar.warning("Please indicate the trigger text you want")
                self.talk("Please indicate the trigger text you want")
                
            # Record the trigger phrase
            record_audio(language=self.language, device_index=self.device)
            listen = speech_to_text.transcribe(filename_temp_audio).strip()
            st.write(listen)
            trigger_phrase = listen

            # Save the trigger phrase to the JSON file
            with open(app_path, 'r+', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:  # If the file is empty
                    data = {}
                data[trigger_phrase] = None  # Use the trigger phrase as the key
                f.seek(0)  # Move the cursor to the beginning of the file
                f.truncate()  # Remove the rest of the file's content
                json.dump(data, f, ensure_ascii=False)

            # Ask the user for the response phrase
            if self.language == 'Fr':
                st.sidebar.warning("Quelle phrase de réponse voulez-vous avoir ?")
                self.talk("Quelle phrase de réponse voulez-vous avoir ?")
            else: 
                st.sidebar.warning("What response sentence do you want to have ?")
                self.talk("What response sentence do you want to have ?")
            
            # Record the response phrase
            record_audio(device_index=self.device)
            listen = speech_to_text.transcribe(filename_temp_audio).strip()
            st.write(listen)
            response_phrase = listen

            # Save the response phrase to the JSON file
            with open(app_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data[trigger_phrase] = response_phrase
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4, ensure_ascii=False)
                if self.language == 'Fr':
                    st.sidebar.success("Texte ajouté")
                    self.talk("Texte ajouté")
                else: 
                    st.sidebar.success("Text added")
                    self.talk("Text added")