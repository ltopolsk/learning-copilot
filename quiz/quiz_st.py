### File that creates the quiz
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_extras.switch_page_button import switch_page
from read import read_questions

# Define quiz questions and answers
questions = read_questions("quiz.json")

# questions = [
#     {
#         "question": "What is the capital of France?",
#         "options": ["Berlin", "Madrid", "Paris", "Rome"],
#         "correct_answer": "Paris",
#     },
#     {
#         "question": "Which planet is known as the Red Planet?",
#         "options": ["Mars", "Jupiter", "Venus", "Saturn"],
#         "correct_answer": "Mars",
#     },
#     # Add more questions as needed
# ]

# Initialize session state
if 'score' not in st.session_state:
    st.session_state['score'] = 0

if 'user_answer' not in st.session_state:
    st.session_state['user_answer'] = [0] * len(questions)
    
if 'disabled' not in st.session_state:
    st.session_state['disabled'] = False

if 'correct' not in st.session_state:
    st.session_state['correct'] = [0] * len(questions)

# Function to display and process the quiz
def display_quiz():
    global user_answer
    for i, q in enumerate(questions, start=1):
        st.subheader(f"Pytanie {i}: {q['question']}")
        # selected_option_index = st.radio("Choose an option:", q["options"], index=None)

        st.session_state['user_answer'][i-1] = st.radio("Wybierz poprawną odpowiedź:", q["options"], index=None)
        print(i)
        print(st.session_state['user_answer'])

        # if user_answer == q["correct_answer"]:
        #     st.session_state['score'] += 1
            # score += 1
# Function to display and process the quiz
def display_answers():
    st.markdown(
        """
        ## Answers
        """
    )
    for i, q in enumerate(questions, start=1):
        answer = ""
        st.subheader(f"Pytanie {i}: {q['question']}")
        if st.session_state['correct'][i-1] == 1:
            answer = "Brawo, to poprawna odpowiedź" +  '\u2714'
        if st.session_state['correct'][i-1] == -1:
            answer = "Brak odpowiedzi"
        if st.session_state['correct'][i-1] == 0:
            answer = "Twoja odpowiedź jest błędna   " +  '\u2716'
        st.markdown(
        """
            {} \n
            Poprawna odpowiedź to: {} \n
            Twoja odpowiedź: {}
        """.format(answer, q["correct_answer"], st.session_state['user_answer'][i-1])
    )

# Streamlit app
st.title("GPT-Based Quiz App")

# Display the quiz
display_quiz()

if st.button("Submit"):
    # Redirect to the "Results" page
    for i, q in enumerate(questions, start=1):
        if st.session_state['user_answer'][i-1] == q["correct_answer"]:
            st.session_state['score'] += 1
            st.session_state['correct'][i-1] = 1
        if st.session_state['user_answer'][i-1] != q["correct_answer"]:
            st.session_state['correct'][i-1] = 0
        if st.session_state['user_answer'][i-1] == None:
            st.session_state['correct'][i-1] = -1
    

    st.markdown(
        """
        ## Wyniki
        Twój rezultat: {}/{}
        """.format(st.session_state['score'], len(questions))
    )
    # st.switch_page('pages/quiz_2.py')
    display_answers()
    st.session_state['score'] = 0
    st.session_state['user_answer'] = [None] * len(questions);

if st.button("Reload"):
    st.session_state['score'] = 0
    st.session_state['user_answer'] = [None] * len(questions);
    st.rerun()
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

