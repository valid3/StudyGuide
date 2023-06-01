# PLEASE READ
# Technically, this program isn't need but will make study guide writing easier and faster
# Enjoy

import json
import sys
import os

if sys.platform == 'win32':
    def clr():
        os.system('cls')
else:
    def clear():
        os.system('clear')


class main:
    def __init__(self):
        self.problems = {}

    def add(self, question, answer):
        self.problems[question] = answer

    def exit(self):
        name = input("Name of Guide (Type 'cancel' then press ENTER to cancel this action): ")
        if name.lower() != 'cancel':
            with open('guides.json', "r") as json_file:
                data = json.load(json_file)
            if name not in data:
                data[name] = self.problems
                with open('guides.json', 'w') as json_file2:
                    json.dump(data, json_file2, indent=4)
            else:
                print('Guide name already in file! Please try this action again using a different name!')

    def ask(self):
        clr()
        question = input('Question: ')
        answer = input('Answer: ')
        clr()
        print(f'Question: {question}\nAnswer: {answer}')
        YN = input('\nWould you like to insert this into the guide? (Y/N): ')
        if YN.lower() == 'y':
            self.add(question, answer)
        elif YN.lower() == 'n':
            self.ask()

    def view(self):
        for q, a in self.problems.items():
            print(f'Question: {q}\nAnswer: {a}\n\n')

    def delete(self):
        with open('guides.json', "r") as json_file:
            data = json.load(json_file)
        for name in data.keys():
            print(name)
        to_delete = input("Type in the name of the guide you would like to delete: ")
        YN = input(f'\nAre you sure you want to delete "{to_delete}"? (Y/N): ')
        if YN.lower() == 'y':
            data.pop(to_delete)
            with open('guides.json', 'w') as json_file2:
                json.dump(data, json_file2, indent=4)
        elif YN.lower() == 'n':
            self.ask()

    def choice(self):
        return int(input(
            "Would you like to exit and save, write more questions, etc? Type...\n(1) Exit/Save\n(2) Write\n(3) View\n(4) Delete A Guide\n\nAction: "))

try:
    setup = main()

    actions = {
        "1": setup.exit,
        "2": setup.ask,
        "3": setup.view,
        "4": setup.delete
    }

    def m():
        clr()
        try:
            action = setup.choice()
            actions[str(action)]()
        except (ValueError, KeyError):
            print("Invalid Action! Type 1, 2, 3, or 4 for the corresponding action above!")
        input("Press ENTER to continue: ")
        m()

    m()
except Exception as e:
    with open('guides.json', "r") as backup:
        data = json.load(backup)
    data["BACKUP_TRUE"] = setup.problems
    with open('guides.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("AN UNEXPECTED ERROR HAS OCCURRED, A BACKUP HAS BEEN MADE IN GUIDES.JSON IN THE GUIDE NAMED 'BACKUP_TRUE'")
    print(f"Error: {e}")
