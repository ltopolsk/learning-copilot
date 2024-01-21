import streamlit as st
import src.app.auth_test as auth
from streamlit_extras.switch_page_button import switch_page

st.session_state.user_id = auth.get_user()
switch_page("st")
