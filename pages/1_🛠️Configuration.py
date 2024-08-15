import streamlit as st
import platform
import os
import comtypes.client
comtypes.CoInitialize()

from functions._ui_global.page_title import set_page_title
from functions._ui_global.custom_ui import custom_ui
from functions.menu_page.get_language import get_lang
from functions.config_page.selection_microphone import select_microphone
from functions.config_page.narrator_voice import NarratorVoice
from functions.config_page.json.create_trigger_response_json import json_trigger_response
from functions.config_page.json.create_trigger_app_json import json_trigger_app
from functions.config_page.mic_sensitivity import mic_record_threshold
from functions.config_page.cam_index import choose_cam


# Add a language switcher to the sidebar
lang = get_lang()

# Narrator Voice checkbox
select_micro = st.sidebar.checkbox("Configurez Microphone" if lang == 'Fr' else "Configure Microphone")
if select_micro:
    select_microphone(lang)

# Narrator Voice checkbox
narrator_voice = st.sidebar.checkbox("Configurez Voix Narrateur" if lang == 'Fr' else "Configure Narrator Voice")
if narrator_voice:
    voice_index = NarratorVoice(lang)
    voice_index.select_voice(lang)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# JSON trigger text and response
json_trigger_and_response = st.sidebar.checkbox("Texte déclencheur et réponse" if lang == 'Fr' else "Trigger text and response")
if json_trigger_and_response:
    json_trigger_response(lang)
    
# JSON trigger text and start app
json_trigger_start_app = st.sidebar.checkbox("Texte déclencheur d'application" if lang == 'Fr' else "Trigger text application")
if json_trigger_start_app:
    json_trigger_app(lang)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Mic Detection Sensitivity
mic_sensitivity = st.sidebar.checkbox("Sensibilité détection du micro" if lang == 'Fr' else "Mic Detection Sensitivity")
if mic_sensitivity:
    mic_record_threshold(lang)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Cam selection
cam_selection = st.sidebar.checkbox("Caméra" if lang == 'Fr' else "Camera")
if cam_selection:
    choose_cam(lang)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Add a button to the sidebar that redirects to modelfile.py
if st.sidebar.button('Paramètres Modèles' if lang == 'Fr' else 'Models Parameters'):
    if platform.system() == "Windows":
        os.system("start cmd /K python functions/config_page/custom_model/modelfile.py")
    else:
        os.system("gnome-terminal -e 'bash -c \"python functions/config_page/custom_model/modelfile.py; exec bash\"'")

comtypes.CoUninitialize()

# Use the function to set the page title
set_page_title("Configuration · Streamlit", "🛠️ Configuration")
custom_ui()