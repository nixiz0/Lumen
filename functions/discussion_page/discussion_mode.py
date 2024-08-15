import streamlit as st
import os
from functions.config_page.speech_to_text.speech import SpeechToText
from functions.config_page.speech_to_text.record import record_audio
from functions._functions_global_.llm_model_functions.llm_generate import LLMGenerate
from functions._functions_global_.llm_model_functions.llm_save_hist import save_conversation


def start_discussion(device, lang, talk, model_path, hist_dir):
    llm = LLMGenerate(talk)
    conversation_history = []
    speech_to_text = SpeechToText()
    working = True
    filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'

    if os.path.isfile(model_path):
        with open(model_path, 'r') as file:
            llm_model = file.read().strip()
    else:
        st.sidebar.error("Veuillez configurer le modèle à utiliser dans la page discussion." if lang == 'Fr' else 
                         "Please configure the template to be used in the discussion page.")

    while True:
        if working:
            st.markdown("<p style='font-weight: bold; color:#c05bb6;'>Mode texte LLM..</p>" if lang == 'Fr' else 
                        "<p style='font-weight: bold; color:#c05bb6;'>Text LLM mode..</p>", unsafe_allow_html=True)
            record_audio(language=lang, device_index=device)
            listen = speech_to_text.transcribe(filename_temp_audio)

            # Check if the user wants to save the conversation
            detect_save_keyords = ['sauvegarde notre discussion', 'sauvegarde notre conversation', 'sauvegarde la discussion', 'sauvegarde la conversation',
                                    'save our discussion', 'save our conversation', 'save the discussion', 'save the conversation']
            if any(keyword in listen for keyword in detect_save_keyords):
                talk("La conversation a été sauvegardé" if lang=='Fr' else "The conversation has been saved")
                st.success("Conversation sauvegardé" if lang == 'Fr' else "Conversation saved.")
                save_conversation(chat_history, hist_dir)
                continue

            # Check if the user wants to stop the LLM conversation for return to basic voice detection
            detect_stop_llm_keyords = ['c\'est bon tu peux arrêter', 'tu peux arrêter', 'désactive llm',
                                       'passe en mode classique', 'passage en mode classique',
                                       'passe classique','disable llm', 'switch to classic mode',
                                       'switch classic mode', 'it\'s okay you can stop', 'it is okay you can stop', 'you can stop']
            if any(keyword in listen for keyword in detect_stop_llm_keyords):
                talk("Passage en mode exécution de commandes" if lang == 'Fr' else "Switching to commands execution mode")
                st.error("Arrêt de la conversation avec le LLM" if lang == 'Fr' else "Stopping the conversation with the LLM.")
                working = False
                break

            # Generate a response
            lang_preprompt = "Réponds en français, " if lang == 'Fr' else "Respond in English, "
            user_input_str = str(listen)
            full_prompt_user = lang_preprompt + user_input_str
            _, chat_history = llm.generate_response(llm_model, full_prompt_user, conversation_history)