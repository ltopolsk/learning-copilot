import streamlit as st
from src.app.mongo import DBClient
from src.gpt.gptApi import gptManager
from src.app.auth import run_page
from src.app.misc import render_sidebar, render_pdf
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

def main(user_id, user_email):
    st.session_state.user_id=user_id
    db_client = DBClient(config=st.secrets["mongo"])
    gpt_manager = gptManager(**st.secrets["gpt_api"])
    st.session_state.db = db_client

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

    sidebar, body = st.columns([1, 8])

    render_sidebar(sidebar)

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
    body.markdown('Learning Copilot przyjmuje wykłady w formacie pdf i odczytuje tekst - nie potrafi interpretować obrazów. Ilość wygenerowanych notatek bądź długość quizu zależy od treścliwości stron wczytanego dokumentu.')
    uploaded = body.file_uploader(label='Dodaj plik',on_change=upload_file, type=['pdf'])
    title = body.text_input('Wprowadź tytuł notatek/quizu')

    if title is not None and title != '':
        st.session_state.title = title

    save_result = body.checkbox('Zapisz quiz/notatki na później')
    col1, col2 = body.columns(2)
    clicked_notes = col1.button('Wygeneruj notatki', key='genNotes', disabled=st.session_state.disabled,use_container_width=True)
    clicked_quiz = col2.button('Wygeneruj quiz', key='genQuiz', disabled=st.session_state.disabled,use_container_width=True)

    if uploaded is not None:
        st.session_state.file_uploaded=True
    else:
        st.session_state.file_uploaded=False

    
    if clicked_notes:
        result_holder = body.empty()
        result_holder.markdown("### Tworzenie notatek: 0%")
        result_holder.progress(0)
        def progress(percent):
            with result_holder.container():
                st.markdown(f"### Tworzenie notatek: {percent*100:.0f}%")
                st.progress(percent)
        md_content =gpt_manager.forward(uploaded, 'notes_markdown', callback=progress)
        st.session_state.md_notes = md_content
        st.session_state.file = render_pdf(md_content)
        if save_result:
            db_client.upload_notes(st.session_state.user_id, st.session_state.file, md_content, title)
        switch_page("notes")
    if clicked_quiz:
        result_holder = body.empty()
        result_holder.markdown("### Tworzenie quizu: 0%")
        result_holder.progress(0)
        def progress(percent):
            with result_holder.container():
                st.markdown(f"### Tworzenie quizu: {percent*100:.0f}%")
                st.progress(percent)
    
        st.session_state.quiz = gpt_manager.forward(uploaded, 'quiz', callback=progress)
        if save_result:
            db_client.upload_quiz(st.session_state.user_id, st.session_state.quiz, title)
        switch_page("quiz")


if __name__ == '__main__':
    run_page(main)

