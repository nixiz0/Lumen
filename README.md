
# **Lumen** (for Windows)

**Assistant to support you in your projects and tasks.**


## Installation

Run the **start-assistant.bat** and follow the instructions on the shell.

**ATTENTION :**
This application is not suitable for **Mac** and **Linux** and may not work depending on the hardware of your Windows computer.
## Synthetic Voices

If you want to have more synthetic voices available, on Windows you have to go to the narrator settings and you can download the voices you want.

If this doesn't work and doesn't recognize the voices you have installed on the narrator settings, follow this steps :
1. Open the **Registry Editor** by pressing the **“Windows” and “R”** keys simultaneously, then type **“regedit”** and press Enter.

2. Navigate to the registry key : **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens**.

3. Export this key to a **REG file** (with a right click on the file).

4. Open this file with a text editor and replace all occurrences of **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens** 
with **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens**.

5. Save the modified file and double-click it to import the changes to the registry.


## Tech Stack

**Language :** Python 3.11.7

**CUDA Compiler/Toolkit** : Cuda 11.8

**Local AI Models:** Ollama (version 0.3.2)

**Voice Recognition:** openai/whisper-large-v3

**Audio Device Scanning:** pyaudio

**Synthetic Voices:** pyttsx3

**Interface:** streamlit

**Computer Commands:** webbrowser (search on web) / pywhatkit (search on youtube) / pycaw (change volume computer) / sympy (calcul)


## Author

- [@nixiz0](https://github.com/nixiz0)
