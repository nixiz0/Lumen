import streamlit as st
import pyaudio
import os


def get_microphone_list():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    devices = {}
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            devices[i] = p.get_device_info_by_host_api_device_index(0, i).get('name')
    return devices

def select_microphone(lang):
    devices = get_microphone_list()
    device_names = [''] + [devices[i] for i in devices]  # Add an empty string to the top of the list
    config_txt_file = "save_config_txt/select_microphone.txt"

    selected_device_index = 0
    if lang == "Fr":
        selected_device_name = st.selectbox('Sélectionnez le microphone à utiliser', device_names, index=selected_device_index)
    else:
        selected_device_name = st.selectbox('Select the microphone to use', device_names, index=selected_device_index)
    
    # If the user has not selected a microphone, do nothing
    if selected_device_name == '':
        return None

    selected_device_index = list(devices.values()).index(selected_device_name)

    # Write the name of the selected microphone in a text file
    with open(config_txt_file, 'w') as f:
        f.write(str(selected_device_index))

    # Read the content of the text file and display it
    with open(config_txt_file, 'r') as f:
        content = f.read()
        st.markdown("<p style='font-weight: bold; color:#c05bb6;'>Index du Microphone selectionné: " + content + "</p>" if lang == 'Fr' else 
                    "<p style='font-weight: bold; color:#c05bb6;'>Selected Microphone Index: " + content + "</p>", unsafe_allow_html=True)

    return selected_device_index

def get_microphone(lang):
    # Read the microphone frome the .txt file
    filename_microphone = 'save_config_txt/select_microphone.txt'
    if os.path.exists(filename_microphone):
        with open(filename_microphone, 'r') as file:
            device = int(file.read().strip())
    else:
        st.sidebar.error("Veuillez aller à la page configuration pour définir le microphone." if lang == 'Fr' else 
                         "Please go to the configuration page to set the microphone.")
    
    return device