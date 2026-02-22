from tkinter import Canvas, Scrollbar
from datetime import date, datetime
import json, os
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

GoalList = []
DisplayIndex = 0
RenderToken = 0

def ParseDateOrDateTime(Value):
    if not Value:
        return None
    try:
        if isinstance(Value, str) and len(Value) == 10:
            D = date.fromisoformat(Value)
            return datetime(D.year, D.month, D.day, 0, 0, 0)
        return datetime.fromisoformat(Value)
    except:
        return None

def SaveGoals():
    Data = []
    for GoalItem in GoalList:
        GoalData = {
            "Title": GoalItem.Title,
            "GoalType": GoalItem.GoalType,
            "CreatedAt": GoalItem.CreatedAt.isoformat(),
            "Description": getattr(GoalItem, "Description", "")
        }

        if GoalItem.GoalType == "Task":
            GoalData["completed"] = GoalItem.completed
            GoalData["CompletedAt"] = (GoalItem.CompletedAt.isoformat() if GoalItem.CompletedAt else None)
            GoalData["RepeatEnabled"] = getattr(GoalItem, "RepeatEnabled", False)
            GoalData["RepeatSeconds"] = int(getattr(GoalItem, "RepeatSeconds", 0))

        if GoalItem.GoalType == "Habit":
            GoalData["LastDone"] = (GoalItem.LastDone.isoformat() if GoalItem.LastDone else None)
            GoalData["CooldownSeconds"] = int(getattr(GoalItem, "CooldownSeconds", 86400))

        Data.append(GoalData)

    with open("goals.json", "w") as File:
        json.dump(Data, File, indent=4)

def LoadGoals():
    if not os.path.exists("goals.json"):
        return

    with open("goals.json", "r") as File:
        Data = json.load(File)

    for Item in Data:
        NewGoal = Goal(Item["Title"], Item["GoalType"])
        NewGoal.CreatedAt = date.fromisoformat(Item["CreatedAt"])
        NewGoal.Description = Item.get("Description", "")

        if NewGoal.GoalType == "Task":
            NewGoal.completed = Item.get("completed", False)
            NewGoal.CompletedAt = ParseDateOrDateTime(Item.get("CompletedAt"))
            NewGoal.RepeatEnabled = Item.get("RepeatEnabled", False)
            NewGoal.RepeatSeconds = int(Item.get("RepeatSeconds", 0))

        if NewGoal.GoalType == "Habit":
            NewGoal.LastDone = ParseDateOrDateTime(Item.get("LastDone"))
            NewGoal.CooldownSeconds = int(Item.get("CooldownSeconds", 86400))

        GoalList.append(NewGoal)

class Goal:
    def __init__(self, Title, GoalType):
        self.Title = Title
        self.GoalType = GoalType
        self.CreatedAt = date.today()
        self.Description = ""

        if GoalType == "Task":
            self.completed = False
            self.CompletedAt = None
            self.RepeatEnabled = False
            self.RepeatSeconds = 0

        if GoalType == "Habit":
            self.LastDone = None
            self.CooldownSeconds = 86400

    def CompletedTask(self):
        if self.GoalType == "Task":
            self.completed = True
            self.CompletedAt = datetime.now()

    def ResetTask(self):
        if self.GoalType == "Task":
            self.completed = False
            self.CompletedAt = None

window = ctk.CTk()
window.geometry("900x560")
window.title("Tracker App")
window.minsize(820, 520)

window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

LeftPanel = ctk.CTkFrame(window, corner_radius=16)
LeftPanel.grid(row=0, column=0, sticky="nsw", padx=12, pady=12)
LeftPanel.grid_rowconfigure(1, weight=1)

SidebarTitle = ctk.CTkLabel(LeftPanel, text="Goals", font=ctk.CTkFont(size=18, weight="bold"))
SidebarTitle.grid(row=0, column=0, padx=14, pady=(14, 8), sticky="w")

