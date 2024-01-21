import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import src.app.auth_test as auth
from mongo import DBClient

if st.session_state.get('user_id', None) is None:
    switch_page('login')

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

db_client = DBClient(config=st.secrets["mongo"])
def clear_name():
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

home_button = sidebar.button('HOME', key='homeButton', use_container_width=True)

if home_button:
    switch_page("st")

def get_doc(file_id, filename):
    # print(file_id)
    st.session_state.title = filename
    st.session_state.file = db_client.get_one_pdf(file_id)
    # switch_page("main_notes")

notes_expander = sidebar.expander("NOTES")
notes_expander_buttons = []
for x in db_client.get_notes(st.session_state.user_id):
    notes_expander_buttons.append(notes_expander.button(x['filename'], use_container_width=True, key=x["file_id"], on_click=get_doc, args=(x['file_id'],x['filename'])))

# print(notes_expander_buttons)
if any(notes_expander_buttons):
    switch_page("main_notes")
# quizes_expander = sidebar.expander("QUIZES")
# for x in db_client.get_quizes("Client1"):
#    quizes_expander.button(x['filename'], use_container_width=True, key=f'{x["filename"]}Quiz')

body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
uploaded = body.file_uploader(label='Dodaj plik',on_change=upload_file, type=['pdf', 'pptx'])
title = body.text_input('Wprowadź tytuł notatek/quizu')

if title is not None and title != '':
    st.session_state.title = title

col1, col2 = body.columns(2)
clicked_notes = col1.button('Wygeneruj notatki', key='genNotes', disabled=st.session_state.disabled,use_container_width=True)
clicked_quiz = col2.button('Wygeneruj quiz', key='genQuiz', disabled=st.session_state.disabled,use_container_width=True)

if uploaded is not None:
    st.session_state.file_uploaded=True
    bytes_data = uploaded.getvalue()
    st.session_state.file = bytes_data
else:
    st.session_state.file_uploaded=False

if clicked_notes:
    with st.spinner("Processing..."):
       db_client.upload_notes(st.session_state.user_id, bytes_data, title)
    switch_page("main_notes")

