import customtkinter as ctk
import os
import sys
import subprocess
import io
from contextlib import redirect_stdout


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class OceabGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OCEAB Interface v1.0.0")
        self.geometry("1000x700")

       
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
            rb.pack(pady=12, padx=20, anchor="w")

      
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.tab_console = self.tabview.add("Console")
        self.tab_editor = self.tabview.add("Script Creator")
        self.tab_files = self.tabview.add("Script Manager")

        self.setup_console_tab()
        self.setup_editor_tab()
        self.setup_files_tab()

   
    def setup_console_tab(self):
        self.console_output = ctk.CTkTextbox(self.tab_console, state="disabled", font=("Consolas", 13))
        self.console_output.pack(expand=True, fill="both", padx=5, pady=5)

        self.input_frame = ctk.CTkFrame(self.tab_console, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=5, pady=5)

        self.console_input = ctk.CTkEntry(self.input_frame, placeholder_text="Enter Python code or OCEAB commands...")
        self.console_input.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.console_input.bind("<Return>", lambda e: self.run_code())

        self.run_btn = ctk.CTkButton(self.input_frame, text="Execute", width=100, command=self.run_code)
        self.run_btn.pack(side="right")

        self.log("Welcome to OCEAB v1.0.0\nMathematical Computing Environment Active.\n" + "="*50)

   
    def setup_editor_tab(self):
        self.filename_entry = ctk.CTkEntry(self.tab_editor, placeholder_text="script_name.py")
        self.filename_entry.pack(fill="x", padx=20, pady=(10, 5))

        self.code_editor = ctk.CTkTextbox(self.tab_editor, font=("Consolas", 14), wrap="none")
        self.code_editor.pack(expand=True, fill="both", padx=20, pady=5)

        self.save_btn = ctk.CTkButton(self.tab_editor, text="Save to /scripts", command=self.save_script)
        self.save_btn.pack(pady=10)

    
    def setup_files_tab(self):
        self.file_scroll = ctk.CTkScrollableFrame(self.tab_files, label_text="Stored Scripts")
        self.file_scroll.pack(expand=True, fill="both", padx=20, pady=20)
        self.refresh_file_list()

    
    def log(self, message):
        self.console_output.configure(state="normal")
        self.console_output.insert("end", f"{message}\n")
        self.console_output.see("end")
        self.console_output.configure(state="disabled")

    def load_engine(self):
        choice = self.engine_var.get()
        self.log(f"OCEAB: Initializing Engine {choice}...")
        try:
            if choice == '1':
                global np, pd, plt, math, statistics
                import numpy as np, pandas as pd, matplotlib.pyplot as plt, math, statistics
                self.log("Engine 1 Loaded: numpy(np), pandas(pd), matplotlib(plt), math, statistics")
            elif choice == '2':
                global socket, http, urllib, smtplib, webbrowser
                import socket, http, urllib, smtplib, webbrowser
                self.log("Engine 2 Loaded: Networking and Web tools ready.")
            elif choice == '3':
                global json, csv, sqlite3, pathlib, shutil
                import json, csv, sqlite3, pathlib, shutil
                self.log("Engine 3 Loaded: File storage and SQLite tools ready.")
            elif choice == '4':
                global itertools, functools, dataclasses, collections, re, enum
                import itertools, functools, dataclasses, collections, re, enum
                self.log("Engine 4 Loaded: Advanced Dev tools ready.")
            elif choice == '5':
                global time, datetime, random, argparse, builtins
                import time, datetime, random, argparse, builtins
                self.log("Engine 5 Loaded: System utilities ready.")
            elif choice == '6':
                self.log("Engine 6: Loading Full Environment (Please wait...)")
                exec("import numpy as np, pandas as pd, matplotlib.pyplot as plt, math, statistics, socket, http, urllib, smtplib, webbrowser, json, csv, sqlite3, pathlib, shutil, itertools, functools, dataclasses, collections, re, enum, time, datetime, random, argparse, builtins", globals())
                self.log("FULL OCEAB ENGINE LOADED.")
        except Exception as e:
            self.log(f"Load Error: {e}")

    def run_code(self):
        user_input = self.console_input.get().strip()
        if not user_input: return
        
        self.console_input.delete(0, "end")
        
        
        if user_input == "clear()":
            self.console_output.configure(state="normal")
            self.console_output.delete("1.0", "end")
            self.console_output.configure(state="disabled")
            return
        
        self.log(f"OCEAB > {user_input}")
        
        try:
            f = io.StringIO()
            with redirect_stdout(f):
                exec(user_input, globals())
            out = f.getvalue()
            if out: self.log(out)
        except Exception as e:
            self.log(f"Error: {e}")

    def save_script(self):
        name = self.filename_entry.get().strip()
        if not name.endswith(".py"): name += ".py"
        content = self.code_editor.get("1.0", "end-1c")
        
        if not os.path.exists("scripts"): os.makedirs("scripts")
        with open(os.path.join("scripts", name), "w") as f:
            f.write(content)
        
        self.log(f"Script '{name}' saved successfully.")
        self.refresh_file_list()

    def refresh_file_list(self):
        for widget in self.file_scroll.winfo_children():
            widget.destroy()
        
        if not os.path.exists("scripts"): return
        
        for file in os.listdir("scripts"):
            if file.endswith(".py"):
                frame = ctk.CTkFrame(self.file_scroll)
                frame.pack(fill="x", pady=2, padx=5)
                
                ctk.CTkLabel(frame, text=file, width=200, anchor="w").pack(side="left", padx=10)
                ctk.CTkButton(frame, text="Run", width=60, fg_color="green", 
                              command=lambda f=file: self.run_external_script(f)).pack(side="right", padx=5)

    def run_external_script(self, filename):
        path = os.path.join("scripts", filename)
        self.log(f"--- Launching {filename} ---")
        try:
            result = subprocess.run([sys.executable, path], capture_output=True, text=True)
            if result.stdout: self.log(result.stdout)
            if result.stderr: self.log(f"STDERR: {result.stderr}")
        except Exception as e:
            self.log(f"Execution Error: {e}")
        self.log("--- Finished ---")

if __name__ == "__main__":
    app = OceabGUI()
    app.mainloop()