CardCanvas = Canvas(LeftPanel, bg="#15171a", highlightthickness=0)
CardScrollbar = Scrollbar(LeftPanel, orient="vertical", command=CardCanvas.yview)
CardCanvas.configure(yscrollcommand=CardScrollbar.set)

CardScrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 12))
CardCanvas.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))

CardContainer = ctk.CTkFrame(CardCanvas, fg_color="transparent")
CardCanvasWindow = CardCanvas.create_window((0, 0), window=CardContainer, anchor="nw")

def UpdateScrollRegion(event=None):
    CardCanvas.configure(scrollregion=CardCanvas.bbox("all"))

def ResizeInnerFrame(event):
    CardCanvas.itemconfig(CardCanvasWindow, width=event.width)

CardContainer.bind("<Configure>", UpdateScrollRegion)
CardCanvas.bind("<Configure>", ResizeInnerFrame)

def OnMouseWheel(event):
    CardCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

CardCanvas.bind("<Enter>", lambda e: CardCanvas.bind_all("<MouseWheel>", OnMouseWheel))
CardCanvas.bind("<Leave>", lambda e: CardCanvas.unbind_all("<MouseWheel>"))

GoalDisplayWindow = ctk.CTkFrame(window, corner_radius=16)
GoalDisplayWindow.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
GoalDisplayWindow.grid_rowconfigure(2, weight=1)
GoalDisplayWindow.grid_columnconfigure(0, weight=1)

Header = ctk.CTkFrame(GoalDisplayWindow, corner_radius=16)
Header.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 10))
Header.grid_columnconfigure(0, weight=1)

GoalTitleDisplay = ctk.CTkLabel(Header, text="Select a goal", font=ctk.CTkFont(size=22, weight="bold"))
GoalTitleDisplay.grid(row=0, column=0, sticky="w", padx=14, pady=12)

StatusPill = ctk.CTkLabel(Header, text="", corner_radius=999, padx=12, pady=6, font=ctk.CTkFont(size=12, weight="bold"))
StatusPill.grid(row=0, column=1, sticky="e", padx=14, pady=12)

Content = ctk.CTkFrame(GoalDisplayWindow, corner_radius=16)
Content.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
Content.grid_columnconfigure(0, weight=1)

SideContainer = ctk.CTkFrame(window, corner_radius=16, width=320)
PanelWidth = 320
PanelHiddenX = 900
PanelShownX = 900 - PanelWidth - 12
SideContainer.place(x=9999, y=12, relheight=0.955)

PanelTitle = ctk.CTkLabel(SideContainer, text="Create Goal", font=ctk.CTkFont(size=18, weight="bold"))
PanelTitle.pack(padx=16, pady=(16, 10), anchor="w")

GoalTitleLable = ctk.CTkLabel(SideContainer, text="Title")
GoalTitleLable.pack(padx=16, pady=(0, 6), anchor="w")

CreateGoalTitleField = ctk.CTkEntry(SideContainer, placeholder_text="e.g. Finish homework")
CreateGoalTitleField.pack(padx=16, pady=(0, 12), fill="x")

DescriptionLabel = ctk.CTkLabel(SideContainer, text="Description")
DescriptionLabel.pack(padx=16, pady=(0, 6), anchor="w")

CreateDescriptionBox = ctk.CTkTextbox(SideContainer, height=90, corner_radius=12)
CreateDescriptionBox.pack(padx=16, pady=(0, 14), fill="x")

GoalTypeLabel = ctk.CTkLabel(SideContainer, text="Type")
GoalTypeLabel.pack(padx=16, pady=(0, 6), anchor="w")

GoalTypeDecider = ctk.IntVar(value=0)

IsHabitRadio = ctk.CTkRadioButton(SideContainer, text="Habit", variable=GoalTypeDecider, value=1)
IsTaskRadio = ctk.CTkRadioButton(SideContainer, text="Task", variable=GoalTypeDecider, value=2)
IsHabitRadio.pack(padx=16, pady=6, anchor="w")
IsTaskRadio.pack(padx=16, pady=(0, 12), anchor="w")

