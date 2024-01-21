import asyncio

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2


client_id = st.secrets['google_auth']['client_id']
client_secret = st.secrets['google_auth']['client_secret']
redirect_uri = st.secrets['google_auth']['redirect_uri']


def get_login_url():
    client: GoogleOAuth2 = GoogleOAuth2(client_id, client_secret)
    authorization_url = asyncio.run(
        get_authorization_url(client, redirect_uri))
    return authorization_url

async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
    return authorization_url

async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    return token

async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email

def get_user():
    client: GoogleOAuth2 = GoogleOAuth2(client_id, client_secret)
    # get the code from the url
    code = st.experimental_get_query_params()['code']
    token = asyncio.run(get_access_token(
        client, redirect_uri, code))
    user_id, _ = asyncio.run(
        get_email(client, token['access_token']))
    return user_id

# st.write(get_login_str(), unsafe_allow_html=True)
# display_user()