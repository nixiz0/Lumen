import streamlit as st
import cv2
import os
import time

from functions.menu_page.commands.cam.cam_index import read_cam_index


def capture_camera(cam_index):
    if not os.path.exists('photos'):
        os.makedirs('photos')
    cap = cv2.VideoCapture(int(cam_index))
    ret, frame = cap.read()
    time.sleep(1)
    cv2.imwrite('photos/camera.png', frame)
    cap.release()

class CamCommand:
    def __init__(self, listen, device, language, talk):
        self.listen = listen
        self.device = device
        self.language = language
        self.talk = talk

    def screen_cam(self):
        screen_keywords = ['lumen screen avec la caméra', 'lumen screen avec la cam', 'lumen screen cam', 'lumen screencam',         
                           'lumen screen with camera', 'lumen cam screen']
        for keyword in screen_keywords:
            if keyword in self.listen:
                if self.language == 'Fr':
                    self.talk("Lancement du screen avec caméra")
                else: 
                    self.talk("Launch of the screen with camera")

                cam_index = read_cam_index()
                if cam_index is not None:
                    capture_camera(cam_index)
                    if self.language == 'Fr':
                        self.talk("Screen de la caméra effectué")
                    else: 
                        self.talk("Camera screen taken")
                    return True
                else:
                    if self.language == 'Fr':
                        st.warning("Veuillez aller dans la page de configuration pour configurer une caméra.")
                    else:
                        st.warning("Please go to the configuration page to set up a camera.")
                    return False