RepeatEnabledVar = ctk.BooleanVar(value=False)
RepeatSwitch = ctk.CTkSwitch(SideContainer, text="Repeat Task", variable=RepeatEnabledVar)
RepeatSwitch.pack(padx=16, pady=(4, 10), anchor="w")

RepeatTimeLabel = ctk.CTkLabel(SideContainer, text="Repeat Cooldown")
RepeatTimeLabel.pack(padx=16, pady=(0, 6), anchor="w")

RepeatTimeRow = ctk.CTkFrame(SideContainer, fg_color="transparent")
RepeatTimeRow.pack(padx=16, pady=(0, 12), fill="x")

RepeatHoursVar = ctk.IntVar(value=0)
RepeatMinutesVar = ctk.IntVar(value=0)
RepeatSecondsVar = ctk.IntVar(value=0)

def ClampInt(Var, MinVal, MaxVal):
    Val = Var.get()
    if Val < MinVal:
        Var.set(MinVal)
    if Val > MaxVal:
        Var.set(MaxVal)

def MakeTimeSpinner(Parent, TitleText, Var, MinVal, MaxVal):
    Box = ctk.CTkFrame(Parent, corner_radius=14)
    Box.pack(side="left", expand=True, fill="x", padx=6)

    Title = ctk.CTkLabel(Box, text=TitleText, text_color="#a6acb8")
    Title.pack(pady=(8, 2))

    ValueLabel = ctk.CTkLabel(Box, textvariable=Var, font=ctk.CTkFont(size=18, weight="bold"))
    ValueLabel.pack(pady=(0, 6))

    ButtonRow = ctk.CTkFrame(Box, fg_color="transparent")
    ButtonRow.pack(pady=(0, 10))

    def Up():
        Var.set(Var.get() + 1)
        ClampInt(Var, MinVal, MaxVal)

    def Down():
        Var.set(Var.get() - 1)
        ClampInt(Var, MinVal, MaxVal)

    UpButton = ctk.CTkButton(ButtonRow, text="▲", width=44, height=30, corner_radius=10, command=Up)
    DownButton = ctk.CTkButton(ButtonRow, text="▼", width=44, height=30, corner_radius=10, fg_color="#2b2f36", hover_color="#343a43", command=Down)
    UpButton.pack()
    DownButton.pack(pady=(6, 0))
    return Box

MakeTimeSpinner(RepeatTimeRow, "Hours", RepeatHoursVar, 0, 999)
MakeTimeSpinner(RepeatTimeRow, "Minutes", RepeatMinutesVar, 0, 59)
MakeTimeSpinner(RepeatTimeRow, "Seconds", RepeatSecondsVar, 0, 59)

SubmitNewGoalButton = ctk.CTkButton(SideContainer, text="Create", height=40)
SubmitNewGoalButton.pack(padx=16, pady=(6, 10), fill="x")

CancelButton = ctk.CTkButton(SideContainer, text="Cancel", height=40, fg_color="#2b2f36", hover_color="#343a43")
CancelButton.pack(padx=16, pady=(0, 16), fill="x")

AddNewGoalButton = ctk.CTkButton(window, text="+ New", height=38, corner_radius=12, font=ctk.CTkFont(size=14, weight="bold"))
AddNewGoalButton.place(relx=1.0, x=-16, y=16, anchor="ne")

def SelectGoal(GoalItem):
    global DisplayIndex
    if GoalItem not in GoalList:
        return
    
    DisplayIndex = GoalList.index(GoalItem)
    GoalTitleDisplay.configure(text=GoalList[DisplayIndex].Title)
    RenderGoal(GoalList[DisplayIndex])

