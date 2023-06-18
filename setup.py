import tkinter
import json
import customtkinter

customtkinter.set_default_color_theme('green')
QuestionsAnswers = {}
currentQAR = 0

root = customtkinter.CTk()
root.geometry('500x651')
root.title('Study Guide Setup')
root.resizable(False, False)

# SETUP
mainFrame = customtkinter.CTkFrame(master=root, width=470, height=545, border_width=3, border_color='#1C1C1C')
scrollable_frame = customtkinter.CTkScrollableFrame(master=mainFrame, width=428, height=512, scrollbar_button_color='#222222', scrollbar_button_hover_color='#1C1C1C')
controlFrame = customtkinter.CTkFrame(master=root, width=470, height=63, border_width=3, border_color='#1C1C1C')
createQA = customtkinter.CTkButton(master=scrollable_frame, width=426, height=55, fg_color='#222222', hover_color='#1C1C1C', text='+', text_color='#333333', font=("Arial", 65))
dividedButton = customtkinter.CTkSegmentedButton(master=controlFrame, values=['Exit', 'Save', 'Clear'], height=48, corner_radius=8, fg_color='#2B2B2B', unselected_color='#222222', unselected_hover_color='#1C1C1C', selected_hover_color='#1C1C1C', selected_color='#222222')
switch1 = customtkinter.CTkSwitch(master=controlFrame, text='Ask To Clear', button_color='#222222', progress_color='#717171', button_hover_color='#171717')
switch2 = customtkinter.CTkSwitch(master=controlFrame, text='Auto Clear On Save', button_color='#222222', progress_color='#717171', button_hover_color='#171717')

# PLACEMENT
mainFrame.place(x=15, y=15)
scrollable_frame.place(x=10, y=10)
controlFrame.place(x=15, rely=1, y=-77)
dividedButton.place(x=7, y=7)
switch1.select()
switch1.place(x=170, y=20)
switch2.place(x=290, y=20)
createQA.grid(row=0, column=0, pady=1.75)

# FUNCTIONS
def place():
    global currentQAR

    questionAnswerFrame = customtkinter.CTkFrame(master=scrollable_frame, width=426, height=70, fg_color='#222222')
    entryQuestion = customtkinter.CTkEntry(master=questionAnswerFrame, placeholder_text="Question", corner_radius=4, width=355, height=33)
    entryAnswer = customtkinter.CTkEntry(master=questionAnswerFrame, placeholder_text="Answer", corner_radius=4, width=355, height=33)
    deleteButton = customtkinter.CTkButton(master=questionAnswerFrame, width=66, height=66, fg_color='#343638', hover_color='#1C1C1C', text_color='#9E9E9E', corner_radius=4, border_width=2, border_color='#565B5E', font=('Arial', 16))

    entryQuestion.place(x=1.75, y=1.75)
    entryAnswer.place(x=1.75, y=35.75)
    deleteButton.place(x=358, y=1.75)
    deleteButton.configure(text="Delete", command=questionAnswerFrame.destroy)

    currentQAR += 1
    createQA.grid(row=currentQAR, column=0, pady=1.75)
    questionAnswerFrame.grid(row=currentQAR - 1, column=0, pady=1.75)
    QuestionsAnswers[currentQAR - 1] = questionAnswerFrame

def on_closing():
    if tkinter.messagebox.askyesno("Quit", "Are you sure you want to quit? Any unsaved progress will be gone."):
        root.destroy()

def dividedHandler(value):
    global currentQAR
    if value == 'Clear':
        if switch1.get() == 0:
            for k, v in QuestionsAnswers.items():
                v.destroy()
            QuestionsAnswers.clear()
            dividedButton.set('')
            currentQAR = 0
        else:
            result = tkinter.messagebox.askyesno('Confirm', 'Are you sure you want to clear all questions/answers?')
            if result:
                for k, v in QuestionsAnswers.items():
                    v.destroy()
                QuestionsAnswers.clear()
                dividedButton.set('')
                currentQAR = 0
    elif value == 'Clear2':
        for k, v in QuestionsAnswers.items():
            v.destroy()
        QuestionsAnswers.clear()
        dividedButton.set('')
        currentQAR = 0
    elif value == 'Exit':
        on_closing()
        dividedButton.set('')
    elif value == 'Save':
        name = tkinter.simpledialog.askstring('Save', 'What would you like to name the guide?')
        problems = {}
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame):
                question = widget.winfo_children()[0].get()
                answer = widget.winfo_children()[1].get()
                problems[question] = answer
        with open('guides.json', "r") as json_file:
            data = json.load(json_file)
        if name not in data:
            data[name] = problems
            with open('guides.json', 'w') as json_file2:
                json.dump(data, json_file2, indent=4)
            tkinter.messagebox.showinfo('Success', 'Guide save is successful!')
            dividedButton.set('')
            if switch2.get() == 1:
                dividedHandler('Clear2')
        else:
            tkinter.messagebox.showinfo('Error', 'The name you have chosen are already in your guides!')
            dividedButton.set('')

# CONFIGURATION
createQA.configure(command=place)
dividedButton.configure(command=dividedHandler)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
