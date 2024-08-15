import streamlit as st
import base64
from PIL import Image
from io import BytesIO

from functions._ui_global.page_title import set_page_title
from functions._ui_global.custom_ui import custom_ui
from functions.menu_page.get_language import define_lang
from functions.menu_page.start_assistant import run_assistant


# Add a language switcher to the sidebar
lang = define_lang()
st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Activate the Assistant
activate_assistant = st.sidebar.checkbox("Activer l'Assistant" if lang == 'Fr' else "Enable Assistant")
if activate_assistant:
    st.warning("Mettre pause l'Assistant dire:" if lang == 'Fr' else "Pause the Assistant say:")
    st.warning("['mode pause', 'mets-toi en pause', 'mets toi en pause', 'pause mode']")

    st.error("Stopper l'Assistant dire: " if lang == 'Fr' else "Stop the Assistant say:")
    st.error("['éteins-toi', 'arrête-toi', 'stop tout', 'mode arrêt', 'shutdown mode', 'shoot down mode', 'shootdown mode']")

    st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)
    run_assistant(lang)

# Open image
logo_entreprise = Image.open('ressources/lumen_logo.png')

# Convert image to base64 to display in markdown
buffered = BytesIO()
logo_entreprise.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Show image centered
st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_str}' width='450'/></div>", unsafe_allow_html=True)

# Add an H2 title
if lang == 'Fr':
    st.markdown("<h2 style='text-align: center;'>Bienvenue sur votre Lumen</h2>", unsafe_allow_html=True)
elif lang == 'En':
    st.markdown("<h2 style='text-align: center;'>Welcome to your Lumen</h2>", unsafe_allow_html=True)

# Presentation Text
if lang == 'Fr':
    st.markdown("<p style='text-align: center;'> \
                Lumen est un assistant intelligent capable de voir 👀 écouter 👂 discuter 💬 et coder 💻 \
                vous permettant de naviguer sur le web, contrôler votre multimédia et automatiser des tâches \
                en toute simplicité. <br><br>Avec ses capacités de reconnaissance visuelle et vocale, Lumen s'adapte \
                à vos besoins pour optimiser votre productivité et enrichir votre expérience numérique.<br><br> \
                Découvrez une nouvelle façon d'interagir avec la technologie grâce à Lumen, \
                votre partenaire technologique au quotidien. ✨ \
                </p>", 
                unsafe_allow_html=True)
elif lang == 'En':
    st.markdown("<p style='text-align: center;'> \
                Lumen is an intelligent assistant capable of seeing 👀 listening 👂 conversing 💬 and coding 💻 \
                allowing you to browse the web, control your multimedia, and automate tasks with ease.<br><br> \
                With its visual and voice recognition capabilities, Lumen adapts to your needs to enhance \
                productivity and enrich your digital experience. <br><br>Discover a new way to interact with technology \
                with Lumen, your everyday tech partner. ✨ \
                </p>", 
                unsafe_allow_html=True)

# Use the function to set the page title
set_page_title("Menu · Streamlit", "Menu")
custom_ui()