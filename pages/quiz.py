import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.app.auth import run_page
from src.app.misc import render_sidebar

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

def parse_quiz(data_dict):
    questions = []
    for i in range(len(data_dict['question'])): 
        answers = []
        for q in data_dict['answers'][i]:
            answers.append(q)
        questions.append({'question': data_dict['question'][i], 'options': answers, 'correct_answer': data_dict['correct'][i]})
    return questions

def quiz_page(user_id, user_email):
    sidebar, body = st.columns([1, 8])

    render_sidebar(sidebar)

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)

    # Define quiz questions and answers
    questions = parse_quiz(st.session_state.quiz)

    st.session_state['score'] = 0

    st.session_state['user_answer'] = [0] * len(questions)
        
    st.session_state['disabled'] = False

    st.session_state['correct'] = [0] * len(questions)

    # Function to display and process the quiz
    def display_quiz():
        global user_answer
        for i, q in enumerate(questions, start=1):
            body.subheader(f"Pytanie {i}: {q['question']}")

            st.session_state['user_answer'][i-1] = body.radio("Wybierz poprawną odpowiedź:", q["options"], index=None)

    # Function to display and process the quiz
    def display_answers():
        background_color = "#add8e6"
        body.markdown(
            """
            ## Answers
            """
        )
        for i, q in enumerate(questions, start=1):
            answer = ""
            body.subheader(f"Pytanie {i}: {q['question']}")
            if st.session_state['correct'][i-1] == 1:
                answer = "Brawo, Twoja odpowiedź jest poprawna   " +  '\u2714'
                background_color = "#90EE90"
            if st.session_state['correct'][i-1] == -1:
                answer = "Brak odpowiedzi"
                background_color = "#D3D3D3"
            if st.session_state['correct'][i-1] == 0:
                answer = "Twoja odpowiedź jest błędna   " +  '\u2716'
                background_color = "#FFA07A"
            corr = q["correct_answer"]
            user_an = st.session_state['user_answer'][i-1]
            colored_box = f"""
            <div style="
            background-color: {background_color};
            padding: 20px;
            border-radius: 10px;
            text-align: left;">
                <p style="color: white;">{answer}</p>
                <p style="color: white;">Poprawna odpowiedź to: {corr}</p>
                <p style="color: white;">Twoja odpowiedź: {user_an}</p>
            </div>"""
            body.markdown(colored_box, unsafe_allow_html=True)

    # Display the quiz
    display_quiz()

    if body.button("Submit"):
        # Redirect to the "Results" page
        for i, q in enumerate(questions, start=1):
            if st.session_state['user_answer'][i-1] == q["correct_answer"]:
                st.session_state['score'] += 1
                st.session_state['correct'][i-1] = 1
            if st.session_state['user_answer'][i-1] != q["correct_answer"]:
                st.session_state['correct'][i-1] = 0
            if st.session_state['user_answer'][i-1] == None:
                st.session_state['correct'][i-1] = -1
        

        body.markdown(
            """
            ## Wyniki
            Twój rezultat: {}/{}
            """.format(st.session_state['score'], len(questions))
        )
        display_answers()
        st.session_state['score'] = 0
        st.session_state['user_answer'] = [None] * len(questions)

    if body.button("Reload"):
        st.session_state['score'] = 0
        st.session_state['user_answer'] = [None] * len(questions)
        st.rerun()

run_page(quiz_page)