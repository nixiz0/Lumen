import cv2
import streamlit as st
import os


def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(f"Caméra {index}")
        cap.release()
        index += 1
    return arr

def choose_cam(lang):
    file_path = 'save_config_txt/chosen_cam.txt'
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            default_index = int(file.read().strip())
    else:
        default_index = 0  # Default value
        # Create the file and write the default
        with open(file_path, 'w') as file:
            file.write(str(default_index))

    st.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    cameras = list_cameras()
    cam_name = st.selectbox("Sélectionnez la caméra" if lang == 'Fr' else "Select Camera", cameras, index=default_index)
    new_cam_index = cameras.index(cam_name)

    # If the user changes the value, update the file
    if new_cam_index != default_index:
        with open(file_path, 'w') as file:
            file.write(str(new_cam_index))

    return new_cam_index