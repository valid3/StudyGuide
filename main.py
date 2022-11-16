import random
import os

# READ

# Use key words as value of dictionary key. For example, setting value to sky can make you type in "The big blue sky!" and be considered right!

problems = {
    "What is the blue thing above you outside called?":"sky",
    "What has 8 legs and red triangle on back?":"black widow spider",
}
spec_chars = ['!','.','?',',',';',':',"'",'/']
# REMOVING SPECIAL CHARS
for spec in spec_chars:
    for question, answer in problems.items():
        if spec in answer:
            problems[question] = answer.replace(spec, '').lower()
# TURNING ALL ANSWERS INTO LIST
for question, answer in problems.items():
    problems[question] = answer.split()
grade_display = len(problems)
max_display = len(problems)
def give_question():
    global grade_display; global max_display
    if len(problems) == 0:
        os.system('clear')
        print(f'Congratulations You Scored {max_display}/{grade_display}\n\n%: {(100/max_display)*grade_display}%')
    else:
        os.system('clear')
        question, answer = random.choice(list(problems.items()))
        print(f'\n\n{question}\n\n')
        finalAnswer = (str(input('Answer: ')))
        for spec in spec_chars:
            for char in finalAnswer:
                if spec in char:
                    finalAnswer = finalAnswer.replace(spec, '').lower()
        finalAnswer = finalAnswer.split()
        is_right = all(x in finalAnswer for x in answer)
        if is_right == True:
            print('\n\nCorrect Answer!')
            problems.pop(question)
        else:
            print(f'\n\nIncorrect Answers\n\nCorrect Answer: {answer}')
            problems.pop(question)
            grade_display -= 1
        input('Press ENTER For Next Question: ')  
        give_question()
give_question()
