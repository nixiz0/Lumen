import streamlit as st
import os


class NoteCommands:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk

    def vocal_note(self):
        text_note_keywords = ['lumen prends note', 'lumen prend note', 'lumen take note']
        for keyword in text_note_keywords:
            if keyword in self.listen:
                self.listen = self.listen.replace(keyword, '').strip()
                # Gets the user's download path
                download_path = os.path.join(os.path.expanduser("~"), 'Downloads')
                file_path = os.path.join(download_path, 'vocal_note.txt')
                
                # Checks if the file is empty or not
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    # If the file is not empty, append what the user said to the end of the file
                    with open(file_path, 'a', encoding="utf-8") as f:
                        f.write('\n' + self.listen)
                else:
                    # If the file is empty, writes what the user said to the file
                    with open(file_path, 'a', encoding="utf-8") as f:
                        f.write(self.listen)

                st.markdown(f"<p style='color:#c05bb6;'>{self.listen}</p>", unsafe_allow_html=True) # Display on the interface the note taken

                # Talk to the user
                if self.language == 'Fr':
                    self.talk("C'est noté")
                else: 
                    self.talk("Noted")