import os
import string
import base64
import streamlit as st
import pandas as pd
import json


class AppButton:
    def __init__(self, lang, history_dir, selected_file):
        self.lang = lang
        self.history_dir = history_dir
        self.selected_file = selected_file

    def rename_file(self):
        new_file_name = st.sidebar.text_input('Nouveau nom' if self.lang == 'Fr' else 'New name')
        if new_file_name:
            new_file_name = new_file_name.translate(str.maketrans('', '', string.punctuation))
            if st.sidebar.button('Renommer' if self.lang == 'Fr' else 'Rename'):
                if not new_file_name.endswith('.json'):
                    new_file_name += '.json'
                os.rename(os.path.join(self.history_dir, self.selected_file), os.path.join(self.history_dir, new_file_name))
                st.rerun()
        else:
            st.sidebar.warning('Veuillez entrer un nom de fichier.' if self.lang == 'Fr' else 'Please enter a file name.')

    def delete_file(self):
        if st.sidebar.button('Supprimer' if self.lang == 'Fr' else 'Delete'):
            os.remove(os.path.join(self.history_dir, self.selected_file))
            st.rerun()
    
    def download_as_csv(self):
        if st.sidebar.button('Télécharger CSV' if self.lang == 'Fr' else 'Download CSV'):
            with open(os.path.join(self.history_dir, self.selected_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False, encoding='utf-8')
                b64 = base64.b64encode(csv.encode()).decode()
                csv_file_name = self.selected_file.replace('.json', '.csv')
                if self.lang == 'Fr':
                    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file_name}">Cliquez pour télécharger</a>'
                else: 
                    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file_name}">Click to download</a>'
                st.sidebar.markdown(href, unsafe_allow_html=True)