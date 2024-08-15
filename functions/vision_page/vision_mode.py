import streamlit as st
import os
import requests 
import json 

from functions.config_page.speech_to_text.speech import SpeechToText
from functions.config_page.speech_to_text.record import record_audio
from functions.menu_page.commands.screenshot import ScreenCommand
from functions.menu_page.commands.cam.screen_cam import CamCommand
from functions.vision_page.encode_img import encode_image_to_base64
from functions._functions_global_.llm_model_functions.llm_save_hist import save_conversation


def start_vision(device, lang, talk, model_path, hist_dir):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': "application/json",}
    vision_history = []
    speech_to_text = SpeechToText()
    working = True
    filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'

    if os.path.isfile(model_path):
        with open(model_path, 'r') as file:
            vision_model = file.read().strip()
    else:
        st.sidebar.error("Veuillez configurer le modèle à utiliser dans la page vision." if lang == 'Fr' else 
                         "Please configure the template to be used in the vision page.")

    def analyze_image(image_path, custom_prompt):
        vision_history.append(custom_prompt)
        image_base64 = encode_image_to_base64(image_path)
        
        payload = {
            "model": vision_model,
            "prompt": custom_prompt,
            "images": [image_base64]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        try: 
            response_lines = response.text.strip().split('\n')
            full_response = ''.join(json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))

            st.write(custom_prompt)
            st.write(full_response)
            chat_history = [
                [custom_prompt, full_response]
            ]
            
            # Read response to user
            talk(full_response)
            
            return full_response, chat_history
        except Exception as e: 
            return f"Error: {e}"

    while True:
        if working:
            st.markdown("<p style='font-weight: bold; color:#c05bb6;'>Mode Vision LLM..</p>" if lang == 'Fr' else 
                        "<p style='font-weight: bold; color:#c05bb6;'>Vision LLM mode..</p>", unsafe_allow_html=True)
            record_audio(language=lang, device_index=device)
            listen = speech_to_text.transcribe(filename_temp_audio)
            st.write(listen)
                
            screenshot = ScreenCommand(listen, lang, talk)
            if screenshot.screen():
                image_path = "photos/screenshot.png"
                if lang == 'Fr':
                    talk("Dites moi ce que je dois faire avec cette image ?")
                    lang_preprompt = "Parle en Français et réponds en français, "
                else:
                    talk("Tell me what I should do with this image ?")
                    lang_preprompt = "Speak in English and respond in English, "
                record_audio(language=lang, device_index=device)
                listen = speech_to_text.transcribe(filename_temp_audio)
                full_prompt = lang_preprompt + listen
                full_response, chat_history = analyze_image(image_path, full_prompt)

            screen_cam = CamCommand(listen, device, lang, talk)
            if screen_cam.screen_cam():
                image_path = "photos/camera.png"
                if lang == 'Fr':
                    talk("Dites moi ce que je dois faire avec cette image ?")
                    lang_preprompt = "Parle en Français et réponds en français,"
                else:
                    talk("Tell me what I should do with this image ?")
                    lang_preprompt = "Speak in English and respond in English,"

                record_audio(language=lang, device_index=device)
                listen = speech_to_text.transcribe(filename_temp_audio)
                full_prompt = lang_preprompt + listen
                full_response, chat_history = analyze_image(image_path, full_prompt)

            # Check if the user wants to save the conversation
            detect_save_keyords = ['sauvegarde notre discussion', 'sauvegarde notre conversation', 'sauvegarde la discussion', 'sauvegarde la conversation',
                                   'save our discussion', 'save our conversation', 'save the discussion', 'save the conversation']
            if any(keyword in listen for keyword in detect_save_keyords):
                talk("La conversation a été sauvegardé" if lang=='Fr' else "The conversation has been saved")
                st.success("Conversation sauvegardé" if lang == 'Fr' else "Conversation saved.")
                save_conversation(chat_history, hist_dir)
                continue

            # Check if the user wants to stop the LLM Vision for return to basic voice detection
            detect_stop_llm_keyords = ['désactive llm', 'désactive vision', 'passe en mode classique', 'passage en mode classique',
                                    'disable llm', 'switch to classic mode', 'switch classic mode']
            if any(keyword in listen for keyword in detect_stop_llm_keyords):
                if lang=='Fr':
                    talk("Passage en mode exécution de commandes")
                else: 
                    talk("Switching to commands execution mode")
                st.error("Stopping the vision with the model.")
                break