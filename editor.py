# Imports
import customtkinter
import tkinter
import json


class MAIN(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Sets up window
        self.title("Editor")  # Sets title of window
        self.geometry("701x550")  # Sets geometry of window
        self.resizable(False, False)  # Ensures window can't be resized

        # Variable Setup
        self.QuestionAnswers = []  # Stores ui QA in this
        self.ExistingGuides = []
        self.EditingGuide = {
            "original": {},
            "name": "",
        }  # Handles saving original stuff
        self.editing = (
            False  # Not 100% needed but is used to tell if a guide is being edited
        )
        self.guides = json.load(open("guides.json", "r"))  # Loads guides from file
        self.EditGuideRow = 0  # For edit guide scrollable
        self.QARow = 0  # For QA scrollable

        # Property Variables
        self.BorderColor = "#1C1C1C"  # Border colors of Main Frames
        self.BorderWidth = 3  # Border width of Main Frames

        # Frame Pre-Setup
        self.GuidesFrame = customtkinter.CTkFrame(
            master=self,
            width=270,
            height=540,
            border_width=self.BorderWidth,
            border_color=self.BorderColor,
        )
        self.EditingFrame = customtkinter.CTkFrame(
            master=self,
            width=416,
            height=476,
            border_width=self.BorderWidth,
            border_color=self.BorderColor,
        )
        self.OptionsMain = customtkinter.CTkFrame(
            master=self,
            width=416,
            height=60,
            border_width=self.BorderWidth,
            border_color=self.BorderColor,
        )

        self.ScrollableGuideFrame = customtkinter.CTkScrollableFrame(
            master=self.GuidesFrame,
            width=245,
            height=528,
            corner_radius=3,
            fg_color="#2B2B2B",
            scrollbar_button_color="#242424",
            scrollbar_button_hover_color="#333333",
        )
        self.ScrollableEditorFrame = customtkinter.CTkScrollableFrame(
            master=self.EditingFrame,
            width=391,
            height=460,
            corner_radius=3,
            fg_color="#2B2B2B",
            scrollbar_button_color="#242424",
            scrollbar_button_hover_color="#333333",
        )

        # Buttons Pre-Setup
        self.CreateQA = customtkinter.CTkButton(
            master=self.ScrollableEditorFrame,
            width=386,
            height=55,
            fg_color="#222222",
            text="+",
            text_color="#333333",
            font=("Arial", 65),
        )
        self.SaveButton = customtkinter.CTkButton(
            master=self.OptionsMain,
            width=75,
            height=44,
            fg_color="#222222",
            text="Save",
            font=("Arial", 22),
        )
        self.ClearButton = customtkinter.CTkButton(
            master=self.OptionsMain,
            width=75,
            height=44,
            fg_color="#222222",
            text="Clear",
            font=("Arial", 22),
        )
        self.DeleteButton = customtkinter.CTkButton(
            master=self.OptionsMain,
            width=75,
            height=44,
            fg_color="#222222",
            text="Delete",
            font=("Arial", 22),
        )

        # Setup
        self.GuidesFrame.place(x=5, y=5)
        self.EditingFrame.place(x=280, y=5)
        self.OptionsMain.place(x=280, y=485)

        self.ScrollableGuideFrame.place(x=3, y=3)
        self.ScrollableEditorFrame.place(x=3, y=3)

        self.CreateQA.grid(row=0, column=0, padx=3, pady=3)
        self.SaveButton.place(x=8, y=8)
        self.ClearButton.place(x=87, y=8)
        self.DeleteButton.place(x=166, y=8)

        self.CreateQA.configure(command=lambda: self.Create(False, False, False))
        self.SaveButton.configure(command=self.Save)
        self.ClearButton.configure(command=lambda: self.ClearEditor(False))
        self.DeleteButton.configure(command=self.DeleteGuide)

        self.LoadExistingGuides()

    def QOACreate(
        self,
    ):  # Quality of Life function where if user presses enter in answer, it'll create a new question/answer
        self.Create(False, False, True).focus()

    def ClearEditor(self, edit):  # Clears Editor
        def m():
            for qa in self.QuestionAnswers:
                qa.destroy()

            self.QuestionAnswers.clear()
            self.QARow = 0

        if edit:
            m()
        else:
            if tkinter.messagebox.askyesno("Clear", f"Are you sure you want to clear?"):
                m()

    def LoadExistingGuides(self):  # A refresh for existing guides
        self.SaveButton.configure(text_color="white")

        for ExistingGuide in self.ExistingGuides:
            ExistingGuide.destroy()

        for (
            GuideName,
            GuideAnswers,
        ) in (
            self.guides.items()
        ):  # Loops through guides folder and making edit for each in GuidesScrollFrame
            # Frame/Labels/Button Pre-Setup
            GuideFrame = customtkinter.CTkFrame(
                master=self.ScrollableGuideFrame,
                width=240,
                height=61,
                fg_color="#242424",
            )
            GuideNameDisplay = customtkinter.CTkLabel(
                master=GuideFrame,
                text=f"Guide Name: {GuideName}",
                width=176,
                height=26,
                fg_color="#333333",
                font=("Arial", 14),
                corner_radius=5,
                anchor="w",
            )
            GuideProblems = customtkinter.CTkLabel(
                master=GuideFrame,
                text=f"Problems: {len(GuideAnswers)}",
                width=176,
                height=25,
                fg_color="#333333",
                font=("Arial", 14),
                corner_radius=5,
                anchor="w",
            )
            GuideEditButton = customtkinter.CTkButton(
                master=GuideFrame,
                width=54,
                height=54,
                text="Edit",
                corner_radius=5,
                font=("Arial", 17),
                fg_color="#333333",
            )

            # Setup
            GuideFrame.grid(row=self.EditGuideRow, column=0, padx=3, pady=3)
            GuideNameDisplay.place(x=3, y=3)
            GuideProblems.place(x=3, y=33)
            GuideEditButton.place(x=183, y=3)

            GuideEditButton.configure(
                command=lambda name=GuideName, frame=GuideFrame: self.Edit(name, frame)
            )

            # Makes sure name of Guide isn't long and overlapping past the Background Frame
            if len(GuideName) >= 9:
                GuideNameDisplay.configure(text=f"Guide Name: {GuideName[0:8]}..")

            # Finalizing
            self.EditGuideRow += 1
            self.ExistingGuides.append(GuideFrame)

    def Edit(self, name, mainframe):  # Edit Handler for editing existing guide
        print(name, self.EditingGuide["name"], self.editing)

        def m():
            if not self.editing:
                if tkinter.messagebox.askyesno(
                    "Confirm",
                    f"Are you sure you want to edit '{name}'? Any questions and answers in the editor will be removed and replaced.",
                ):

                    if self.QuestionAnswers:
                        for QABox in self.QuestionAnswers:
                            self.EditingGuide["original"][
                                QABox.winfo_children()[0].get()
                            ] = QABox.winfo_children()[1].get()

                    self.editing = True
                    self.EditingGuide["name"] = name
                    self.SaveButton.configure(text_color="green")
                    self.ClearEditor(True)

                    mainframe.winfo_children()[2].configure(
                        text="Cancel", font=("Arial", 13)
                    )
                    for Question, Answer in self.guides[name].items():
                        self.Create(Question, Answer, False)
            else:
                if tkinter.messagebox.askyesno(
                    "Cancel",
                    f"Are you sure you want to cancel editing? You will lose unsaved progress.",
                ):
                    self.ClearEditor(True)
                    mainframe.winfo_children()[2].configure(
                        text="Edit", font=("Arial", 17)
                    )
                    if self.EditingGuide["original"]:
                        for Question, Answer in self.EditingGuide["original"].items():
                            self.Create(Question, Answer, False)

                    self.EditingGuide["original"] = {}
                    self.EditingGuide["name"] = ""
                    self.SaveButton.configure(text_color="white")
                    self.editing = False

        if name == self.EditingGuide["name"] or self.EditingGuide["name"] == "":
            m()
        else:
            tkinter.messagebox.showinfo(
                "Error", "You must cancel the current edit to edit another guide."
            )

    def Save(self):  # Saves a guide, this works for both existing and making new guide
        problems = {}

        for widget in self.ScrollableEditorFrame.winfo_children():
            # Adds all the questions and answers from editor into a dictionary
            if isinstance(widget, customtkinter.CTkFrame):  # Checks if its instance Frame
                problems[widget.winfo_children()[0].get()] = widget.winfo_children()[
                    1
                ].get()

        if not self.editing:  # Checks if an existing guide is not being edited
            name = tkinter.simpledialog.askstring(
                "Save", "What would you like to name the guide?"
            )
            if name not in self.guides:  # Checks to see if guide already exists
                self.guides[name] = problems
                with open("guides.json", "w") as json_file:
                    json.dump(self.guides, json_file, indent=4)
                tkinter.messagebox.showinfo("Success", "Guide save is successful!")
                self.LoadExistingGuides()
            else:
                tkinter.messagebox.showinfo(
                    "Error", "The name you have chosen are already in your guides!"
                )
        else:  # Automatically saves guide edit
            self.guides[self.EditingGuide["name"]] = problems
            with open("guides.json", "w") as json_file:
                json.dump(self.guides, json_file, indent=4)
            tkinter.messagebox.showinfo("Success", "Guide edit is successful!")

            self.editing = False
            self.EditingGuide["original"] = {}
            self.EditingGuide["name"] = ""
            self.LoadExistingGuides()

    def Create(
        self, question, answer, qoa
    ):  # Creates a new QA (Input: (False, False) if its adding Question and Answer manually
        # Pre-Setup
        self.QARow += 1

        MainFrame = customtkinter.CTkFrame(
            master=self.ScrollableEditorFrame, width=386, height=70, fg_color="#222222"
        )
        EntryQuestion = customtkinter.CTkEntry(
            master=MainFrame,
            placeholder_text="Question",
            corner_radius=4,
            width=315,
            height=33,
        )
        EntryAnswer = customtkinter.CTkEntry(
            master=MainFrame,
            placeholder_text="Answer",
            corner_radius=4,
            width=315,
            height=33,
        )

        DeleteButton = customtkinter.CTkButton(
            master=MainFrame,
            width=66,
            height=66,
            fg_color="#343638",
            text_color="#9E9E9E",
            corner_radius=4,
            border_width=2,
            border_color="#565B5E",
            text="Delete",
            font=("Arial", 16),
        )

        # Setup
        MainFrame.grid(row=self.QARow - 1, column=0, pady=3, padx=3)
        EntryQuestion.place(x=1.75, y=1.75)
        EntryAnswer.place(x=1.75, y=35.75)
        DeleteButton.place(x=318, y=1.75)

        # Finalizing
        if question and answer:  # Sees if it's a guide being edited
            EntryQuestion.insert(0, question)
            EntryAnswer.insert(0, answer)

        EntryQuestion.bind("<Return>", lambda event: self.Focus(EntryAnswer))
        # QOA of Life - Skips to EntryAnswer when return is pressed
        EntryAnswer.bind("<Return>", lambda event: self.QOACreate())
        # QOA of Life - Makes new question and answer when return is pressed

        self.CreateQA.grid(row=self.QARow, column=0, padx=3, pady=3)
        self.QuestionAnswers.append(MainFrame)
        DeleteButton.configure(command=lambda: self.Delete(MainFrame))

        # For Quality of Life
        if qoa:
            return EntryQuestion

    def Delete(self, qa):  # Handler for deleting a questionAnswer
        qa.destroy()
        self.QuestionAnswers.remove(qa)

    def DeleteGuide(self):  # Handles deleting guide
        if self.editing:
            if tkinter.messagebox.askyesno(
                "Delete",
                f"Are you sure you want to delete '{self.EditingGuide['name']}'? You will not be able to recover it.",
            ):
                self.guides.pop(self.EditingGuide["name"])
                with open("guides.json", "w") as json_file:
                    json.dump(self.guides, json_file, indent=4)
                tkinter.messagebox.showinfo("Success", "Successfully deleted guide!")

                self.EditingGuide["original"] = {}
                self.EditingGuide["name"] = ""
                self.SaveButton.configure(text_color="white")
                self.editing = False

                self.LoadExistingGuides()
                self.ClearEditor(True)
        else:
            tkinter.messagebox.showinfo(
                "Error", "You must be editing a guide to delete it!"
            )

    def Exit(self):  # Asks user if they want to exit program
        if tkinter.messagebox.askyesno(
            "Exit", "Are you sure you want to exit? Your progress will not save."
        ):
            self.destroy()

    @staticmethod
    def Focus(
        answerEntry,
    ):  # Quality of Life function where if user presses enter in question, it'll focus it onto answer
        answerEntry.focus()


APP = MAIN()
APP.protocol("WM_DELETE_WINDOW", APP.Exit)

APP.mainloop()