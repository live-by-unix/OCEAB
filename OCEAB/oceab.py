import sys, shutil, os, json, pathlib, subprocess, builtins, webbrowser
import random, argparse, statistics, math, datetime, csv, sqlite3, socket 
import http, smtplib, re, enum, time, functools, urllib, itertools, dataclasses, collections
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

oceab_welcome = """
Welcome to OCEAB v1.0.0, the open-source cross-platform mathematical computing environment.
Built on top of Python, OCEAB provides a powerful platform for data analysis and research."""

print(oceab_welcome)
print("Type 'help()' to understand how to use OCEAB and its features.")

help_message = """ 
--- OCEAB HELP GUIDE ---
OCEAB is a wrapper around python including pandas (pd), matplotlib.pyplot (plt), and numpy (np).

COMMANDS:
- dedicated() : Create a new .py script. Type your code and press ENTER on an EMPTY LINE to save.
- run()       : Execute a saved script from the /scripts folder.
- clear()     : Clear the terminal screen.
- exit        : Close the OCEAB environment.

DIRECT EXECUTION:
- You can paste or type Python code directly into the prompt.
- For multi-line code (like 'if' statements or loops), keep typing. 
- To EXECUTE, press ENTER on an EMPTY LINE.
"""

while True:
    user_input = input("\nOCEAB > ")

    if not user_input.strip():
        continue

    if user_input == 'exit':
        print("Exiting OCEAB. Goodbye!")
        break 
        
    elif user_input == 'help()':
        print(help_message)

    elif user_input == 'clear()':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(oceab_welcome) 
        
    elif user_input == 'dedicated()':
        user_filename = input("Enter the filename (e.g., myscript.py): ")
        print("Enter/Paste your code. Press ENTER on an EMPTY LINE to save and exit.")
        
        code_lines = []
        while True:
            line = input("... ")
            if line == "": 
                break
            code_lines.append(line)
        
        user_code = "\n".join(code_lines)
        subfolder = "scripts" 

        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        target_path = os.path.join(subfolder, user_filename)
        
        with open(target_path, "w") as f:
            f.write(user_code)
        print(f"Successfully saved to {target_path}")
        
    elif user_input == 'run()':
        target_file = input("Enter the exact filename to run (e.g., script.py): ")
        subfolder = "scripts" 
        full_script_path = os.path.join(subfolder, target_file)
        
        if os.path.exists(full_script_path):
            print(f"--- Launching {target_file} ---")
            subprocess.run([sys.executable, full_script_path])
            print("--- Finished ---")
        else:
            print(f"Error: {target_file} not found in {subfolder} folder.")
            
    else:
        code_block = [user_input]
        
       
        if user_input.strip().endswith(':') or user_input.strip().startswith(('def ', 'for ', 'if ', 'while ')):
            while True:
                line = input("... ")
                if line == "": 
                    break
                code_block.append(line)
        
        final_code = "\n".join(code_block)
        
        try:
            exec(final_code)
        except Exception as e:
            print(f"Error: {e}")