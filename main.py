from tkinter import *
from datetime import date, datetime

GoalList = []
CardWidgets = []
DisplayIndex = 0

RenderToken = 0

window = Tk()
window.geometry("420x420")
window.title("Tracker App")

#Goal Class
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
            self.LastDone = None
            self.CooldownSeconds = 86400   
   
    def CompletedTask(self):
           if self.GoalType == "Task" and not self.completed:
               self.completed = True
               self.CompletedAt = date.today()

    def MarkHabitToday(self):
        today = date.today()
        

LeftPanel = Frame(window, width=150, bg="#2c2c2c")
LeftPanel.pack(side="left", fill="y")
LeftPanel.pack_propagate(False)

cardCanvas = Canvas(LeftPanel, bg="#2c2c2c", highlightthickness=0)
cardScrollbar = Scrollbar(LeftPanel, orient="vertical", command=cardCanvas.yview)

cardCanvas.configure(yscrollcommand=cardScrollbar.set)

cardScrollbar.pack(side="right", fill="y")
cardCanvas.pack(side="left", fill="both", expand=True)


CardContainer = Frame(cardCanvas, bg="#2c2c2c")

cardCanvasWindow = cardCanvas.create_window((0, 0), window=CardContainer, anchor="nw")

def UpdateScrollRegion(event=None):
    cardCanvas.configure(scrollregion=cardCanvas.bbox("all"))

CardContainer.bind("<Configure>", UpdateScrollRegion)

def ResizeInnerFrame(event):
    cardCanvas.itemconfig(cardCanvasWindow, width=event.width)

cardCanvas.bind("<Configure>", ResizeInnerFrame)


def OnMouseWheel(event):
    cardCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

cardCanvas.bind("<Enter>", lambda e: cardCanvas.bind_all("<MouseWheel>", OnMouseWheel))
cardCanvas.bind("<Leave>", lambda e: cardCanvas.unbind_all("<MouseWheel>"))


cardCanvas.bind_all("<MouseWheel>", OnMouseWheel)

goalDisplayWindow = Frame(window, width=300, bg="#add8e6")
goalDisplayWindow.pack_propagate(False)
goalDisplayWindow.place(relx=0.5, rely=0.0, relheight=1.0, anchor="n")


def CreateGoalCard(parent, goal):
    card = Frame(parent, bg="#444444", bd=2, relief="raised", height=80)
    card.pack_propagate(False)

    title = Label(card, text=goal.Title, bg="#444444", fg="white")
    title.pack(pady=(8, 0))

    goalTypeLabel = Label(card, text=goal.GoalType, bg="#444444", fg="lightgray")
    goalTypeLabel.pack(pady=(2, 0))

    deleteButton = Button(card, text="X", bg="red", fg="white", width=2)
    deleteButton.place(relx=1.0, x=-5, y=5, anchor="ne")

    def OnDeleteClick(e, g=goal):
        DeleteGoal(g)
        return "break"

    deleteButton.bind("<Button-1>", OnDeleteClick)

    card.bind("<Button-1>", lambda e, g=goal: SelectGoal(g))
    title.bind("<Button-1>", lambda e, g=goal: SelectGoal(g))
    goalTypeLabel.bind("<Button-1>", lambda e, g=goal: SelectGoal(g))

    return card

def RepositionCards():
    # wipe the UI list
    for child in CardContainer.winfo_children():
        child.destroy()

    # rebuild from GoalList
    for goal in GoalList:
        card = CreateGoalCard(CardContainer, goal)
        card.pack(fill="x", padx=10, pady=6)

    CardContainer.update_idletasks()
    cardCanvas.configure(scrollregion=cardCanvas.bbox("all"))

def DeleteGoal(goal):
    global DisplayIndex

    if goal not in GoalList:
        return

    index = GoalList.index(goal)
    GoalList.pop(index)

    RepositionCards()

    if GoalList:
        DisplayIndex = min(index, len(GoalList) - 1)
        SelectGoal(GoalList[DisplayIndex])
    else:
        DisplayIndex = 0
        GoalTitleDisplay.config(text="Goal Title")
        for w in goalDisplayWindow.winfo_children():
            w.destroy()

#Renders My Goals
def RenderGoal(goalToDisplay):
    global RenderToken
    RenderToken += 1
    MyToken = RenderToken

    # clear display area
    for w in goalDisplayWindow.winfo_children():
        w.destroy()

    GoalTypeText = Label(goalDisplayWindow, text="Task Type: " + goalToDisplay.GoalType)
    GoalTypeText.place(relx=0.5, rely=0.45, anchor=CENTER)

    DateCreatedText = Label(goalDisplayWindow, text="Goal Created: " + str(goalToDisplay.CreatedAt))
    DateCreatedText.place(relx=0.5, rely=0.65, anchor=CENTER)

    # -------- TASK --------
    if goalToDisplay.GoalType == "Task":
        CompleteButton = Button(goalDisplayWindow, text="Complete", command=OnComplete)
        CompleteButton.place(relx=0.5, rely=0.85, anchor=CENTER)
        return

    # -------- HABIT (cooldown) --------
    if goalToDisplay.GoalType == "Habit":
        now = datetime.now()
        last = getattr(goalToDisplay, "LastDone", None)
        cooldown = getattr(goalToDisplay, "CooldownSeconds", 86400)

        if last is None:
            elapsed = cooldown + 1
        else:
            elapsed = (now - last).total_seconds()

        if elapsed >= cooldown:
            def complete_habit():
                goalToDisplay.LastDone = datetime.now()
                RenderGoal(goalToDisplay)

            CompleteButton = Button(goalDisplayWindow, text="Complete Habit", command=complete_habit)
            CompleteButton.place(relx=0.5, rely=0.85, anchor=CENTER)

        else:
            remaining = int(cooldown - elapsed)

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60

            waitLabel = Label(goalDisplayWindow,text=f"Please wait {hours:02d}:{minutes:02d}:{seconds:02d}",fg="red")
            waitLabel.place(relx=0.5, rely=0.85, anchor=CENTER)

    
            def tick():
                if MyToken != RenderToken:
                    return 
                
                RenderGoal(goalToDisplay)

            goalDisplayWindow.after(1000, tick)


