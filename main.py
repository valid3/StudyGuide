from os import system,path
def clear():
    if path.sep == '\\':
        system('cls')
    else:
        system('clear')
try:
    import colorama
except:
    system('pip install colorama')
import random
import colorama

problems = {
    "What law states that the velocity of an object does not change unless the object is acted upon by an external force?":"first law motion",
    "What is energy associated with the position of an object and the forces acting upon it?":"potential energy",
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
        clear()
        print(
            f"Congratulations You Scored {colorama.Fore.GREEN}{grade_display}/{max_display}{colorama.Style.RESET_ALL}\n\n {str((100/max_display)*grade_display)[:5]}%"
        )
    else:
        clear()
        question, answer = random.choice(list(problems.items()))
        finalAnswer = input(
            f"Problems Left: {len(problems)}\n\n{colorama.Fore.GREEN}{question}{colorama.Style.RESET_ALL}\n\n{colorama.Fore.BLUE}Answer:{colorama.Style.RESET_ALL} "
        )
        for spec in spec_chars:
            for char in finalAnswer:
                if spec in char:
                    finalAnswer = finalAnswer.replace(spec, "")
        finalAnswer = list(str(finalAnswer.split()).lower())
        is_right = all(x in finalAnswer for x in str(answer).lower())
        if is_right:
            print(f"\n{colorama.Fore.GREEN}Correct Answer!{colorama.Style.RESET_ALL}")
            problems.pop(question)
        else:
            print(f"\n\n{colorama.Fore.RED}Incorrect Answers{colorama.Style.RESET_ALL}\n\nCorrect Answer: {answer}")
            problems.pop(question)
            grade_display -= 1
        input("Press ENTER For Next Question: ")
        give_question()
give_question()
