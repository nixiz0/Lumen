import streamlit as st 
import os


def mic_record_threshold(lang):
    file_path = 'save_config_txt/mic_record_thresholds.txt'
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            threshold = int(file.read().strip())
    else:
        threshold = 500  # Default value
        # Create the file and write the default
        with open(file_path, 'w') as file:
            file.write(str(threshold))

    st.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    # Create an input field for mic sensitivity
    new_threshold = st.number_input("Sensibilité" if lang == 'Fr' else "Sensitivity", value=threshold)

    # If the user changes the value, update the
    if new_threshold != threshold:
        with open(file_path, 'w') as file:
            file.write(str(new_threshold))