def OnComplete():
    print("Task Finished")


#cointianer For Task Creation Menu
SideContainer = Frame(window, width=250)
SideContainer.place(relx=1.0, rely=0, anchor="ne", relheight=1.0)

CreationTaskBackground = Frame(SideContainer, width=150, bg="#2b2b2b")

CreationTaskBackground.pack_propagate(False)
CreationTaskBackground.pack_forget()

GoalTitleLable = Label(CreationTaskBackground, text="Enter Task Title Here")
CreateGoalTitleField = Entry(CreationTaskBackground)

def SelectGoal(goal):
    global DisplayIndex

    if goal not in GoalList:
        return

    DisplayIndex = GoalList.index(goal)
    GoalTitleDisplay.config(text=GoalList[DisplayIndex].Title)
    RenderGoal(GoalList[DisplayIndex])

#opens Goal Creation Menu
def ShowGoalCreationMenu():
    CreationTaskBackground.pack(side=RIGHT, fill=Y)
     
    AddNewGoalButton.pack_forget()
    GoalTitleLable.pack(pady=10)
    CreateGoalTitleField.pack(pady=50)
    IsHabitRadio.pack(pady=10)
    IsTaskRadio.pack(pady=10)
    SubmitNewGoalButton.pack(side=BOTTOM, anchor=CENTER)

def CreateNewGoal():
    global DisplayIndex

    goaltype = ""
    choice = GoalTypeDecider.get()

    if choice == 1:
        goaltype = "Habit"
    elif choice == 2:
        goaltype = "Task"
    else:
        return  # nothing selected

    NewGoal = Goal(CreateGoalTitleField.get(), goaltype)

    GoalList.append(NewGoal)     
    RepositionCards()             

    DisplayIndex = len(GoalList) - 1
    GoalTitleDisplay.config(text=GoalList[DisplayIndex].Title)
    RenderGoal(GoalList[DisplayIndex])

    # hide menu
    GoalTitleLable.pack_forget()
    IsHabitRadio.pack_forget()
    IsTaskRadio.pack_forget()
    SubmitNewGoalButton.pack_forget()
    CreateGoalTitleField.pack_forget()
    CreationTaskBackground.pack_forget()
    AddNewGoalButton.pack(side=TOP, anchor=NE)
  
#checks when up arrow key is pressed on my keyboard
def OnArrowUp(event):
    global DisplayIndex 
    if not GoalList:
        return

    DisplayIndex = max(0, DisplayIndex-1)
    print("UpArrow Pressed")
    GoalTitleDisplay.config(text=GoalList[DisplayIndex].Title)
    
    RenderGoal(GoalList[DisplayIndex])

#checks when Down arrow key is pressed on my keyboard
def OnArrowDown(event):
    global DisplayIndex
    if not GoalList:
        return

    DisplayIndex = min(len(GoalList) - 1, DisplayIndex + 1)
    print("DownArrow Pressed")
    GoalTitleDisplay.config(text=GoalList[DisplayIndex].Title)

    RenderGoal(GoalList[DisplayIndex])

window.bind_all("<Up>", OnArrowUp)
window.bind_all("<Down>", OnArrowDown)


#displays Goal Ttitle
GoalTitleDisplay = Label(window, text="Goal Title", bg="white")
GoalTitleDisplay.place(relx=0.5, y=8, anchor="n")
AddNewGoalButton = Button(window)

#SHows Image For adding a task to open the menu
AddtaskImage = PhotoImage(file="AddTaskButton.png")
AddNewGoalButton.config(image=AddtaskImage)
AddNewGoalButton.config(command=ShowGoalCreationMenu)
AddNewGoalButton.pack(side=TOP, anchor=NE)

#Radio Buttons For Tasks
GoalTypeDecider = IntVar()
IsHabitRadio = Radiobutton(CreationTaskBackground,text="Habit",variable=GoalTypeDecider,value=1)
IsTaskRadio = Radiobutton(CreationTaskBackground,text="Task",variable=GoalTypeDecider,value=2)

SubmitNewGoalButton = Button(CreationTaskBackground)
SubmitNewGoalButton.config(text="Submit")
SubmitNewGoalButton.config(background="#00bd32")
SubmitNewGoalButton.pack(side=BOTTOM, anchor=CENTER)
SubmitNewGoalButton.config(command=CreateNewGoal)




window.mainloop()