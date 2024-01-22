import streamlit as st
import src.app.auth_test as auth
from streamlit.components.v1 import html

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)

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
# st.write(f'''<h1>
    # Please login using this <a target="_self"
    # href="{auth.get_login_url()}">url</a></h1>''',
        #  unsafe_allow_html=True)
st.button('Log in with google', on_click=open_page, args=(auth.get_login_url(),))
