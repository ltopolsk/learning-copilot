import streamlit as st
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
from src.app.mongo import DBClient
from src.gpt.gptApi import gptManager
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


async def write_authorization_url(client,
                                  redirect_uri):
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["profile", "email"],
        extras_params={"access_type": "online"},
    )
    return authorization_url


async def write_access_token(client,
                             redirect_uri,
                             code):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client,
                    token):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def main(user_id, user_email):
    st.session_state.user_id=user_id
    db_client = DBClient(config=st.secrets["mongo"])
    gpt_manager = gptManager(**st.secrets["gpt_api"])
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

    def get_doc(user_id, filename):
        st.session_state.title = filename
        st.session_state.file = db_client.get_one_pdf(user_id,filename)

    notes_expander = sidebar.expander("NOTES")
    notes_expander_buttons = []
    for x in db_client.get_notes(st.session_state.user_id):
        notes_expander_buttons.append(notes_expander.button(x['filename'], use_container_width=True, key=x["filename"]))

    # if any(notes_expander_buttons):
        # switch_page("main_notes")

    # quizes_expander = sidebar.expander("QUIZES")
    # for x in db_client.get_quizes("Client1"):
    #    quizes_expander.button(x['filename'], use_container_width=True, key=f'{x["filename"]}Quiz')

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
    uploaded = body.file_uploader(label='Dodaj plik',on_change=upload_file, type=['pdf', 'pptx'])
    title = body.text_input('Wprowadź tytuł notatek/quizu')

    if title is not None and title != '':
        st.session_state.title = title

    save_result = body.checkbox('Zapisz quiz/notatki na później')
    col1, col2 = body.columns(2)
    clicked_notes = col1.button('Wygeneruj notatki', key='genNotes', disabled=st.session_state.disabled,use_container_width=True)
    clicked_quiz = col2.button('Wygeneruj quiz', key='genQuiz', disabled=st.session_state.disabled,use_container_width=True)

    if uploaded is not None:
        st.session_state.file_uploaded=True
        bytes_data = uploaded.getvalue()
        # st.session_state.file = bytes_data
    else:
        st.session_state.file_uploaded=False

    if clicked_notes:
        # with st.spinner("Processing..."):
        #     st.session_state.file = open("main.tex").read()
        #     if save_result:
        #         db_client.upload_notes(st.session_state.user_id, st.session_state.file, title)
        switch_page("main_notes")
    # if clicked_quiz:
        # with st.spinner("Processing..."):
            # print(gpt_manager.forward_read(uploaded, 'quiz'), file=open('quiz.json','w'))
            # if save_result:
                # db_client.upload_notes(st.session_state.user_id, st.session_state.file, title)
        # switch_page("main_notes")


if __name__ == '__main__':
    client_id = st.secrets['google_auth']['client_id']
    client_secret = st.secrets['google_auth']['client_secret']
    redirect_uri = st.secrets['google_auth']['redirect_uri']

    client = GoogleOAuth2(client_id, client_secret)
    authorization_url = asyncio.run(
        write_authorization_url(client=client,
                                redirect_uri=redirect_uri)
    )

    session_state = st.session_state
    if session_state.get('token', None) is None:
        try:
            code = st.experimental_get_query_params()['code']
        except:
            st.write(f'''<h1>Please login using Google account</h1>''',unsafe_allow_html=True)
            if st.button('Log in with google'):
                st.markdown(f"""<meta http-equiv="refresh" content="0; url='{authorization_url}'" />""",
                            unsafe_allow_html=True)
        else:
            # Verify token is correct:
            try:
                token = asyncio.run(
                    write_access_token(client=client,
                                       redirect_uri=redirect_uri,
                                       code=code))
            except:
                st.write('''<h1>Please login using Google account</h1>''',unsafe_allow_html=True)
                if st.button('Log in with google'):
                    st.markdown(f"""<meta http-equiv="refresh" content="0; url='{authorization_url}'" />""",
                                unsafe_allow_html=True)
            else:
                # Check if token has expired:
                session_state.token = token
                user_id, user_email = asyncio.run(
                    get_email(client=client,
                            token=token['access_token'])
                    )
                session_state.user_id = user_id
                session_state.user_email = user_email
                main(user_id=session_state.user_id,
                         user_email=session_state.user_email)
    else:
        main(user_id=session_state.user_id,
             user_email=session_state.user_email)

