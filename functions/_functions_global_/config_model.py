import streamlit as st 
import os 

from functions._functions_global_.get_model import get_model_names


def configuration_model(lang, filename_model):
    # Get the names of the models
    model_names = get_model_names()
    model_names.insert(0, "")

    # Select model
    model_use = st.sidebar.selectbox('🔬 Modèles' if lang == "Fr" else '🔬 Models', model_names)

    # Create the folder if it doesn't exist
    if not os.path.exists('save_config_txt'):
        os.makedirs('save_config_txt')

    # Write the name of the model in the .txt only if a model is selected
    if model_use != "":
        with open(filename_model, 'w') as f:
            f.write(model_use)
