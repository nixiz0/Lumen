import streamlit as st
import os
import cv2    
from pathlib import Path

from functions.config_page.speech_to_text.record import record_audio
from functions.config_page.speech_to_text.speech import SpeechToText
from functions.menu_page.commands.cam.cam_index import read_cam_index


def video_capture(listen, device, lang, talk):
    speech_to_text = SpeechToText()
    filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'

    if lang == 'Fr':
        talk("Voulez-vous définir un titre pour votre vidéo ?")
    else:
        talk("Do you want to set a title for your video ?")
    while True:
        record_audio(language=lang, device_index=device)
        listen = speech_to_text.transcribe(filename_temp_audio)
        user_response = listen
        st.write(user_response)

        if 'oui' in user_response or 'yes' in user_response:
            user_response = 'yes'
            break
        elif 'non' in user_response or 'no' in user_response:
            user_response = 'no'
            break
        else:
            if lang == 'Fr':
                talk("Veuillez répondre Oui ou Non.")
            else:
                talk("Please answer yes or no.")

    if user_response == 'yes':
        if lang == 'Fr':
            talk("Veuillez indiquer le titre de la vidéo.")
        else:
            talk("Please indicate the title of the video.")
        record_audio(language=lang, device_index=device)
        listen = speech_to_text.transcribe(filename_temp_audio)
        title_video_input = listen
        st.write(title_video_input)

        title_video_command = title_video_input.strip() or "video_save.mp4"
        title_video = title_video_command if title_video_command.endswith(".mp4") else title_video_command + ".mp4"
    else:
        title_video = "video_save.mp4"
        
    num_cam = read_cam_index()
    fps = 60
    desktop_path = str(Path.home() / "Downloads")
    video_path = os.path.join(desktop_path, title_video)
    cap = cv2.VideoCapture(num_cam)
    if not cap.isOpened():
        if lang == 'Fr':
            talk("Erreur : Impossible d'ouvrir la caméra.")
        else:
            talk("Error: Unable to open the camera.")
        return

    width = int(cap.get(3))
    height = int(cap.get(4))

    # Set video codec and creator
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    if lang == 'Fr':
        talk("Lancement de la vidéo")
    else:
        talk("Video launch")
    while True:
        ret, frame = cap.read()
        if not ret:
            if lang == 'Fr':
                st.error("Erreur lecture de la caméra.")
            else:
                st.error("Error reading camera.")
            break

        cv2.imshow("Live video (press 'space' to exit)", frame)
        video_writer.write(frame)
        # Stop video capture when 'space' key is pressed
        if cv2.waitKey(1) == 32:
            break
    listen = ""
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()