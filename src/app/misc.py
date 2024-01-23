import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from md2pdf.core import HTML, markdown, CSS

def render_sidebar(sidebar):
    home_button = sidebar.button('HOME', key='homeButton', use_container_width=True)

    if home_button:
        switch_page("main_page")

    def get_notes(notes_id):
        notes = st.session_state.db.get_one_notes(st.session_state.user_id, notes_id)
        st.session_state.file = notes['file']
        st.session_state.title = notes['title']

    notes_expander = sidebar.expander("NOTES")
    notes_expander_buttons = []
    for x in st.session_state.db.get_notes(st.session_state.user_id):
        notes_expander_buttons.append(notes_expander.button(x['title'], use_container_width=True, key=f'{x["_id"]}_notes', on_click=get_notes, args=(x['_id'],)))

    if any(notes_expander_buttons):
        switch_page("notes")

    def get_quiz(quiz_id):
        st.session_state.quiz = st.session_state.db.get_one_quiz(st.session_state.user_id, quiz_id)['quiz']
 
    quizes_expander = sidebar.expander("QUIZES")
    quizes_expander_buttons = []
    for x in st.session_state.db.get_quizes(st.session_state.user_id):
       quizes_expander_buttons.append(quizes_expander.button(x['name'], use_container_width=True, key=f'{x["_id"]}_quiz', on_click=get_quiz, args=(x['_id'],)))

    if any(quizes_expander_buttons):
        switch_page("quiz")
    
    logout_button = sidebar.button('Wyloguj się', key='logoutButton', use_container_width=True)
    if logout_button:
        st.session_state.token = None
        st.rerun()

def render_pdf(md_content):
    html = HTML(string=markdown(md_content, extras=['fenced-code-blocks', 'cuddled-lists']))
    font = CSS(string="body{font-family: Arial, sans-serif;}")
    x= html.render(stylesheets=[font])
    return x.write_pdf()
