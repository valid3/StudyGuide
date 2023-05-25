# Hey, thank you for using this, I doubt anyone will, but that's okay, sometimes people underappreciate simple softwares
import random
import sys
import os

if sys.platform == 'win32':
    def clear():
        os.system('cls')
else:
    def clear():
        os.system('clear')
# This was made/tested on Mac and Windows. I don't imagine someone studying on a Linux (Lol)

problems = {"What is nine plus ten?": {"ANSWERS": "TWENTY ONE!"},
            "What is inf + inf": {"ANSWERS": "16"}
            }

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
        new_list[index], new_list[index+1] = new_list[index+1], old
        forward.append(''.join(new_list))
        new_list = list(s).copy()
    return forward

def backward_algo(s):
    backward = []
    new_list = list(s).copy()
    for index in range(len(s) - 1, 0, -1):
        old = new_list[index]
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

def main():
    clear()
    global current_Grade
    if len(problems) != 0:
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
            input('Incorrect! Press ANY KEY for next question!')
            current_Grade -= 1
        problems.pop(question)
    else:
        input(f'Congratulations you have scored {(100/problem_Count)*current_Grade}!')
    main()
main()
