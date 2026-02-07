from tkinter import *
GoalList = []


window = Tk()
window.geometry("420x420")
window.title("Tracker App")

CreateGoalTitleField = Entry()
CreateGoalTitleField.place_forget()


class Goal():
    def __init__(self, Title):
        self.Title = Title
       


def ShowGoalCreationMenu():
    CreateGoalTitleField.pack()
    

def SubmitNewGoal():
    NewGoal = Goal(CreateGoalTitleField.get())
    
    GoalList.append(NewGoal)
    

def CloseTextTyping(event):

    if event.widget is not CreateGoalTitleField:
        CreateGoalTitleField.pack_forget()

GoalTitleDisplay = Label(window, text="Goal Title",bg="white")
GoalTitleDisplay.pack()
AddNewGoalButton = Button(window)

AddtaskImage = PhotoImage(file="AddTaskButton.png")
AddNewGoalButton.config(image=AddtaskImage)
AddNewGoalButton.config(command=ShowGoalCreationMenu)
AddNewGoalButton.pack(side=TOP, anchor=NE)

SubmitNewGoalButton = Button(window)
SubmitNewGoalButton.config(text="Submit")
SubmitNewGoalButton.config(background="#00bd32")
SubmitNewGoalButton.pack(side=BOTTOM, anchor=CENTER)
SubmitNewGoalButton.config(command=SubmitNewGoal)
SubmitNewGoalButton.pack()

window.bind("<Button-1>", CloseTextTyping)

window.mainloop()