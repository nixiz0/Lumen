import streamlit as st


def set_page_title(title, user_title):
    if title != user_title:
        title = user_title
        st.markdown(unsafe_allow_html=True, body=f"""
            <iframe height=0 srcdoc="<script>
                parent.document.title = '{title}';
            </script>" />
        """)
