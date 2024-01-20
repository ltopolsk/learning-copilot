import streamlit as st
import streamlit.components.v1 as components

# if 'genNotes' not in st.session_state:
#     st.session_state.disabled = True
# 
st.markdown('<h1>Learning Copilot</h1>')
uploaded = st.file_uploader('Dodaj prezentację123')
clicked = st.button('Wygeneruj notatki', disabled=True, key='genNotes')
# 
if uploaded is not None:
    st.text('HOORAY')
# 
# with open("style.css") as style:
#     st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)

# st.markdown("""<html>
# <body>
# <div style="width: 100%; height: 100%; position: relative; background: white">
#     <div style="width: 216px; height: 40px; left: 462px; top: 115px; position: absolute"></div>
#     <div style="width: 395px; height: 75px; left: 356px; top: 106px; position: absolute; color: black; font-size: 36px; font-family: Comfortaa; font-weight: 400; word-wrap: break-word">Learning Copilot 📚 </div>
#     <div style="width: 387px; height: 59px; left: 113px; top: 243px; position: absolute; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25)">
#         <div style="width: 387px; height: 59px; left: 0px; top: 0px; position: absolute; background: black; border-radius: 6px; border: 2px black solid"></div>
#         <div style="left: 145.29px; top: 23px; position: absolute; text-align: center; color: white; font-size: 13px; font-family: Roboto; font-weight: 900; text-transform: uppercase; letter-spacing: 0.52px; word-wrap: break-word">REJESTRACJA</div>
#     </div>
#     <div style="width: 387px; height: 59px; left: 599px; top: 243px; position: absolute; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25)">
#         <div style="width: 387px; height: 59px; left: 0px; top: 0px; position: absolute; background: black; border-radius: 6px; border: 2px black solid"></div>
#         <div style="left: 153.29px; top: 23px; position: absolute; text-align: center; color: white; font-size: 13px; font-family: Roboto; font-weight: 900; text-transform: uppercase; letter-spacing: 0.52px; word-wrap: break-word">LOGOWANIE</div>
#     </div>
# </div>
# </body>r
# </html>
# """, unsafe_allow_html=True)

# # st.markdown("<h1>Hello, World</h1>", unsafe_allow_html=True)

# # st.write("Learning Copilot 📚")
# # st.button("Rejestracja")
# # st.markdown('<div style="width: 100%; height: 100%; position: relative; background: white">', unsafe_allow_html=True)