def DeleteGoal(GoalItem):
    global DisplayIndex
    if GoalItem not in GoalList:
        return

    Index = GoalList.index(GoalItem)
    GoalList.pop(Index)

    SaveGoals()
    RepositionCards()

    if GoalList:
        DisplayIndex = min(Index, len(GoalList) - 1)
        SelectGoal(GoalList[DisplayIndex])
    else:
        DisplayIndex = 0
        GoalTitleDisplay.configure(text="Select a goal")
        for W in Content.winfo_children():
            W.destroy()
        StatusPill.configure(text="", fg_color="transparent")

def CreateGoalCard(Parent, GoalItem):
    Card = ctk.CTkFrame(Parent, corner_radius=14)
    Card.pack(fill="x", padx=10, pady=6)

    Row = ctk.CTkFrame(Card, fg_color="transparent")
    Row.pack(fill="x", padx=12, pady=10)
    Row.grid_columnconfigure(0, weight=1)

    Title = ctk.CTkLabel(Row, text=GoalItem.Title, font=ctk.CTkFont(size=14, weight="bold"))
    Title.grid(row=0, column=0, sticky="w")

    TypeText = ctk.CTkLabel(Row, text=GoalItem.GoalType, font=ctk.CTkFont(size=12), text_color="#a6acb8")
    TypeText.grid(row=1, column=0, sticky="w", pady=(2, 0))

    DeleteButton = ctk.CTkButton(Row, text="✕", width=34, height=28, corner_radius=10, fg_color="#3a2020", hover_color="#4a2424")
    DeleteButton.grid(row=0, column=1, rowspan=2, sticky="e", padx=(10, 0))

    def OnDeleteClick(e=None, G=GoalItem):
        DeleteGoal(G)
        return "break"

    def OnSelectClick(e=None, G=GoalItem):
        SelectGoal(G)
        return "break"

    DeleteButton.configure(command=OnDeleteClick)
    Card.bind("<Button-1>", OnSelectClick)
    Title.bind("<Button-1>", OnSelectClick)
    TypeText.bind("<Button-1>", OnSelectClick)

    return Card

def RepositionCards():
    for Child in CardContainer.winfo_children():
        Child.destroy()

    for GoalItem in GoalList:
        CreateGoalCard(CardContainer, GoalItem)

    CardContainer.update_idletasks()
    CardCanvas.configure(scrollregion=CardCanvas.bbox("all"))

def FormatSeconds(TotalSeconds):
    TotalSeconds = max(0, int(TotalSeconds))
    Hours = TotalSeconds // 3600
    Minutes = (TotalSeconds % 3600) // 60
    Seconds = TotalSeconds % 60
    if Hours > 99:
        return f"{Hours}h {Minutes:02d}m {Seconds:02d}s"
    return f"{Hours:02d}:{Minutes:02d}:{Seconds:02d}"

