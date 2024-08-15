import streamlit as st
import os 


def define_lang():
    # Check if the directory save_config_txt exists, if not, create it
    if not os.path.exists('save_config_txt'):
        os.makedirs('save_config_txt')

    # Check if the lang.txt file exists
    lang_file = 'save_config_txt/lang.txt'
    if os.path.exists(lang_file):
        # Read the value from the file
        with open(lang_file, 'r') as file:
            saved_lang = file.read().strip()
    else:
        # If the file doesn't exist, use a default value
        saved_lang = 'Fr'

    # Add a language switcher to the sidebar with the read or default value
    lang = st.sidebar.selectbox('🔤 Language', ['Fr', 'En'], index=['Fr', 'En'].index(saved_lang))

    # Write the selected language to the file
    with open(lang_file, 'w') as file:
        file.write(lang)
    return lang

def get_lang():
    # Check if the file exists
    lang_file = 'save_config_txt/lang.txt'
    if os.path.exists(lang_file):
        # Read the language from the file
        with open(lang_file, 'r') as file:
            lang = file.read().strip()
    else:
        # Display an error message in the sidebar
        st.sidebar.error("The language file doesn't exist. Please go to the menu to set a language.")
    return lang