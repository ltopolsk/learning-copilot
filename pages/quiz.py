import streamlit as st
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

def parse_quiz(data_dict):
    questions = []
    # if(len(data_dict['question']) == len(data_dict['answers'] == data_dict['correct'])):
    # print(data_dict)
    for i in range(len(data_dict['question'])): 
        answers = []
        for q in data_dict['answers'][i]:
            answers.append(q)
            # if(data_dict['correct'][i]==q):
                # print("Match for question ", i)
        questions.append({'question': data_dict['question'][i], 'options': answers, 'correct_answer': data_dict['correct'][i]})
    return questions

sidebar, body = st.columns([1, 10])

home_button = sidebar.button('HOME', key='homeButton', use_container_width=True)

if home_button:
    switch_page("st")

body.markdown('<h1>Learning Copilot</h1>', unsafe_allow_html=True)

# Define quiz questions and answers
questions = parse_quiz(st.session_state.get('quiz', None))

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
        body.subheader(f"Pytanie {i}: {q['question']}")
        # selected_option_index = st.radio("Choose an option:", q["options"], index=None)

        st.session_state['user_answer'][i-1] = body.radio("Wybierz poprawną odpowiedź:", q["options"], index=None)
        # print(i)
        # print(st.session_state['user_answer'])

        # if user_answer == q["correct_answer"]:
        #     st.session_state['score'] += 1
            # score += 1
# Function to display and process the quiz
def display_answers():
    body.markdown(
        """
        ## Answers
        """
    )
    for i, q in enumerate(questions, start=1):
        answer = ""
        body.subheader(f"Pytanie {i}: {q['question']}")
        if st.session_state['correct'][i-1] == 1:
            answer = "Brawo, to poprawna odpowiedź" +  '\u2714'
        if st.session_state['correct'][i-1] == -1:
            answer = "Brak odpowiedzi"
        if st.session_state['correct'][i-1] == 0:
            answer = "Twoja odpowiedź jest błędna   " +  '\u2716'
        body.markdown(
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
    st.session_state['user_answer'] = [None] * len(questions);

if body.button("Reload"):
    st.session_state['score'] = 0
    st.session_state['user_answer'] = [None] * len(questions);
    st.rerun()
