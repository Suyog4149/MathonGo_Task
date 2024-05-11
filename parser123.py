import re
import json

with open('Task.txt', 'r') as file:
    text = file.read()
cleaned_text = re.sub(r'\\section\*{([^}]*)}', r'\1', text)
questions = re.split(r'Question ID: (\d+)', cleaned_text)[1:]
json_objects = []
question_number = 1
for i in range(0, len(questions), 2):
    question_id = questions[i]
    question_text = questions[i+1].split('(A)')[0].strip()
    options = re.findall(r'\(A\) (.+?)\(B\)', questions[i+1], re.DOTALL)[0].strip().split('\n')
    options = [{'optionNumber': chr(ord('A') + j), 'optionText': option.strip(), 'isCorrect': False} 
               for j, option in enumerate(options)]
    correct_option = re.search(r'Answer \((.)\)', questions[i+1]).group(1)
    for option in options:
        if option['optionNumber'] == correct_option:
            option['isCorrect'] = True
    solution_text = re.search(r'Sol\.([\s\S]*?)(?:Question ID:|$)', questions[i+1]).group(1).strip()

    question_obj = {
        'questionNumber': question_number,
        'questionId': int(question_id),
        'questionText': question_text,
        'options': options,
        'solutionText': solution_text
    }

    json_objects.append(question_obj)
    question_number += 1
json_data = json.dumps(json_objects, indent=2)
with open('questions.json', 'w') as json_file:
    json_file.write(json_data)
