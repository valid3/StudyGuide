from os import system,path
def clear():
    if path.sep == '\\':
        system('cls')
    else:
        system('clear')
try:
    from colorama import Fore
except:
    system('pip install colorama')
from secrets import choice
from colorama import Fore,Style

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
# MAIN
def give_question():
    global grade_display
    global max_display
    if len(problems) == 0:
        clear()
        print(
            f"Congratulations You Scored {Fore.GREEN}{grade_display}/{max_display}{Style.RESET_ALL}\n\n {str((100/max_display)*grade_display)[:5]}%"
        )
    else:
        clear()
        question, answer = choice(list(problems.items()))
        finalAnswer = input(
            f"Problems Left: {len(problems)}\n\n{Fore.GREEN}{question}{Style.RESET_ALL}\n\n{Fore.BLUE}Answer:{Style.RESET_ALL} "
        )
        for spec in spec_chars:
            for char in finalAnswer:
                if spec in char:
                    finalAnswer = finalAnswer.replace(spec, "")
        finalAnswer = list(str(finalAnswer.split()).lower())
        is_right = all(x in finalAnswer for x in str(answer).lower())
        if is_right:
            print(f"\n{Fore.GREEN}Correct Answer!{Style.RESET_ALL}")
            problems.pop(question)
        else:
            print(f"\n\n{Fore.RED}Incorrect Answers{Style.RESET_ALL}\n\nCorrect Answer: {answer}")
            problems.pop(question)
            grade_display -= 1
        input("Press ENTER For Next Question: ")
        give_question()
give_question()
