import streamlit as st
import os
import json
import string


def remove_punctuation_and_lowercase(input_string):
    # Remove punctuation and convert to lowercase
    return input_string.translate(str.maketrans('', '', string.punctuation)).lower()

def json_trigger_app(lang):
    # Create the folder if it doesn't exist
    if not os.path.exists('config_json'):
        os.makedirs('config_json')

    st.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    # Create input field for file path
    file_path = st.text_input("Chemin du fichier" if lang == 'Fr' else "File path")
    file_path = file_path.replace('"', '')

    # Create input field for trigger text
    text_trigger = st.text_input("Texte déclencheur" if lang == 'Fr' else "Trigger text")
    text_trigger = remove_punctuation_and_lowercase(text_trigger)

    # If a file path and a trigger text is provided
    if file_path and text_trigger:
        # Create the Record Button
        if st.button("Enregistrer" if lang == 'Fr' else "Save"):
            # Load existing data
            if os.path.exists('config_json/app.json'):
                with open('config_json/app.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}

            # Update data with new entry
            data[file_path] = text_trigger  # Change this line

            # Write the updated data to the json file
            with open('config_json/app.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)

            st.success("Données enregistrées avec succès !" if lang == 'Fr' else "Successfully Recorded Data !")
    elif text_trigger:
        st.error("Veuillez fournir un chemin de fichier." if lang == 'Fr' else "Please provide a file path.")
    elif file_path:
        st.error("Veuillez remplir le champ de saisie du texte déclencheur." if lang == 'Fr' else "Please fill in the trigger text input field.")

    # Load and display existing data with delete buttons
    if os.path.exists('config_json/app.json'):
        with open('config_json/app.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create a selectbox for the keys
        option = st.selectbox(
            'Choisissez une entrée à supprimer' if lang == 'Fr' else 'Choose an entry to delete',
            list(data.keys())
        )

        if option != None:
            # Create a delete button for the selected key
            if st.button("Supprimer '{}'".format(option) if lang == 'Fr' else "Delete '{}'".format(option)):
                del data[option]
                with open('config_json/app.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                    st.rerun()