# To-Do / Goal Tracker Application — Tkinter

A simple desktop productivity app built with **Python + Tkinter** that lets you track:
- **Tasks** (one-time items you can complete)
- **Habits** (repeatable items with **streak tracking** and “done today” logic)

It’s lightweight, fast, and designed to be easy to extend.

---

## Features

###  Tasks
- Add a task
- Mark as **Complete**
- Stores completion date (optional if your code tracks it)

###  Habits
- Add a habit
- Mark **Done Today**
- Tracks:
  - `last_done`
  - `streak` (keeps streak if done on consecutive days)

### Saves
- **Save / Load to JSON** so your list persists between runs

### Simple UI & Modern UI
- Plus button opens an “Add Goal” menu
- Choose **Task** vs **Habit**
- Each goal row shows title + type + status button:
  - Task → **Complete**
  - Habit → **Done Today**

---

## Screenshots
Add screenshots here if you want:
![image alt](https://github.com/SpeedZDev/HabitTrackerApp/blob/main/Screenshot%202026-02-22%20161623.png?raw=true)
![image alt](https://github.com/SpeedZDev/HabitTrackerApp/blob/main/Screenshot%202026-02-22%20161735.png?raw=true)
![image alt](https://github.com/SpeedZDev/HabitTrackerApp/blob/main/Screenshot%202026-02-22%20161623.png?raw=true)
---

## Requirements

- **Python 3.10+** recommended  
- **PLEASE NOTE** Tkinter comes bundled with most Python installs.
