import json
import os
import tkinter as tk
from tkinter import ttk

DATA_FILE = "nestjs_xp_tracker_gui.json"

ranks = [
    ("Unranked", 0), ("Bronze", 100), ("Silver", 300), ("Gold", 600),
    ("Platinum", 1000), ("Diamond", 1500), ("Master", 2100),
    ("Grandmaster", 2800), ("Legend", 3600), ("Infinite", 5000)
]

roadmap = {
    "🔥 Phase 1: Core Fundamentals": [
        ("Setup NestJS Project", "Bronze"),
        ("Understand Modules & Providers", "Bronze"),
        ("Implement Dependency Injection", "Silver"),
        ("Apply Validation & Pipes", "Silver"),
    ],
    "⚙️ Phase 2: Auth & DB": [
        ("Implement JWT Auth", "Gold"),
        ("Add Refresh Token Flow", "Platinum"),
        ("Connect to SQL DB with TypeORM", "Bronze"),
    ],
    "🌟 Bonus Achievements": [
        ("Complete All Tasks", "Legend"),
        ("Deploy Real App", "Infinite")
    ]
}

xp_per_rank = {
    "Unranked": 0, "Bronze": 100, "Silver": 300, "Gold": 600,
    "Platinum": 1000, "Diamond": 1500, "Master": 2100,
    "Grandmaster": 2800, "Legend": 3600, "Infinite": 5000
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"xp": 0, "completed": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_rank(xp):
    for name, threshold in reversed(ranks):
        if xp >= threshold:
            return name
        else:
            return "unranked"
        
    

class XPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 NestJS XP Quest Tracker")
        self.root.geometry("600x700")
        self.root.configure(bg="#1c1c1e")

        self.data = load_data()

        self.xp_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), fg="#00FF7F", bg="#1c1c1e")
        self.xp_label.pack(pady=10)

        self.progress = ttk.Progressbar(root, length=500, style="green.Horizontal.TProgressbar")
        self.progress.pack(pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("green.Horizontal.TProgressbar", foreground="#00FF7F", background="#00FF7F")

        self.task_vars = {}
        for phase, tasks in roadmap.items():
            frame = tk.LabelFrame(root, text=phase, fg="white", bg="#2c2c2e", padx=10, pady=10, font=("Helvetica", 12, "bold"))
            frame.pack(padx=10, pady=5, fill="both", expand=True)
            for task, rank in tasks:
                var = tk.BooleanVar(value=task in self.data['completed'])
                chk = tk.Checkbutton(frame, text=f"{task} ({rank} - {xp_per_rank[rank]} XP)", variable=var,
                                     command=self.update_xp, fg="white", bg="#2c2c2e", selectcolor="#1c1c1e", font=("Helvetica", 10))
                chk.pack(anchor="w")
                self.task_vars[task] = (var, rank)

        self.update_ui()

    def update_xp(self):
        xp = 0
        completed = []
        for task, (var, rank) in self.task_vars.items():
            if var.get():
                xp += xp_per_rank[rank]
                completed.append(task)
        self.data = {"xp": xp, "completed": completed}
        save_data(self.data)
        self.update_ui()

    def update_ui(self):
        xp = self.data['xp']
        rank = get_rank(xp)
        self.xp_label.config(text=f"🔥 XP: {xp} | 🧱 Rank: {rank}")
        max_xp = ranks[-1][1]
        self.progress['value'] = (xp / max_xp) * 100

root = tk.Tk()
app = XPTrackerApp(root)
root.mainloop()
