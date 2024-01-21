import streamlit as st
from streamlit_extras.switch_page_button import switch_page

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



# with open('data/MED_dokumentacja.pdf', "rb") as f:
file = st.session_state.get('file', None)

sidebar, body = st.columns([1, 10])

home_button = sidebar.button('HOME', key='homeButton', use_container_width=True)

if home_button:
    switch_page("st")

body.markdown('<h1>Learning Copilot</h1>', unsafe_allow_html=True)
if file is not None:
    body.download_button(
        label="Pobierz notatki",
        data=file,
        file_name=f"{st.session_state.get('title', 'notes')}.tex",
        mime='text/plain',
        # disabled=(file is not None)
    )
else:
    body.button(
        label="Pobierz notatki",
        disabled=True
    )
