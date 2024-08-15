import streamlit as st
from functions.config_page.speech_to_text.record import record_audio
from functions.config_page.speech_to_text.speech import SpeechToText


class SpeechToEnCommand:
    def __init__(self, listen, device, language, talk):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk

    def translate(self):
        filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'
        translate_keywords = ['lumen mode traduction', 'lumen passe en mode traduction', 
                              'lumen translation mode', 'lumen switch to translation mode']
        for keyword in translate_keywords:
            if keyword in self.listen:
                if self.language == 'Fr':
                    st.sidebar.success("Mode Traduction (Langue détecté vers l'Anglais) [dire 'stop' pour arrêter de traduire]")
                    self.talk("Mode Traduction Activé")
                else: 
                    st.sidebar.success("Translation Mode (Language detected to English) [Say 'stop' to stop the translation")
                    self.talk("Traduction Mode Activated")

                speech_to_text = SpeechToText()
                talking = False
                while True:
                    record_audio(language=self.language, device_index=self.device)
                    listen = speech_to_text.translate_to_en(filename_temp_audio)
                    st.write(listen)

                    if talking:
                        self.talk(listen)

                    talking_on_keywords = ['activate the voice', 'activate voice', 'voice activate']
                    if any(keyword in listen for keyword in talking_on_keywords):
                        if self.language == 'Fr': 
                            self.talk("Voix activée")
                        else: 
                            self.talk("Voice activated")
                        talking = True

                    talking_off_keywords = ['desactivate the voice', 'desactivate voice', 'voice desactivate']
                    if any(keyword in listen for keyword in talking_off_keywords):
                        if self.language == 'Fr': 
                            self.talk("Voix activée")
                        else: 
                            self.talk("Voice activated")
                        talking = True

                    translate_keywords = ['stop', 'stopp']
                    if any(keyword in listen for keyword in translate_keywords):
                        if self.language == 'Fr': 
                            st.sidebar.success("Mode Traduction Désactivé")
                            self.talk("Mode Traduction Désactivé")
                        else: 
                            st.sidebar.success("Traduction Mode Desactivated")
                            self.talk("Traduction Mode Desactivated")
                        break