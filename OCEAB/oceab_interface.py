import customtkinter as ctk
import os
import sys
import subprocess
import io
import threading
from contextlib import redirect_stdout

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class OceabGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OCEAB v2.0.0 - Open Computing Environment")
        self.geometry("1200x800")

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="OCEAB ENGINES", font=ctk.CTkFont(size=18, weight="bold"))
        self.sidebar_label.pack(pady=(20, 10), padx=10)

        self.engine_var = ctk.StringVar(value="None")
        engines = [
            ("None", "Default (os, sys)"),
            ("1", "Math & Data"),
            ("2", "Web & Network"),
            ("3", "Storage & Files"),
            ("4", "Dev Tools"),
            ("5", "Utilities"),
            ("6", "LOAD ALL (Full)")
        ]

        for val, text in engines:
            rb = ctk.CTkRadioButton(self.sidebar, text=text, variable=self.engine_var, value=val, command=self.load_engine)
            rb.pack(pady=10, padx=20, anchor="w")

        ctk.CTkLabel(self.sidebar, text="SYSTEM", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(30, 5))
        
        self.lib_btn = ctk.CTkButton(self.sidebar, text="Install Libraries", fg_color="#2c3e50", hover_color="#34495e", command=self.open_installer)
        self.lib_btn.pack(pady=10, padx=20)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.tab_console = self.tabview.add("Main Console")
        self.tab_editor = self.tabview.add("Script Creator")
        self.tab_files = self.tabview.add("Script Manager")

        self.setup_console_tab()
        self.setup_editor_tab()
        self.setup_files_tab()

    def setup_console_tab(self):
        self.console_output = ctk.CTkTextbox(self.tab_console, state="disabled", font=("Consolas", 13))
        self.console_output.pack(expand=True, fill="both", padx=10, pady=(10, 5))

        self.input_label = ctk.CTkLabel(self.tab_console, text="Command Input (Ctrl+Enter to Execute):", font=("Arial", 11))
        self.input_label.pack(anchor="w", padx=15)

        self.console_input = ctk.CTkTextbox(self.tab_console, height=150, font=("Consolas", 14), border_width=2)
        self.console_input.pack(fill="x", padx=10, pady=5)
        self.console_input.bind("<Control-Return>", lambda e: self.run_code())

        self.btn_frame = ctk.CTkFrame(self.tab_console, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=10, pady=5)

        self.run_btn = ctk.CTkButton(self.btn_frame, text="Execute Block", width=150, command=self.run_code)
        self.run_btn.pack(side="right")
        
        self.clear_btn = ctk.CTkButton(self.btn_frame, text="Clear Console", width=100, fg_color="#c0392b", command=lambda: self.clear_console(self.console_output))
        self.clear_btn.pack(side="left")

    def setup_editor_tab(self):
        self.filename_entry = ctk.CTkEntry(self.tab_editor, placeholder_text="script_name.py")
        self.filename_entry.pack(fill="x", padx=20, pady=(10, 5))

        self.code_editor = ctk.CTkTextbox(self.tab_editor, font=("Consolas", 14), wrap="none")
        self.code_editor.pack(expand=True, fill="both", padx=20, pady=5)

        self.save_btn = ctk.CTkButton(self.tab_editor, text="Save to /scripts", command=self.save_script)
        self.save_btn.pack(pady=10)

    def setup_files_tab(self):
        self.manager_split = ctk.CTkFrame(self.tab_files, fg_color="transparent")
        self.manager_split.pack(expand=True, fill="both")

        self.file_scroll = ctk.CTkScrollableFrame(self.manager_split, label_text="Stored Scripts", width=300)
        self.file_scroll.pack(side="left", expand=False, fill="both", padx=(0, 10), pady=10)

        self.script_console_frame = ctk.CTkFrame(self.manager_split)
        self.script_console_frame.pack(side="right", expand=True, fill="both", pady=10)

        self.script_header = ctk.CTkFrame(self.script_console_frame, height=40)
        self.script_header.pack(fill="x")
        
        ctk.CTkLabel(self.script_header, text="SCRIPT OUTPUT", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        
        self.close_con_btn = ctk.CTkButton(self.script_header, text="Clear Output", width=80, height=24, command=lambda: self.clear_console(self.script_console_out))
        self.close_con_btn.pack(side="right", padx=10)

        self.script_console_out = ctk.CTkTextbox(self.script_console_frame, state="disabled", font=("Consolas", 12), fg_color="#000000")
        self.script_console_out.pack(expand=True, fill="both", padx=5, pady=5)

        self.refresh_file_list()

    def log(self, message, target=None):
        console = target if target else self.console_output
        console.configure(state="normal")
        console.insert("end", f"{message}\n")
        console.see("end")
        console.configure(state="disabled")

    def clear_console(self, target):
        target.configure(state="normal")
        target.delete("1.0", "end")
        target.configure(state="disabled")

    def run_code(self):
        user_input = self.console_input.get("1.0", "end-1c").strip()
        if not user_input: return
        
        self.log(f"OCEAB > Running Code...")
        
        try:
            compile(user_input, '<string>', 'exec')
            f = io.StringIO()
            with redirect_stdout(f):
                exec(user_input, globals())
            out = f.getvalue()
            if out: self.log(out)
        except SyntaxError as se:
            self.log(f"SYNTAX ERROR: {se.msg} (Line {se.lineno})")
        except Exception as e:
            self.log(f"RUNTIME ERROR: {e}")

    def save_script(self):
        name = self.filename_entry.get().strip() or "script.py"
        if not name.endswith(".py"): name += ".py"
        content = self.code_editor.get("1.0", "end-1c")
        
        if not os.path.exists("scripts"): os.makedirs("scripts")
        with open(os.path.join("scripts", name), "w") as f:
            f.write(content)
        
        self.log(f"System: Script '{name}' saved.")
        self.refresh_file_list()

    def refresh_file_list(self):
        for widget in self.file_scroll.winfo_children():
            widget.destroy()
        if not os.path.exists("scripts"): return
        
        for file in os.listdir("scripts"):
            if file.endswith(".py"):
                frame = ctk.CTkFrame(self.file_scroll)
                frame.pack(fill="x", pady=2, padx=5)
                ctk.CTkLabel(frame, text=file, width=120, anchor="w").pack(side="left", padx=5)
                ctk.CTkButton(frame, text="RUN", width=40, fg_color="#27ae60", command=lambda f=file: self.run_external_script(f)).pack(side="right", padx=2)

    def run_external_script(self, filename):
        path = os.path.join("scripts", filename)
        self.log(f"--- START: {filename} ---", self.script_console_out)
        
        def task():
            try:
                process = subprocess.Popen([sys.executable, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                if stdout: self.log(stdout, self.script_console_out)
                if stderr: self.log(f"ERROR:\n{stderr}", self.script_console_out)
            except Exception as e:
                self.log(f"EXECUTION FAILURE: {e}", self.script_console_out)
            self.log("--- FINISHED ---", self.script_console_out)

        threading.Thread(target=task, daemon=True).start()

    def open_installer(self):
        dialog = ctk.CTkInputDialog(text="Enter Library Name:", title="Pip Installer")
        lib = dialog.get_input()
        if lib:
            self.log(f"SYSTEM: Installing '{lib}'...")
            threading.Thread(target=self.pip_install, args=(lib,), daemon=True).start()

    def pip_install(self, lib):
        try:
            proc = subprocess.Popen([sys.executable, "-m", "pip", "install", lib], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate()
            if stdout: self.log(f"PIP SUCCESS: {stdout}")
            if stderr: self.log(f"PIP INFO: {stderr}")
        except Exception as e:
            self.log(f"INSTALL ERROR: {e}")

    def load_engine(self):
        choice = self.engine_var.get()
        self.log(f"OCEAB: Initializing Engine {choice}...")
        try:
            if choice == '1':
                global np, pd, plt, math, statistics
                import numpy as np, pandas as pd, matplotlib.pyplot as plt, math, statistics
                self.log("Engine 1 Loaded: Math & Data Science libraries ready.")
            elif choice == '2':
                global socket, http, urllib, smtplib, webbrowser
                import socket, http, urllib, smtplib, webbrowser
                self.log("Engine 2 Loaded: Web & Networking libraries ready.")
            elif choice == '3':
                global json, csv, sqlite3, pathlib, shutil
                import json, csv, sqlite3, pathlib, shutil
                self.log("Engine 3 Loaded: File System & Database libraries ready.")
            elif choice == '4':
                global itertools, functools, dataclasses, collections, re, enum
                import itertools, functools, dataclasses, collections, re, enum
                self.log("Engine 4 Loaded: Developer toolkit ready.")
            elif choice == '5':
                global time, datetime, random, argparse
                import time, datetime, random, argparse
                self.log("Engine 5 Loaded: Utilities & System libraries ready.")
            elif choice == '6':
                self.log("Loading Full Suite...")
                exec("import numpy as np, pandas as pd, matplotlib.pyplot as plt, math, statistics, socket, http, urllib, smtplib, webbrowser, json, csv, sqlite3, pathlib, shutil, itertools, functools, dataclasses, collections, re, enum, time, datetime, random, argparse", globals())
                self.log("OCEAB FULL ENGINE LOADED.")
        except Exception as e:
            self.log(f"LOAD ERROR: {e}")

if __name__ == "__main__":
    app = OceabGUI()
    app.mainloop()
