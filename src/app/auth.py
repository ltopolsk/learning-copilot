import asyncio
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2

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

def run_page(page):

    client_id = st.secrets['google_auth']['client_id']
    client_secret = st.secrets['google_auth']['client_secret']
    redirect_uri = st.secrets['google_auth']['redirect_uri']
    client = GoogleOAuth2(client_id, client_secret)

    authorization_url = asyncio.run(
        write_authorization_url(client=client,
                                redirect_uri=redirect_uri)
    )
    if st.session_state.get('token', None) is None:
        try:
            code = st.experimental_get_query_params()['code']
        except:
            st.write('''<h1>Learning Copilot 📚</h1>''',unsafe_allow_html=True)
            st.link_button('Zaloguj sie z użyciem konta Google', url=authorization_url)
        else:
            # Verify token is correct:
            try:
                token = asyncio.run(
                    write_access_token(client=client,
                                       redirect_uri=redirect_uri,
                                       code=code))
            except:
                st.write('''<h1>Learning Copilot 📚</h1>''',unsafe_allow_html=True)
                st.link_button('Zaloguj sie z użyciem konta Google', url=authorization_url)
            else:
                st.session_state.token = token
                user_id, user_email = asyncio.run(
                    get_email(client=client,
                            token=token['access_token'])
                    )
                st.session_state.user_id = user_id
                st.session_state.user_email = user_email
                page(user_id=st.session_state.user_id,
                         user_email=st.session_state.user_email)
    else:
        page(user_id=st.session_state.user_id,
             user_email=st.session_state.user_email)