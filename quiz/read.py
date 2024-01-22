### File that reads the questions from the file / chat-gpt format, to be improved yet
import json

def read_questions(file_path):
    with open(file_path, "r") as file:
        data_dict = json.load(file)

    questions = []
    # if(len(data_dict['question']) == len(data_dict['answers'] == data_dict['correct'])):
    for i in range(len(data_dict['question'])): 
        answers = []
        for q in data_dict['answers'][i]:
            answers.append(q)
            if(data_dict['correct'][i]==q):
                print("Match for question ", i)
        questions.append({'question': data_dict['question'][i], 'options': answers, 'correct_answer': data_dict['correct'][i]})
    return questions

questions = read_questions("./quiz.json")
for i, q in enumerate(questions, start=1):
    print(i, ". ", q['correct_answer'])

print(len(questions))