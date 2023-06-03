# Hey, thank you for using this, I doubt anyone will, but that's okay, sometimes the least known software you find is the best
import random
import json
import sys
import os

if sys.platform == 'win32':
    def clear():
        os.system('cls')
else:
    def clear():
        os.system('clear')
# This was made/tested on Mac and Windows. I don't imagine someone studying on a Linux (Lol)

problems = {}
restartProblems = {}
wrong = {}

with open('guides.json', "r") as json_file:
    data = json.load(json_file)
if data:
    def p():
        clear()
        print('Type name of guide below to study!\n')
        for name in data.keys():
            print(name)
        nameInput = input('\nName Here: ')
        if nameInput in data:
            global problems
            for k, v in data[nameInput].items():
                problems[k] = {"ANSWERS" : v}
        else:
            print('No guide found! Please correct spelling, it is case sensitive!')
            input('Press ENTER if you understand.')
            p()
    p()
else:
    print('You have no guides setup!')
    sys.exit()

# FORMAT
# {Question: {Answer: [Answer] }, {Misspellings: {word: [misspellings]} }}
problem_Count, current_Grade = len(problems), len(problems)

def algo(answer):
    aMain = str(answer.lower())
    special_characters = '!@#$%^&*()-_=+[{]};:.>/?`~'
    for char in special_characters:
        aMain = aMain.replace(char, '')
    return aMain.split()

def forward_algo(s):
    forward = []
    new_list = list(s).copy()
    for index in range(len(s) - 1):
        old = new_list[index]
        if new_list[index+1] != old:
            new_list[index], new_list[index+1] = new_list[index+1], old
            forward.append(''.join(new_list))
            new_list = list(s).copy()
    return forward

def backward_algo(s):
    backward = []
    new_list = list(s).copy()
    for index in range(len(s) - 1, 0, -1):
        old = new_list[index]
        if new_list[index - 1] != old:
            new_list[index], new_list[index - 1] = new_list[index - 1], old
            backward.append(''.join(new_list))
            new_list = list(s).copy()
    return backward

for q, a in problems.items():
    problems[q]["ANSWERS"] = algo(problems[q]["ANSWERS"])
    problems[q]["MISSPELLINGS"] = {}

for ques, ans in problems.items():
    for element in ans["ANSWERS"]:
        if not type(element) is int:
            if len(element) >= 4:
                problems[ques]["MISSPELLINGS"][element] = {"forwards": forward_algo(element), "backwards": backward_algo(element)}

restartProblems = problems.copy()

def main():
    clear()
    global current_Grade
    global problems
    if problems:
        print(f'Problems Left: {len(problems)}\n')
        question, answer = random.choice(list(problems.items()))
        user_answer = input(f'{question}\n\n')

        for word, misspellings in answer["MISSPELLINGS"].items():
            if word not in misspellings:
                for user_word in algo(user_answer):
                    if user_word in misspellings['forwards'] or user_word in misspellings['backwards']:
                        input(f"Misspelling Detected! The misspelled word is {word}! You typed in {user_word}!")

        if all(x in algo(user_answer) for x in answer["ANSWERS"]):
            input('Correct! Press ANY KEY for next question!')
        else:
            input(f'Incorrect! The answer was ({" ".join(answer["ANSWERS"])}) Press ANY KEY for next question!')
            wrong[question] = {"user_Answer": user_answer, "rightAnswer" : " ".join(answer['ANSWERS'])}
            current_Grade -= 1
        problems.pop(question)
    else:
        print(f'Congratulations you have scored {(100/problem_Count)*current_Grade}! ({current_Grade}/{problem_Count})\n')
        if wrong:
            for questionWrong, properties in wrong.items():
                print(f'Question: {questionWrong} | Your Answer: {properties["user_Answer"]} | Right Answer: {properties["rightAnswer"]}')
            print('\n')

        input('Press ENTER if you would like to restart on this guide, or stop and setup for a different guide.')
        problems = restartProblems.copy()
    main()
main()
