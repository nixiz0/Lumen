import streamlit as st
import json


def load_and_display_chat(filename):
    # Load the chat history from the json file
    with open(filename, 'r', encoding='utf-8') as f:
        chat_history = json.load(f)

    # Store the chat history in the session state
    st.session_state['session_state'] = chat_history

    # Display the chat history on Streamlit
    for message in st.session_state['session_state']:
        with st.chat_message(message['role']):
            st.write(message['content'])
