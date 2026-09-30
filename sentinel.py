import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
import datetime

# 🔊 Voice Support
try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voice_support = True
except:
    voice_support = False

def speak(text):
    if voice_support:
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

# ---------- CORE ----------
def ping_host(host):
    return "ONLINE" if os.system(f"ping -n 1 {host} > nul") == 0 else "OFFLINE"

# ---------- TYPEWRITER ----------
def type_writer(text, tag=None):
    for char in text:
        output.insert(tk.END, char, tag)
        output.update()
        time.sleep(0.01)
    output.insert(tk.END, "\n")

# ---------- MONITOR ----------
def monitor():
    while running:
        output.delete(1.0, tk.END)

        total = len(hosts)
        online = 0

        now = datetime.datetime.now().strftime("%H:%M:%S")
        output.insert(tk.END, f">>> LIVE MONITOR {now}\n", "header")
        output.insert(tk.END, "-"*50 + "\n")

        for host in hosts:
            status = ping_host(host)

            if status == "ONLINE":
                online += 1
                output.insert(tk.END, f"[+] {host} ---> ONLINE\n", "online")
            else:
                output.insert(tk.END, f"[!] {host} ---> OFFLINE\n", "offline")

                # 🔊 Voice Alert
                threading.Thread(
                    target=speak,
                    args=(f"Alert! {host} is offline",),
                    daemon=True
                ).start()

        health = (online / total * 100) if total else 0
        health_var.set(f"SYSTEM HEALTH: {health:.1f}%")
        stats_var.set(f"NODES:{total} | ACTIVE:{online} | CRITICAL:{total-online}")

        type_writer("AI ANALYSIS: NETWORK STABLE", "header")

        time.sleep(refresh_var.get())

# ---------- ACTIONS ----------
def start():
    global running
    if not hosts:
        messagebox.showwarning("Error", "Add IP first")
        return
    running = True
    threading.Thread(target=monitor, daemon=True).start()

def add():
    ip = entry.get().strip()
    if not ip:
        return

    # Hacker loading animation
    output.delete(1.0, tk.END)
    type_writer(f">>> Injecting node {ip}...", "header")
    type_writer("Accessing network...", "header")
    type_writer("Establishing secure channel...", "header")
    type_writer("Node added successfully ✔", "online")

    if ip not in hosts:
        hosts.append(ip)
        listbox.insert(tk.END, ip)

    entry.delete(0, tk.END)

def remove():
    sel = listbox.curselection()
    if sel:
        index = sel[0]
        hosts.pop(index)
        listbox.delete(index)

# ---------- UI ----------
root = tk.Tk()
root.title("SENTINEL FINAL")
root.geometry("900x700")
root.configure(bg="black")

hosts = []
running = False

health_var = tk.StringVar(value="SYSTEM HEALTH: 0%")
stats_var = tk.StringVar(value="NODES:0 | ACTIVE:0 | CRITICAL:0")
refresh_var = tk.IntVar(value=3)

# ---------- GRID BACKGROUND ----------
canvas = tk.Canvas(root, bg="#020205", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

def draw_grid():
    canvas.delete("grid")
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    for i in range(0, w, 40):
        canvas.create_line(i, 0, i, h, fill="#0a1a2f", tags="grid")

    for i in range(0, h, 40):
        canvas.create_line(0, i, w, i, fill="#0a1a2f", tags="grid")

canvas.bind("<Configure>", lambda e: draw_grid())

# ---------- MAIN FRAME ----------
frame = tk.Frame(root, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
tk.Label(frame, textvariable=health_var,
         fg="#00FF00", bg="black",
         font=("Courier", 18, "bold")).pack(pady=10)

tk.Label(frame, textvariable=stats_var,
         fg="#00cc66", bg="black").pack()

# Entry
entry = tk.Entry(frame,
                 width=30,
                 bg="#000000",
                 fg="#00FF00",
                 insertbackground="#00FF00",
                 font=("Consolas", 12),
                 borderwidth=0,
                 highlightthickness=1,
                 highlightbackground="#00FF00")
entry.pack(pady=10)

# Refresh selector
tk.Label(frame, text="REFRESH RATE (sec)",
         fg="#00FF00", bg="black").pack()

refresh_menu = tk.OptionMenu(frame, refresh_var, 1, 2, 3, 5, 10)
refresh_menu.config(bg="#000000", fg="#00FF00")
refresh_menu.pack(pady=5)

# Buttons
tk.Button(frame, text="ADD NODE", command=add,
          bg="#002200", fg="#00FF00", width=20).pack(pady=3)

tk.Button(frame, text="REMOVE NODE", command=remove,
          bg="#220000", fg="#00FF00", width=20).pack(pady=3)

# Listbox
listbox = tk.Listbox(frame,
                     width=40,
                     height=6,
                     bg="#000000",
                     fg="#00FF00",
                     font=("Consolas", 10),
                     borderwidth=0,
                     highlightthickness=1,
                     highlightbackground="#00FF00")
listbox.pack(pady=10)

# Start
tk.Button(frame, text="START MONITOR",
          command=start,
          bg="#001a00", fg="#00FF00",
          width=25).pack(pady=10)

# Output
output = tk.Text(frame,
                 height=15,
                 width=70,
                 bg="#000000",
                 fg="#00FF00",
                 font=("Consolas", 10))
output.pack(pady=10)

output.tag_config("online", foreground="#00FF00")
output.tag_config("offline", foreground="#FF3333")
output.tag_config("header", foreground="#00FF00")

# Exit
tk.Button(frame, text="EXIT",
          command=root.destroy,
          bg="#220000", fg="#00FF00").pack(pady=10)

root.mainloop()