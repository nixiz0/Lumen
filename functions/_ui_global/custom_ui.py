import streamlit as st


def custom_ui():
    # Hide deploybutton in streamlit ui
    st.markdown("""
        <style>
        .stDeployButton {display:none;}
        </style>
        """, unsafe_allow_html=True)