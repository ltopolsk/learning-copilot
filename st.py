import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
from mongo import DBClient

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide"
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
button.st-emotion-cache-19rxjzo {
    height: auto;
    width: inherit;
}
</style>
""",
    unsafe_allow_html=True,
)

import requests

def get_external_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Unknown"

external_ip = get_external_ip()
st.write("External IP:", external_ip)

#db_client = DBClient(config=st.secrets["mongo"])
# def clear_name():
st.session_state.title = None

def disable():
    st.session_state.disabled = True

def enable():
    st.session_state.disabled = False

def upload_file():
    if not st.session_state.get('file_uploaded', False):
        enable()
    else:
        disable()

if 'genNotes' not in st.session_state:
    st.session_state.disabled = True
if 'genQuiz' not in st.session_state:
    st.session_state.disabled = True

sidebar, body = st.columns([1, 10])

home_button = sidebar.button('HOME', key='homeButton')

if home_button:
    switch_page("st")

notes_expander = sidebar.expander("NOTES")
#for x in db_client.get_notes("Client1"):
 #   notes_expander.button(x['filename'])

body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
uploaded = body.file_uploader(label='Dodaj plik',on_change=upload_file, type=['pdf', 'pptx'])
title = body.text_input('Wprowadź tytuł notatek/quizu')

if title is not None and title != '':
    st.session_state.title = title

col1, col2 = body.columns(2)
clicked_notes = col1.button('Wygeneruj notatki', key='genNotes', disabled=st.session_state.disabled)
clicked_quiz = col2.button('Wygeneruj quiz', key='genQuiz', disabled=st.session_state.disabled)

if uploaded is not None:
    st.session_state.file_uploaded=True
    bytes_data = uploaded.getvalue()
    st.session_state.file = bytes_data
else:
    st.session_state.file_uploaded=False

if clicked_notes:
  #  with st.spinner("Processing..."):
   #     db_client.upload_notes('Client1', bytes_data, title)
    switch_page("main_notes")


# def process_file():

# # st.write("Learning Copilot 📚")
# # st.button("Rejestracja")
# # st.markdown('<div style="width: 100%; height: 100%; position: relative; background: white">', unsafe_allow_html=True)

