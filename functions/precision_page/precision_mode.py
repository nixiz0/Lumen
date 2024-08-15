import streamlit as st
import os
import time
from functions.config_page.speech_to_text.speech import SpeechToText
from functions.config_page.speech_to_text.record import record_audio
from functions._functions_global_.llm_model_functions.llm_generate import LLMGenerate
from functions._functions_global_.llm_model_functions.llm_save_hist import save_conversation


def start_precision(device, lang, talk, model_path, hist_dir):
    llm = LLMGenerate(talk)
    conversation_history = []
    speech_to_text = SpeechToText()
    working = True
    filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'

    if os.path.isfile(model_path):
        with open(model_path, 'r') as file:
            llm_model = file.read().strip()
    else:
        st.sidebar.error("Veuillez configurer le modèle à utiliser dans la page précision." if lang == 'Fr' else 
                         "Please configure the template to be used in the precision page.")
        
    detect_element_keywords = ['je veux rentrer des données', 'aide moi sur ça', 'je veux rentrer du code', 'insérer des éléments'
                               'insérer un élément', 'I want to enter code', 'help me on this', 'insert elements']
    st.success(f"Si vous souhaitez rentrer des éléments pour parler dessus dire {detect_element_keywords}" if lang == 'Fr' else 
               f"If you want to enter some elements to talk about it, say {detect_element_keywords}")

    def ask_user_intent():
        trigger_phrases = ["c'est bon", "j'ai déposé mon élément", "j'ai déposé mes éléments", "code déposé", "éléments déposé", "élément déposé", 
                           "it's okay", "I submitted my code", 'code submitted', "it is okay", "okai", "ok", "okay", 
                           "I submitted my element", "I submitted my elements"]
        st.warning(f"Pour continuer, dire:\n {trigger_phrases}\n") if lang == 'Fr' else print(f"To continue, say:\n{trigger_phrases}\n")

        # Create the path if it doesn't exist
        file_path = 'functions/precision_page/temp_element/temp_element.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # clean the file before opening it
        with open(file_path, 'w') as file:
            file.write('')
            
        os.system(f'notepad {file_path}')
        while True:
            record_audio(language=lang, device_index=device)
            listen = speech_to_text.transcribe(filename_temp_audio)
            if any(keyword in listen for keyword in trigger_phrases):
                break
            time.sleep(1)

        with open(file_path, 'r') as file:
            elements = file.read()

        if lang == 'Fr':
            talk("Que voulez-vous faire avec le/les élément/s fourni/s ?")
        else: 
            talk("What do you want to do with the element/s provided ?")
        record_audio(language=lang, device_index=device)
        user_intent = speech_to_text.transcribe(filename_temp_audio)
        return elements, user_intent

    while True:
        if working:
            st.markdown("<p style='font-weight: bold; color:#c05bb6;'>Mode Précision LLM..</p>" if lang == 'Fr' else 
                        "<p style='font-weight: bold; color:#c05bb6;'>Precision LLM mode..</p>", unsafe_allow_html=True)
            record_audio(language=lang, device_index=device)
            listen = speech_to_text.transcribe(filename_temp_audio)

            # Check if the user wants to enter elements
            if any(keyword in listen for keyword in detect_element_keywords):
                elements, user_intent = ask_user_intent()
                    
                if lang == 'Fr':
                    lang_preprompt = "Parle en Français et réponds en français, "
                else: 
                    lang_preprompt = "Speak in English and respond in English, "
                full_prompt_user = lang_preprompt + user_intent
                _, chat_history = llm.generate_response(llm_model, full_prompt_user + " " + elements, conversation_history)
                continue

            # Check if the user wants to save the conversation
            detect_save_keyords = ['sauvegarde notre discussion', 'sauvegarde notre conversation', 'sauvegarde la discussion', 'sauvegarde la conversation',
                                    'save our discussion', 'save our conversation', 'save the discussion', 'save the conversation']
            if any(keyword in listen for keyword in detect_save_keyords):
                talk("La conversation a été sauvegardé" if lang=='Fr' else "The conversation has been saved")
                st.success("Conversation sauvegardé" if lang == 'Fr' else "Conversation saved.")
                save_conversation(chat_history, hist_dir)
                continue

            # Check if the user wants to stop the LLM conversation for return to basic voice detection
            detect_stop_llm_precision_keyords = ['c\'est bon tu peux arrêter', 'tu peux arrêter', 'désactive llm', 'passe en mode classique', 
                                            'passage en mode classique', 'désactive précision llm', 'passe classique','disable llm',
                                            'switch to classic mode','switch classic mode', 'disable precision llm', 
                                            'it\'s okay you can stop', 'it is okay you can stop', 'you can stop']
            if any(keyword in listen for keyword in detect_stop_llm_precision_keyords):
                talk("Passage en mode exécution de commandes" if lang == 'Fr' else "Switching to commands execution mode")
                st.error("Arrêt du mode précision." if lang == 'Fr' else "Stopping the precision mode.")
                working = False
                break

            # Generate a response
            lang_preprompt = "Réponds en français, " if lang == 'Fr' else "Respond in English, "
            user_input_str = str(listen)
            full_prompt_user = lang_preprompt + user_input_str
            _, chat_history = llm.generate_response(llm_model, full_prompt_user, conversation_history)