def RenderGoal(GoalToDisplay):
    global RenderToken
    RenderToken += 1
    MyToken = RenderToken

    for W in Content.winfo_children():
        W.destroy()

    if GoalToDisplay.GoalType == "Task":
        if getattr(GoalToDisplay, "completed", False):
            StatusPill.configure(text="TASK DONE", fg_color="#1f3b2a")
        else:
            StatusPill.configure(text="TASK", fg_color="#1f2f3b")
    else:
        StatusPill.configure(text="HABIT", fg_color="#3b2f1f")

    Info = ctk.CTkFrame(Content, corner_radius=16)
    Info.pack(fill="x", padx=14, pady=(14, 10))

    ctk.CTkLabel(Info, text=f"Type: {GoalToDisplay.GoalType}", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(12, 2))
    ctk.CTkLabel(Info, text=f"Created: {GoalToDisplay.CreatedAt}", text_color="#a6acb8").pack(anchor="w", padx=14, pady=(0, 6))

    DescText = getattr(GoalToDisplay, "Description", "")
    if DescText.strip():
        DescBox = ctk.CTkTextbox(Info, height=90, corner_radius=12)
        DescBox.pack(fill="x", padx=14, pady=(6, 12))
        DescBox.insert("1.0", DescText)
        DescBox.configure(state="disabled")
    else:
        ctk.CTkLabel(Info, text="No description.", text_color="#a6acb8").pack(anchor="w", padx=14, pady=(6, 12))

    Actions = ctk.CTkFrame(Content, corner_radius=16)
    Actions.pack(fill="x", padx=14, pady=(0, 14))

    def OnCompleteTask():
        GoalToDisplay.CompletedTask()
        SaveGoals()
        RepositionCards()
        RenderGoal(GoalToDisplay)

    if GoalToDisplay.GoalType == "Task":
        RepeatEnabled = bool(getattr(GoalToDisplay, "RepeatEnabled", False))
        RepeatSeconds = int(getattr(GoalToDisplay, "RepeatSeconds", 0))
        Completed = bool(getattr(GoalToDisplay, "completed", False))

        if Completed and RepeatEnabled and RepeatSeconds > 0:
            Now = datetime.now()
            CompletedAt = getattr(GoalToDisplay, "CompletedAt", None)

            if CompletedAt is None:
                GoalToDisplay.ResetTask()
                SaveGoals()
                RepositionCards()
                RenderGoal(GoalToDisplay)

                return

            Elapsed = (Now - CompletedAt).total_seconds()
            Remaining = int(RepeatSeconds - Elapsed)

            if Remaining <= 0:
                GoalToDisplay.ResetTask()
                SaveGoals()
                RepositionCards()
                RenderGoal(GoalToDisplay)

                return

            WaitLabel = ctk.CTkLabel(Actions,text=f"Repeat In: {FormatSeconds(Remaining)}",font=ctk.CTkFont(size=13, weight="bold"),text_color="#ffcc7a")
            WaitLabel.pack(padx=14, pady=(14, 8), anchor="w")

            ConfigLabel = ctk.CTkLabel(Actions, text=f"Repeat Time Set: {FormatSeconds(RepeatSeconds)}",text_color="#a6acb8")
            ConfigLabel.pack(padx=14, pady=(0, 12), anchor="w")

            DisabledButton = ctk.CTkButton(Actions, text="Completed", height=40, state="disabled")
            DisabledButton.pack(fill="x", padx=14, pady=(0, 14))

            def Tick():
                if MyToken != RenderToken:
                    return
                RenderGoal(GoalToDisplay)

            window.after(250, Tick)
            return

        ButtonText = "Mark Complete" if not Completed else "Completed"
        BtnState = "normal" if not Completed else "disabled"
        CompleteButton = ctk.CTkButton(Actions, text=ButtonText, height=40, state=BtnState, command=OnCompleteTask)
        CompleteButton.pack(fill="x", padx=14, pady=14)
        return

    Now = datetime.now()
    Last = getattr(GoalToDisplay, "LastDone", None)
    Cooldown = int(getattr(GoalToDisplay, "CooldownSeconds", 86400))
    Elapsed = Cooldown + 1 if Last is None else (Now - Last).total_seconds()

    if Elapsed >= Cooldown:
        def CompleteHabit():
            GoalToDisplay.LastDone = datetime.now()
            SaveGoals()
            RepositionCards()
            RenderGoal(GoalToDisplay)

        CompleteHabitButton = ctk.CTkButton(Actions, text="Complete Habit", height=40, command=CompleteHabit)
        CompleteHabitButton.pack(fill="x", padx=14, pady=14)
    else:
        Remaining = int(Cooldown - Elapsed)
        WaitLabel = ctk.CTkLabel(Actions, text=f"Cooldown: {FormatSeconds(Remaining)}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#ff7a7a")
        WaitLabel.pack(padx=14, pady=14, anchor="w")

        def Tick():
            if MyToken != RenderToken:
                return
            RenderGoal(GoalToDisplay)

        window.after(250, Tick)

PanelOpen = False

def RecalcPanelPositions():
    WindowWidth = window.winfo_width()
    global PanelHiddenX, PanelShownX
    PanelHiddenX = WindowWidth + 20
    PanelShownX = WindowWidth - PanelWidth - 12

