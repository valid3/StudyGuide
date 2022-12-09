# READ

# Use key words as value of dictionary key. For example, setting value to sky can make you type in "The big blue sky!" and be considered right!

import os
try:
    import colorama
except:
    os.system('pip install colorama')
import random
import colorama

problems = {
    "What is significant digits of 33.831":"33.8",
    "What law states that the velocity of an object does not change unless the object is acted upon by an external force?":"first law motion",
}

spec_chars = ["!", ".", "?", ",", ";", ":", "'", "/"]
# REMOVING SPECIAL CHARACTERS
for spec in spec_chars:
    for question, answer in problems.items():
        if spec in answer:
            problems[question] = answer.replace(spec, "").lower()
# TURNING ALL ANSWERS INTO LIST
for question, answer in problems.items():
    problems[question] = answer.split()
grade_display = len(problems)
max_display = len(problems)

def give_question():
    global grade_display
    global max_display
    if len(problems) == 0:
        os.system("clear")
        print(
            f"Congratulations You Scored {grade_display}/{max_display}\n\n%: {(100/max_display)*grade_display}%"
        )
    else:
        os.system("clear")
        question, answer = random.choice(list(problems.items()))
        finalAnswer = input(
            f"\n\n{colorama.Fore.GREEN}{question}{colorama.Style.RESET_ALL}\n\n{colorama.Fore.BLUE}Answer:{colorama.Style.RESET_ALL} "
        )
        for spec in spec_chars:
            for char in finalAnswer:
                if spec in char:
                    finalAnswer = finalAnswer.replace(spec, "")
        finalAnswer = list(str(finalAnswer.split()).lower())
        is_right = all(x in finalAnswer for x in str(answer).lower())
        if is_right == True:
            print("\n\nCorrect Answer!")
            problems.pop(question)
        else:
            print(f"\n\nIncorrect Answers\n\nCorrect Answer: {answer}")
            problems.pop(question)
            grade_display -= 1
        input("Press ENTER For Next Question: ")
        give_question()

give_question()
