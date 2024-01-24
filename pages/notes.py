import streamlit as st
from src.app.auth import run_page
from src.app.misc import render_sidebar
import base64
from streamlit.components.v1 import html

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


def notes_page(user_id, user_email):
    file = st.session_state.get('file', None)
    md_notes = st.session_state.get('md_notes', None)
    sidebar, body = st.columns([1, 8])

    # def display_pdf(file):
        # base64_pdf = base64.b64encode(file).decode('utf-8')
# 
        # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
# 
        # body.write(pdf_display, unsafe_allow_html=True)

    render_sidebar(sidebar)

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
    body.markdown('Learning Copilot przyjmuje wykłady w formacie pdf i odczytuje tekst - nie potrafi interpretować obrazów. Ilość wygenerowanych notatek zależy od treścliwości stron wczytanego dokumentu.')
    if md_notes is not None:
        body.markdown(md_notes, unsafe_allow_html=True)

    if file is not None:
        body.download_button(
            label="Pobierz notatki",
            data=file,
            file_name=f"{st.session_state.get('title', 'notes')}.pdf",
            mime='application/pdf',
        )
    else:
        body.button(
            label="Pobierz notatki",
            disabled=True
        )

run_page(notes_page)
