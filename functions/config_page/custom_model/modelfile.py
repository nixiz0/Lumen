import subprocess
import platform
import os
from colors import *


def interact_with_user():
    # Ask the user which language they want to use
    language = input(f"{CYAN} Type 1 for English, 2 for French : {RESET}")
    while language not in ['1', '2']:
        language = input(f"{RED}Invalid entry. Please type 1 for English, 2 for French : {RESET}")

    language = int(language)
    while True:
        try:
            if language == 2:
                user_input = input(f"{GREEN}\nTapez 1 pour afficher les modèles, 2 pour passer à l'étape suivante :\n{RESET}")
            else: 
                user_input = input(f"{GREEN}\nType 1 to view templates, 2 to go to next step :\n{RESET}")

            if user_input == '1':
                print("")
                subprocess.run(["ollama", "list"])
                break
            else:
                if language == 2:
                    print(f"{GREEN}\nPassage à l'étape suivante.{RESET}")
                else: 
                    print(f"{GREEN}\nMoving on to the next step.{RESET}")
                break
        except subprocess.CalledProcessError:
            if language == 2:
                print(f"{RED}Veuillez taper 1 ou 2.{RESET}")
            else: 
                print(f"{RED}Please type 1 or 2.{RESET}")

    while True:
        if language == 2:
            model_name = input(f"{GREEN}\nVeuillez entrer le nom du modèle que vous souhaitez afficher :\n{RESET}")
        else: 
            model_name = input(f"{GREEN}\nPlease enter the model name you want to display :\n{RESET}")
            
        try:
            print("")
            subprocess.run(["ollama", "show", model_name, "--modelfile"], check=True)
            break
        except subprocess.CalledProcessError:
            if language == 2:
                print(f"{RED}Le nom du modèle n'est pas valide. Veuillez réessayer.{RESET}")
            else: 
                print(f"{RED}The model name is invalid. Try Again.{RESET}")

    # Set messages according to your chosen language
    if language == 2:
        messages = {
            "edit_message": "\nTapez 1 quand vous avez fini d'éditer le fichier Modelfile :\n",
            "model_message": "\nVeuillez entrer le nom du modèle que vous souhaitez créer :\n"
        }
    else:
        messages = {
            "edit_message": "\nType 1 when you have finished editing the Modelfile :\n",
            "model_message": "\nPlease enter the name of the model you wish to create :\n"
        }

    # Create the folder if it doesn't exist
    file_path = 'functions/config_page/custom_model/temp_modelfile'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # Create the Modelfile
    with open(f'{file_path}/Modelfile', 'w') as f:
        f.write('')

    # Open the file via a text editor
    if platform.system() == 'Windows':
        os.startfile(os.path.abspath(f'{file_path}/Modelfile'))
    elif platform.system() == 'Linux':
        subprocess.run(["xdg-open", os.path.abspath(f'{file_path}/Modelfile')])

    # Ask the user to type 1 when finished
    user_input = input(messages["edit_message"])
    while user_input != '1':
        user_input = input(messages["edit_message"])

    # Ask the user the name of the model they want
    model_name = input(messages["model_message"])

    # Run the ollama create command
    subprocess.run(["ollama", "create", model_name, "--file", os.path.abspath(f'{file_path}/Modelfile')])


interact_with_user()