import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from src.app.auth import run_page
from src.app.misc import render_sidebar

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

    # def display_pdf(file:bytes):
    #     # Opening file from file path
    #     base64_pdf = base64.b64encode(file).decode('utf-8')

    #     # Embedding PDF in HTML
    #     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'

    #     # Displaying File
    #     body.markdown(pdf_display, unsafe_allow_html=True)

    # def display_latex(latex_string):
    #     # Opening file from file path
    #     # base64_pdf = base64.b64encode(file).decode('utf-8')

    #     # Embedding PDF in HTML
    #     pdf_display = f'<iframe src="data:text/plain{latex_string}" width="100%" height="1000" type="text/plain"></iframe>'

    #     # Displaying File
    #     body.markdown(pdf_display, unsafe_allow_html=True)

    render_sidebar(sidebar)

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
    if file is not None:
        body.download_button(
            label="Pobierz notatki",
            data=file,
            file_name=f"{st.session_state.get('title', 'notes')}.tex",
            mime='text/plain',
        )
    else:
        body.button(
            label="Pobierz notatki",
            disabled=True
        )

run_page(notes_page)