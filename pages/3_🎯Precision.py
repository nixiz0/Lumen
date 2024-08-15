import streamlit as st
import os

from functions._ui_global.page_title import set_page_title
from functions._ui_global.custom_ui import custom_ui
from functions.menu_page.get_language import get_lang
from functions._functions_global_.config_model import configuration_model
from functions._functions_global_.app_button import AppButton
from functions._functions_global_.llm_model_functions.llm_load_hist import load_and_display_chat


# Add a language switcher to the sidebar
lang = get_lang()
configuration_model(lang=lang, filename_model='save_config_txt/precision_model.txt')

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Get a list of all json files in the directory
history_dir = 'functions/precision_page/precision_history'

# Create the directory if it doesn't exist
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

json_files = [f for f in os.listdir(history_dir) if f.endswith('.json')]

if json_files:  # Check if the list is not empty
    # Add a selectbox to the sidebar for file selection
    selected_file = st.sidebar.selectbox('Select a file', json_files)

    # Load and display the selected chat history
    load_and_display_chat(os.path.join(history_dir, selected_file))

    app_btn = AppButton(lang, history_dir, selected_file)
    if selected_file:
        app_btn.rename_file()
        app_btn.download_as_csv()
        app_btn.delete_file()
else:
    st.sidebar.write("Aucun fichier d'historique de chat n'a été trouvé." if lang == 'Fr' else "No chat history files found.")

# Use the function to set the page title
set_page_title("Precision · Streamlit", "🎯 Precision")
custom_ui()