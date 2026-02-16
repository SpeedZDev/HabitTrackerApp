from tkinter import *
from datetime import date
GoalList = []


window = Tk()
window.geometry("420x420")
window.title("Tracker App")

class Goal():
    def __init__(self, Title, GoalType):
        self.Title = Title
        self.GoalType = GoalType
        self.CreatedAt = date.today()
        
        if GoalType == "Task":
            self.completed = False
            self.CompletedAt = None
        
        if GoalType == "Habit":
            self.created_at = date.today()
            self.last_done = None
            self.streak = 0
   
    def CompletedTask(self):
           if self.GoalType == "Task" and not self.completed:
               self.completed = True
               self.CompletedAt = date.today()

    def MarkHabitToday(self):
        today = date.today()
        
goalDisplayWindow = Frame(window, width=300, bg="#add8e6")
goalDisplayWindow.pack_propagate(False)
goalDisplayWindow.place(relx=0.5, rely=0.0, relheight=1.0, anchor="n")


def RenderGoal(goalToDisplay):
    GoalTypeText = Label(goalDisplayWindow, text="Task Type: " + goalToDisplay.GoalType)
    GoalTypeText.place(relx=0.5, rely=0.45, anchor=CENTER)
    DateCreatedText = Label(goalDisplayWindow, text="Goal Created: " + str(goalToDisplay.CreatedAt))
    DateCreatedText.place(relx=0.5, rely=0.65, anchor=CENTER)
    CompleteButton = Button(goalDisplayWindow)
    if goalToDisplay.GoalType == "Task":
        CompleteButton.config(text="Complete")
        CompleteButton.place(relx=0.5, rely=0.85, anchor=CENTER)
    if goalToDisplay.GoalType == "Habit":
        CompleteButton.config(text="End Streak Counter")
        CompleteButton.place(relx=0.5, rely=0.85, anchor=CENTER)


SideContainer = Frame(window, width=250)
SideContainer.place(relx=1.0, rely=0, anchor="ne", relheight=1.0)

CreationTaskBackground = Frame(SideContainer, width=150, bg="#2b2b2b")

CreationTaskBackground.pack_propagate(False)
CreationTaskBackground.pack_forget()

GoalTitleLable = Label(CreationTaskBackground, text="Enter Task Title Here")
CreateGoalTitleField = Entry(CreationTaskBackground)

def ShowGoalCreationMenu():
    CreationTaskBackground.pack(side=RIGHT, fill=Y)
     
    AddNewGoalButton.pack_forget()
    GoalTitleLable.pack(pady=10)
    CreateGoalTitleField.pack(pady=50)
    IsHabitRadio.pack(pady=10)
    IsTaskRadio.pack(pady=10)
    SubmitNewGoalButton.pack(side=BOTTOM, anchor=CENTER)

def CreateNewGoal():
    goaltype = ""
    choice = GoalTypeDecider.get()
    if choice == 1:
        goaltype = "Habit"

    if choice == 2:
        goaltype = "Task"

    NewGoal = Goal(CreateGoalTitleField.get(), goaltype)
    GoalList.append(NewGoal)

    
    GoalTitleDisplay.config(text=GoalList[len(GoalList) - 1].Title) 
    
    RenderGoal(GoalList[len(GoalList) - 1])



    GoalTitleLable.pack_forget()
    IsHabitRadio.pack_forget()
    IsTaskRadio.pack_forget()
    SubmitNewGoalButton.pack_forget()
    CreateGoalTitleField.pack_forget()
    CreateGoalTitleField.pack_forget()
    CreationTaskBackground.pack_forget()
    AddNewGoalButton.pack(side=TOP, anchor=NE)
  
    

GoalTitleDisplay = Label(window, text="Goal Title", bg="white")
GoalTitleDisplay.place(relx=0.5, y=8, anchor="n")
AddNewGoalButton = Button(window)

AddtaskImage = PhotoImage(file="AddTaskButton.png")
AddNewGoalButton.config(image=AddtaskImage)
AddNewGoalButton.config(command=ShowGoalCreationMenu)
AddNewGoalButton.pack(side=TOP, anchor=NE)

GoalTypeDecider = IntVar()
IsHabitRadio = Radiobutton(CreationTaskBackground,text="Is This a Habit?",variable=GoalTypeDecider,value=1)
IsTaskRadio = Radiobutton(CreationTaskBackground,text="Is This a Task?",variable=GoalTypeDecider,value=2)

SubmitNewGoalButton = Button(CreationTaskBackground)
SubmitNewGoalButton.config(text="Submit")
SubmitNewGoalButton.config(background="#00bd32")
SubmitNewGoalButton.pack(side=BOTTOM, anchor=CENTER)
SubmitNewGoalButton.config(command=CreateNewGoal)




window.mainloop()