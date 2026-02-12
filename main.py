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
        
    
       
SideContainer = Frame(window)
SideContainer.pack(side=RIGHT, fill=Y)
CreationTaskBackground = Frame(SideContainer, width=200, bg="#2b2b2b")
CreationTaskBackground.pack_forget()

CreateGoalTitleField = Entry(CreationTaskBackground)
CreateGoalTitleField.pack_forget()

def ShowGoalCreationMenu():
    AddNewGoalButton.pack_forget()
    CreationTaskBackground.pack(side=RIGHT, fill=Y)
    CreationTaskBackground.pack_propagate(False)
    CreateGoalTitleField.pack(pady=50)
    IsHabitCheckBox.pack(pady= 100)
    IsTaskCheckBox.pack(pady=200)

def SubmitNewGoal():
    NewGoal = Goal(CreateGoalTitleField.get())
    GoalList.append(NewGoal)

    if len(GoalList) == 1:
        GoalTitleDisplay.config(text=GoalList[0].Title) 
        
    CreateGoalTitleField.pack_forget()


GoalTitleDisplay = Label(window, text="Goal Title",bg="white")
GoalTitleDisplay.pack()
AddNewGoalButton = Button(window)

AddtaskImage = PhotoImage(file="AddTaskButton.png")
AddNewGoalButton.config(image=AddtaskImage)
AddNewGoalButton.config(command=ShowGoalCreationMenu)
AddNewGoalButton.pack(side=TOP, anchor=NE)


HabitDecider = IntVar()
TaskDecider = IntVar()
IsHabitCheckBox = Checkbutton(CreationTaskBackground, text="Is This a Habit?", variable=HabitDecider, onvalue=1, offvalue=0)
IsTaskCheckBox = Checkbutton(CreationTaskBackground, text="Is This a Task?", variable=TaskDecider, onvalue=1, offvalue=0)

SubmitNewGoalButton = Button(window)
SubmitNewGoalButton.config(text="Submit")
SubmitNewGoalButton.config(background="#00bd32")
SubmitNewGoalButton.pack(side=BOTTOM, anchor=CENTER)
SubmitNewGoalButton.config(command=SubmitNewGoal)
SubmitNewGoalButton.pack()


window.mainloop()