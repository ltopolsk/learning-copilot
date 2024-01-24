import streamlit as st
from src.app.auth import run_page
from src.app.misc import render_sidebar
import base64


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
    sidebar, body = st.columns([1, 8])

    def display_pdf(file):
        base64_pdf = base64.b64encode(file).decode('utf-8')

        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000"></embed>'

        body.markdown(pdf_display, unsafe_allow_html=True)

    render_sidebar(sidebar)

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)

    if file is not None:
        display_pdf(file)
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
