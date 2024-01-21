import streamlit as st
import src.app.auth_test as auth

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

st.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
st.write(f'''<h1>
    Please login using this <a target="_self"
    href="{auth.get_login_url()}">url</a></h1>''',
         unsafe_allow_html=True)
