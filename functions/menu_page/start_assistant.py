import streamlit as st 
import subprocess
import os

from functions.config_page.speech_to_text.speech import SpeechToText
from functions.config_page.selection_microphone import get_microphone
from functions.config_page.narrator_voice import NarratorVoice
from functions.config_page.speech_to_text.record import record_audio
from functions.menu_page.commands.json.load_json import load_sentences, load_app_paths
from functions.menu_page.commands.json.text_add_json import TextAddCommands
from functions.menu_page.commands.web.check_connection import is_connected
from functions.menu_page.commands.web.search_web import WebCommands
from functions.menu_page.commands.speech_to_en import SpeechToEnCommand
from functions.menu_page.commands.audio_gestion import VolumeCommands
from functions.menu_page.commands.app_chrono import ChronoCommand
from functions.menu_page.commands.take_note import NoteCommands
from functions.menu_page.commands.cybersec_info_system import InfoCommands
from functions.menu_page.commands.data_time import TimeCommands
from functions.menu_page.commands.screenshot import ScreenCommand
from functions.menu_page.commands.math_calcul import CalculCommands
from functions.menu_page.commands.cam.screen_cam import CamCommand
from functions.menu_page.commands.cam.video_command import VideoCommand
from functions.discussion_page.discussion_command import DiscussionCommand
from functions.code_page.code_command import CodeCommand
from functions.precision_page.precision_command import PrecisionCommand
from functions.vision_page.vision_command import VisionCommand


def run_assistant(lang):
    speech_to_text = SpeechToText()
    device = get_microphone(lang)
    voice = NarratorVoice(lang)
    record_working = True

    def talk(text):
        voice.speak(text)

    sentences = load_sentences()
    app_paths = load_app_paths()
    sorted_keys_sentences = sorted(sentences.keys(), key=len, reverse=True)
    sorted_keys_app_paths = sorted(app_paths.keys(), key=len, reverse=True)
    while True:
        if record_working == False:
            btn_unpause_conv = st.sidebar.button("Reprendre" if lang == 'Fr' else "Take back")
            if btn_unpause_conv:
                record_working = True

        if record_working:
            filename_temp_audio = 'functions/config_page/speech_to_text/temp_audio/audio.wav'
            record_audio(language=lang, device_index=device)
            listen = speech_to_text.transcribe(filename_temp_audio)
            st.write(listen)

        for key in sorted_keys_sentences:
            # Split the key and command into words
            key_words = key.split()
            command_words = listen.split()

            # Check if all words in the key are in the command and in the correct order
            if all(word in command_words[i:] for i, word in enumerate(key_words)):
                talk(sentences[key])
                break 

        for app_path in sorted_keys_app_paths:
            # Get the trigger phrase for this app path
            trigger_phrase = app_paths[app_path]

            # Split the trigger phrase and command into words
            trigger_words = trigger_phrase.split()
            command_words = listen.split()

            # Check if all words in the trigger phrase are in the command and in the correct order
            if all(word in command_words[i:] for i, word in enumerate(trigger_words)):
                if lang == 'Fr':
                    talk("Lancement de l'application " + trigger_phrase)
                else: 
                    talk("Starting the application " + trigger_phrase)
                subprocess.Popen(['start', app_path], shell=True)
                break

        if is_connected():
            # Search on Web Commands
            web_commands = WebCommands(listen, lang, talk)
            web_commands.search_ytb()
            web_commands.search_google()
            web_commands.search_wikipedia()
            web_commands.search_bing()
            web_commands.search_gpt()

        # Add JSON Text
        text_add = TextAddCommands(listen, device, lang, talk)
        text_add.add_text()

        # Translate language detected to English
        speech_to_en = SpeechToEnCommand(listen, device, lang, talk)
        speech_to_en.translate()

        # Volume-Commands
        volume_commands = VolumeCommands(listen, lang, talk)
        volume_commands.mute()
        volume_commands.demute()
        volume_commands.volume_increase()
        volume_commands.volume_decrease()

        # Start Chrono App
        start_chrono_app = ChronoCommand(listen, lang, talk)
        start_chrono_app.start_chrono()

        # Take Note (.txt) Command
        take_note_commands = NoteCommands(listen, lang, talk)
        take_note_commands.vocal_note()

        # Cyber-Commands (System Info)
        cyber_commands = InfoCommands(listen)
        cyber_commands.ip_config()
        cyber_commands.system_info()
        cyber_commands.net_info()
        cyber_commands.arp_info()
        cyber_commands.route_info()
        cyber_commands.schtasks_info()
        cyber_commands.driver_info()
        cyber_commands.msinfo32_info()

        # Actual Time/Date Commands
        time_commands = TimeCommands(listen, lang, talk)
        time_commands.time_command()
        time_commands.date_command()

        # Math Calcul-Commands
        calcul_commands = CalculCommands(listen, lang, talk)
        calcul_commands.calcul_command()
                    
        # Do screenshot of the actual screen
        screenshot_command = ScreenCommand(listen, lang, talk)
        screenshot_command.screen()

        # Do camera screenshot of the actual camera
        screen_cam_command = CamCommand(listen, device, lang, talk)
        screen_cam_command.screen_cam()

        # Start filming video & choose a camera
        video_capture = VideoCommand(listen, device, lang, talk)
        video_capture.start_video()

        # Start Discussion (use Ollama) 
        model_discu = os.path.join('save_config_txt', 'discussion_model.txt')
        hist_discu = 'functions/discussion_page/discussion_history'
        start_discussion = DiscussionCommand(listen, device, lang, talk, model_discu, hist_discu)
        start_discussion.launch_discussion_mode()

        # Start Coding (use Ollama) 
        model_code = os.path.join('save_config_txt', 'code_model.txt')
        hist_code = 'functions/code_page/code_history'
        start_code = CodeCommand(listen, device, lang, talk, model_code, hist_code)
        start_code.launch_code_mode()

        # Start Precision (use Ollama) 
        model_precision = os.path.join('save_config_txt', 'precision_model.txt')
        hist_precision = 'functions/precision_page/precision_history'
        start_precision = PrecisionCommand(listen, device, lang, talk, model_precision, hist_precision)
        start_precision.launch_precision_mode()

        # Start Vision LLM (use Ollama) 
        model_vision = os.path.join('save_config_txt', 'vision_model.txt')
        hist_vision = 'functions/vision_page/vision_history'
        start_llm_vision = VisionCommand(listen, device, lang, talk, model_vision, hist_vision)
        start_llm_vision.launch_vision_mode()



        # Pause Conversation
        pause_keywords = ['lumen mode pause', 'lumen mets-toi en pause', 'lumen mets toi en pause', 'lumen pause mode']
        if any(keyword in listen for keyword in pause_keywords):
            record_working = False
            continue
                            
        # Stop the system
        stop_keywords = ['lumen éteins-toi', 'lumen arrête-toi', 'lumen stop tout', 'lumen mode arrêt'
                         'lumen shutdown mode', 'lumen shoot down mode', 'lumen shootdown mode']
        if any(keyword in listen for keyword in stop_keywords):
            if lang == 'Fr':
                talk('Bien Monsieur, arrêt des systèmes en cours..')
            else: 
                talk('Yes sir, systems shutdown in progress..')
            record_working = False
            break
            