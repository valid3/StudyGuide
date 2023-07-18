# Imports
import customtkinter
import tkinter
import json
import random

class MAIN(customtkinter.CTk):
    def __init__(self):
        super().__init__()  # Import CTK Methods

        # Sets Up Window
        self.title('Study Guide Main')  # Sets Title of Window
        self.geometry('851x550')  # Sets Geometry of Window
        self.resizable(False, False)  # Ensures Window Size can't be changed

        # Variable Setup
        self.problems = {}  # Main guide problems/answers
        self.copy = {}  # Copy of it for when restart button is pressed
        self.submitted = False  # For press submit twice to go onto next question
        self.guides = json.load(open('guides.json', 'r'))  # Loads guides from file
        self.problemCount = None  # For grading system
        self.grade = None  # For grading system
        self.loaded = False  # To tell if a guide is loaded
        self.found = False  # For the misspelling
        self.guideRow = 0  # For loaded guide Frame
        self.loggerRow = 0  # For logger
        self.logs = []  # Logs (Used for clearing)
        self.logWrongVariable = False
        self.logMisspellingsVariable = False

        # Property Variables
        self.BorderColor = '#1C1C1C'  # Border colors of Main Frames
        self.BorderWidth = 3  # Border width of Main Frames

        # Frames Pre-Setup
        self.GuidesMain = customtkinter.CTkFrame(master=self, width=240, height=540, border_width=self.BorderWidth, border_color=self.BorderColor)
        self.InformationMain = customtkinter.CTkFrame(master=self, width=596, height=60, border_width=self.BorderWidth, border_color=self.BorderColor)
        self.AnsweringMain = customtkinter.CTkFrame(master=self, width=596, height=411, border_width=self.BorderWidth, border_color=self.BorderColor)
        self.OptionsMain = customtkinter.CTkFrame(master=self, width=596, height=60, border_width=self.BorderWidth, border_color=self.BorderColor)
        self.GuidesScrollFrame = customtkinter.CTkScrollableFrame(master=self.GuidesMain, width=215, height=528, corner_radius=3, fg_color='#2B2B2B', scrollbar_button_color='#242424', scrollbar_button_hover_color='#333333')
        self.OutputMain = customtkinter.CTkFrame(master=self.AnsweringMain, width=580, height=220, border_width=self.BorderWidth, border_color=self.BorderColor)
        self.OutputScrollFrame = customtkinter.CTkScrollableFrame(master=self.OutputMain, width=555, height=208, corner_radius=3, fg_color='#2B2B2B', scrollbar_button_color='#242424', scrollbar_button_hover_color='#333333')

        # Labels/Entries Pre-Setup
        self.ProblemsLeft = customtkinter.CTkLabel(master=self.InformationMain, width=285, height=54, font=('Arial Baltic', 25), text='Problems: None', anchor='e')
        self.LoadedGuideName = customtkinter.CTkLabel(master=self.InformationMain, width=285, height=54, font=('Arial Baltic', 25), text='Name: None', anchor='w')

        self.QuestionDisplayText = customtkinter.CTkLabel(master=self.AnsweringMain, width=578, height=65, corner_radius=3, fg_color='#242424', font=('Arial', 22), text="Press the 'Load' button on any of the guides on the left. If you see none, run setup_up.py! Enjoy!", wraplength=550)
        self.AnswerEntry = customtkinter.CTkEntry(master=self.AnsweringMain, width=385, height=35, placeholder_text='Answer Here')

        # Buttons Pre-Setup
        self.SubmitButton = customtkinter.CTkButton(master=self.AnsweringMain, width=120, height=45, fg_color='#242424', font=('Arial', 22), text='Submit')
        self.RestartButton = customtkinter.CTkButton(master=self.AnsweringMain, width=120, height=45, fg_color='#242424', font=('Arial', 22), text='Restart')
        self.ClearLogButton = customtkinter.CTkButton(master=self.OptionsMain, width=100, height=49, fg_color='#242424', font=('Arial', 20), text='Clear Log')

        # Switches
        self.LogWrong = customtkinter.CTkSwitch(master=self.OptionsMain, text='Log Wrong', height=49, font=('Arial', 16), button_color='#222222', progress_color='#717171', button_hover_color='#171717')
        self.LogMisspellings = customtkinter.CTkSwitch(master=self.OptionsMain, text='Log Misspellings', height=49, font=('Arial', 16), button_color='#222222', progress_color='#717171', button_hover_color='#171717')

        # Setup
        self.GuidesMain.place(x=5, y=5)
        self.InformationMain.place(x=250, y=5)
        self.AnsweringMain.place(x=250, y=70)
        self.OptionsMain.place(x=250, y=485)
        self.GuidesScrollFrame.place(x=3, y=3)
        self.OutputMain.place(x=8, y=182)
        self.OutputScrollFrame.place(x=3, y=3)

        self.ProblemsLeft.place(x=302, y=3)
        self.LoadedGuideName.place(x=9, y=3)

        self.QuestionDisplayText.place(x=9, y=9)
        self.AnswerEntry.place(x=106, y=90)

        self.SubmitButton.place(x=175, y=131)
        self.RestartButton.place(x=301, y=131)
        self.ClearLogButton.place(x=490, y=6)

        self.SubmitButton.configure(command=self.SubmitAnswer)
        self.ClearLogButton.configure(command=self.ClearLog)
        self.RestartButton.configure(command=self.Restart)

        self.LogWrong.select()
        self.LogMisspellings.select()

        self.LogWrong.place(x=9, y=6)
        self.LogMisspellings.place(x=145, y=6)

        for GuideName, GuideAnswers in self.guides.items():  # Loops through guides folder and making loader for each in GuidesScrollFrame
            # Frame/Labels/Button Pre-Setup
            self.GuideFrame = customtkinter.CTkFrame(master=self.GuidesScrollFrame, width=210, height=61, fg_color='#242424')
            self.GuideNameDisplay = customtkinter.CTkLabel(master=self.GuideFrame, text=f'Guide Name: {GuideName}', width=146, height=26, fg_color='#333333', font=('Arial', 14), corner_radius=5, anchor='w')
            self.GuideProblems = customtkinter.CTkLabel(master=self.GuideFrame, text=f'Problems: {len(GuideAnswers)}', width=146, height=25, fg_color='#333333', font=('Arial', 14), corner_radius=5, anchor='w')
            self.GuideLoadButton = customtkinter.CTkButton(master=self.GuideFrame, width=54, height=54, text='Load', corner_radius=5, font=('Arial', 17), fg_color='#333333')

            # Setup
            self.GuideFrame.grid(row=self.guideRow, column=0, padx=3, pady=3)
            self.GuideNameDisplay.place(x=3, y=3)
            self.GuideProblems.place(x=3, y=33)
            self.GuideLoadButton.place(x=153, y=3)

            self.GuideLoadButton.configure(command=lambda name=GuideName, answers=GuideAnswers, asked=False: self.LoadGuide(name, answers, asked))

            # Makes sure name of Guide isn't long and overlapping past the Background Frame
            if len(GuideName) >= 6:
                self.GuideNameDisplay.configure(text=f'Guide Name: {GuideName[0:5]}..')

            # Finalizing
            self.guideRow += 1

    @staticmethod
    def Process(Answer):  # Enhances Quality of Life by making answering questions less tedious
        if type(Answer) != int:
            aMain = str(Answer.lower())
            special_characters = ',!@#$%^&*()-_=+[{]};:.>/?`~'
            for char in special_characters:
                aMain = aMain.replace(char, '')
            return aMain.split()
        else:
            return [str(Answer)]

    @staticmethod
    def ProcessMisspellings(word):  # Processes all possible misspelling a word can have
        misspellings = []
        new_list = list(word).copy()
        for index in range(len(word) - 1):
            old = new_list[index]
            if new_list[index + 1] != old:
                new_list[index], new_list[index + 1] = new_list[index + 1], old
                misspellings.append(''.join(new_list))
                new_list = list(word).copy()
        return misspellings

    def Finalize(self):  # Finalizes the end of finishing the guide
        self.QuestionDisplayText.configure(text_color='white')
        self.ProblemsLeft.configure(text=f'Problems: {len(self.problems)}')
        self.AnswerEntry.delete(0, 'end')
        self.submitted = False
        self.found = False
        self.loaded = False

    def Exit(self):  # Asks user if they want to exit program
        if tkinter.messagebox.askyesno('Exit', 'Are you sure you want to exit? Your submitted answers will not save for the next time when you open.'):
            self.destroy()

    def ShowMisspelling(self, word, misspelling):  # Logs the Misspelling
        if self.LogMisspellings.get() == 1:
            # Pre-Setup
            LogFrame = customtkinter.CTkFrame(master=self.OutputScrollFrame, width=549, height=46, fg_color='#242424')
            WordLabel = customtkinter.CTkLabel(master=LogFrame, width=100, height=40, font=('Arial', 16), text_color='yellow', text=f'Misspelled Word: {misspelling}')
            CorrectButton = customtkinter.CTkButton(master=LogFrame, width=100, height=40, text='Correct Spelling')

            def SHOW():  # Shows the misspelled word in an info box
                tkinter.messagebox.showinfo('Correct Spelling', f"You spelt the word as '{misspelling}', the correct way of spelling is '{word}'.")

            # Setup
            LogFrame.grid(row=self.loggerRow, column=0, padx=3, pady=3)
            WordLabel.place(x=6, y=3)
            CorrectButton.place(x=442, y=3)
            CorrectButton.configure(command=SHOW)

            # Final
            self.logs.append(LogFrame)
            self.loggerRow += 1

    def ShowRightAnswer(self, question, answer):  # Logs the Misspelling
        if self.LogWrong.get() == 1:
            # Pre-Setup
            LogFrame = customtkinter.CTkFrame(master=self.OutputScrollFrame, width=549, height=46, fg_color='#242424')
            QuestionLabel = customtkinter.CTkLabel(master=LogFrame, width=100, height=40, font=('Arial', 16), text_color='red')
            ShowAnswer = customtkinter.CTkButton(master=LogFrame, width=100, height=40, text='Correct Answer')

            def SHOW():
                tkinter.messagebox.showinfo('Right Answer', f"The answer is '{answer}'")

            # Setup
            LogFrame.grid(row=self.loggerRow, column=0, padx=3, pady=3)
            QuestionLabel.place(x=6, y=3)
            ShowAnswer.place(x=444, y=3)
            ShowAnswer.configure(command=SHOW)

            if len(question) > 40:  # Ensures question doesn't go off screen
                QuestionLabel.configure(text=f'Question: {question[:40]}...')
            else:
                QuestionLabel.configure(text=f'Question: {question}')

            # Final
            self.logs.append(LogFrame)
            self.loggerRow += 1

    def Restart(self):  # Restarts Current Loaded Guide
        if self.loaded:
            if tkinter.messagebox.askyesno('Load', f"Are you sure you want to restart '{self.LoadedGuideName.cget('text')[:4]}'?"):
                self.Finalize()
                self.LoadGuide(self.LoadedGuideName.cget('text')[:4], self.copy, True)
        else:
            tkinter.messagebox.showinfo('Error', 'No guide is loaded.')

    def ClearLog(self):  # Clears All of Logs
        for log in self.logs:
            log.destroy()
        self.logs.clear()
        self.loggerRow = 0

    def SubmitAnswer(self):  # Submit an answer to current question
        if not self.submitted:
            if self.loaded:
                CurrentQuestion = self.QuestionDisplayText.cget('text')
                UserAnswer = self.Process(self.AnswerEntry.get())

                self.submitted = True

                if self.problems[CurrentQuestion]['MISSPELLINGS'] is not None and self.problems[CurrentQuestion]['MISSPELLINGS']:  # Checks if there are any misspellings available
                    for word, misspellings in self.problems[CurrentQuestion]['MISSPELLINGS'].items():
                        for misspelling in misspellings:
                            if misspelling in UserAnswer:
                                self.ShowMisspelling(word, misspelling)
                                self.problems.pop(CurrentQuestion)
                                self.found = True
                                self.QuestionDisplayText.configure(text="Correct! Be sure to check spelling! Press 'Submit' again for the next question!", text_color='yellow')

                if not self.found:  # This check is for if a misspelling was found
                    if all(word in UserAnswer for word in self.problems[CurrentQuestion]['ANSWERS']):  # Checks answer
                        self.QuestionDisplayText.configure(text="Correct! Press 'Submit' again for the next question!", text_color='green')
                        self.problems.pop(CurrentQuestion)
                    else:  # This fires when the user answered incorrectly
                        self.QuestionDisplayText.configure(text=f"Wrong! The answer is {' '.join(self.problems[CurrentQuestion]['ANSWERS'])}! Press 'Submit' again for the next question!", text_color='red')
                        self.ShowRightAnswer(CurrentQuestion, ' '.join(self.problems[CurrentQuestion]['ANSWERS']))
                        self.problems.pop(CurrentQuestion)
                        self.grade -= 1
            else:  # If no guide is loaded, it tells user
                tkinter.messagebox.showinfo('Error', 'No guide is loaded.')
        else:  # Fires when it is ready for next click on submit button
            if self.problems:  # If there are problems, give next problem
                self.QuestionDisplayText.configure(text_color='white')
                self.AnswerEntry.delete(0, 'end')
                self.submitted = False
                self.found = False
                self.GiveProblem()
            else:  # If this fires, this means there are no more problems left
                Result = tkinter.messagebox.askyesno('Results', f'You scored {(100/self.problemCount)*self.grade}% ({self.grade}/{self.problemCount}). Would you like to restart?')
                if Result:  # If user presses Yes to restart, this fires
                    self.Finalize()
                    self.LoadGuide(self.LoadedGuideName.cget('text')[:4], self.copy, True)
                else:  # If they don't press Yes to restart, it'll set Name back to None and everything back to normal
                    self.LoadedGuideName.configure(text='Name: None')
                    self.QuestionDisplayText.configure(text="Press the 'Load' button on any of the guides on the left. If you see none, run setup_up.py! Enjoy!")
                    self.Finalize()

    def CanHaveMisspelling(self):  # Sees if a word can be used for ProcessMisspellings
        for Question, Answer in self.problems.items():
            for Word in Answer['ANSWERS']:
                if len(Word) >= 4:
                    return True
        return False

    def GiveProblem(self):  # Gives randomized problem to user
        self.ProblemsLeft.configure(text=f'Problems: {len(self.problems)}')
        self.QuestionDisplayText.configure(text=random.choice(list(self.problems.keys())))

    def LoadGuide(self, name, answers, asked):  # Loads a Guide
        def LOAD():  # Quality of Life, makes it so if you press Yes on restart button, you won't need to press another button
            if not self.loaded:  # If guide not already loaded
                if self.copy:  # Made for handling restarts, checks to see if copy exists, and if it does that's program way of knowing a restart has been initiated
                    self.problems = self.copy.copy()

                self.LoadedGuideName.configure(text=f'Name: {name}')  # Changes loaded guide name to name of the guide that was loaded
                self.problems = answers.copy()  # Shallow copies input (answers) into self.problems
                self.copy = self.problems.copy()

                for Question, Answer in self.problems.copy().items():
                    self.problems[Question] = {'ANSWERS': Answer}
                    self.problems[Question]['ANSWERS'] = self.Process(self.problems[Question]['ANSWERS'])
                    self.problems[Question]['MISSPELLINGS'] = {}

                if self.CanHaveMisspelling():
                    for QuestionMIS, AnswerMIS in self.problems.items():
                        for Word in AnswerMIS['ANSWERS']:
                            if len(Word) >= 4:
                                self.problems[QuestionMIS]['MISSPELLINGS'][Word] = self.ProcessMisspellings(Word)
                else:
                    self.problems['MISSPELLINGS'] = None

                self.loaded = True
                self.grade = len(self.problems)
                self.problemCount = len(self.problems)
                self.GiveProblem()

        if asked:
            LOAD()
        else:
            if tkinter.messagebox.askyesno('Load', f"Are you sure you want to load '{name}'? Any other guides will stop running."):
                LOAD()

APP = MAIN()
APP.AnswerEntry.bind('<Return>', lambda event: APP.SubmitAnswer())
APP.protocol('WM_DELETE_WINDOW', APP.Exit)

APP.mainloop()

# ADD
# - Misspelling Check/Wrong Answer to Right Answer INTERFACE SCROLL FRAME
# - Use Enter key to submit