import streamlit as st
import os
import json
import string


def remove_punctuation_and_lowercase(input_string):
    # Remove punctuation and convert to lowercase
    return input_string.translate(str.maketrans('', '', string.punctuation)).lower()

def json_trigger_response(lang):
    # Create the folder if it doesn't exist
    if not os.path.exists('config_json'):
        os.makedirs('config_json')

    st.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    # Create input fields
    text_trigger = st.text_input("Texte déclencheur" if lang == 'Fr' else "Trigger text")
    text_response = st.text_input("Réponse au texte déclencheur" if lang == 'Fr' else "Response to trigger text")

    # Create the Record Button
    if st.button("Enregistrer" if lang == 'Fr' else "Save"):
        # Verify that both input fields have values
        if text_trigger and text_response:
            # Remove punctuation and convert to lowercase
            text_trigger = remove_punctuation_and_lowercase(text_trigger)

            # Load existing data
            if os.path.exists('config_json/text.json'):
                with open('config_json/text.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}

            # Update data with new entry
            data[text_trigger] = text_response

            # Write the updated data to the json file
            with open('config_json/text.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                
            st.success("Données enregistrées avec succès !" if lang == 'Fr' else "Successfully Recorded Data !")
        else:
            st.error("Veuillez remplir les deux champs de saisie." if lang == 'Fr' else "Please complete both input fields.")

    # Load and display existing data with delete buttons
    if os.path.exists('config_json/text.json'):
        with open('config_json/text.json', 'r', encoding='utf-8') as f:
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
                with open('config_json/text.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                    st.rerun()