def AnimatePanel(TargetX, Step=22):
    Cur = SideContainer.winfo_x()
    if abs(Cur - TargetX) <= Step:
        SideContainer.place(x=TargetX, y=12, relheight=0.955)
        return
    Cur = Cur + Step if Cur < TargetX else Cur - Step
    SideContainer.place(x=Cur, y=12, relheight=0.955)
    window.after(10, lambda: AnimatePanel(TargetX, Step))

def ShowGoalCreationMenu():
    global PanelOpen
    PanelOpen = True
    RecalcPanelPositions()
    SideContainer.place(x=PanelHiddenX, y=12, relheight=0.955)
    AnimatePanel(PanelShownX)

    CreateGoalTitleField.delete(0, "end")
    CreateDescriptionBox.delete("1.0", "end")
    GoalTypeDecider.set(0)
    RepeatEnabledVar.set(False)
    RepeatHoursVar.set(0)
    RepeatMinutesVar.set(0)
    RepeatSecondsVar.set(0)
    CreateGoalTitleField.focus()

def HideGoalCreationMenu():
    global PanelOpen
    PanelOpen = False
    RecalcPanelPositions()
    AnimatePanel(PanelHiddenX)

AddNewGoalButton.configure(command=ShowGoalCreationMenu)
CancelButton.configure(command=HideGoalCreationMenu)

def CreateNewGoal():
    global DisplayIndex

    TitleText = CreateGoalTitleField.get().strip()
    DescriptionText = CreateDescriptionBox.get("1.0", "end").strip()
    Choice = GoalTypeDecider.get()

    if not TitleText:
        StartX = SideContainer.winfo_x()
        def Shake(I=0):
            if I >= 8:
                SideContainer.place(x=StartX, y=12, relheight=0.955)
                return
            Dx = 8 if I % 2 == 0 else -8
            SideContainer.place(x=StartX + Dx, y=12, relheight=0.955)
            window.after(35, lambda: Shake(I + 1))
        Shake()
        return

    if Choice == 1:
        GoalType = "Habit"
    elif Choice == 2:
        GoalType = "Task"
    else:
        return

    NewGoal = Goal(TitleText, GoalType)
    NewGoal.Description = DescriptionText

    if GoalType == "Task":
        RepeatEnabled = bool(RepeatEnabledVar.get())
        RepeatSeconds = int((RepeatHoursVar.get() * 3600) + (RepeatMinutesVar.get() * 60) + RepeatSecondsVar.get())

        if RepeatEnabled and RepeatSeconds > 0:
            NewGoal.RepeatEnabled = True
            NewGoal.RepeatSeconds = RepeatSeconds
        else:
            NewGoal.RepeatEnabled = False
            NewGoal.RepeatSeconds = 0

    GoalList.append(NewGoal)
    SaveGoals()
    RepositionCards()

    DisplayIndex = len(GoalList) - 1
    SelectGoal(GoalList[DisplayIndex])
    HideGoalCreationMenu()

SubmitNewGoalButton.configure(command=CreateNewGoal)

def OnArrowUp(event=None):
    global DisplayIndex
    if not GoalList:
        return
    DisplayIndex = max(0, DisplayIndex - 1)
    SelectGoal(GoalList[DisplayIndex])

def OnArrowDown(event=None):
    global DisplayIndex
    if not GoalList:
        return
    DisplayIndex = min(len(GoalList) - 1, DisplayIndex + 1)
    SelectGoal(GoalList[DisplayIndex])

window.bind_all("<Up>", OnArrowUp)
window.bind_all("<Down>", OnArrowDown)

def OnResize(event=None):
    RecalcPanelPositions()
    SideContainer.place(x=(PanelShownX if PanelOpen else PanelHiddenX), y=12, relheight=0.955)

window.bind("<Configure>", lambda e: OnResize())

LoadGoals()
RepositionCards()

if GoalList:
    SelectGoal(GoalList[0])
else:
    StatusPill.configure(text="", fg_color="transparent")

window.after(50, OnResize)
window.mainloop()
