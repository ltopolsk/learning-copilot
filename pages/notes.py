import streamlit as st
from streamlit_extras.switch_page_button import switch_page
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



file = st.session_state.get('file', None)

sidebar, body = st.columns([1, 10])

home_button = sidebar.button('HOME', key='homeButton', use_container_width=True)
def display_pdf(file:bytes):
    # Opening file from file path
    base64_pdf = base64.b64encode(file).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    body.markdown(pdf_display, unsafe_allow_html=True)

def display_latex(latex_string):
    # Opening file from file path
    # base64_pdf = base64.b64encode(file).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:text/plain{latex_string}" width="100%" height="1000" type="text/plain"></iframe>'

    # Displaying File
    body.markdown(pdf_display, unsafe_allow_html=True)


if home_button:
    switch_page("st")

body.markdown('<h1>Learning Copilot</h1>', unsafe_allow_html=True)
display_pdf(file)
# if file is not None:
#     body.download_button(
#         label="Pobierz notatki",
#         data=file,
#         file_name=f"{st.session_state.get('title', 'notes')}.tex",
#         mime='text/plain',
#     )
# else:
#     body.button(
#         label="Pobierz notatki",
#         disabled=True
#     )
