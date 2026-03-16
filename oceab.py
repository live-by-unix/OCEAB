import os 
import sys

oceab_welcome = """
Welcome to OCEAB v1.0.0, the open-source cross-platform mathematical computing environment.
Built on top of Python, OCEAB provides a powerful platform for data analysis and research."""

print(oceab_welcome)
module_menu = """
--- OCEAB MODULE SELECTOR ---
[1] MATH & DATA    : numpy, pandas, matplotlib, math, statistics
[2] WEB & NETWORK  : socket, http, urllib, smtplib, webbrowser
[3] STORAGE & FILES: json, csv, sqlite3, pathlib, shutil
[4] DEV TOOLS      : itertools, functools, dataclasses, collections, re, enum
[5] UTILITIES      : subprocess, time, datetime, random, argparse, builtins
[6] LOAD ALL       : Load everything, will be slow
-----------------------------
"""
print("Before you can start calculating, please choose a engine to load for OCEAB.")
print()
print(module_menu)
print()
choice = input("Choose the number 1-6, or press enter to load NO EXTRA libs but os and sys which are used by oceab but freely useable for users").strip()
if choice == '1':
    print("Loading math engine, numpy as np, pandas as pd and matplotlib.pyplot as plt")
    import numpy as np, pandas as pd, matplotlib.pyplot as plt
    import math, statistics
elif choice == '2':
    print("Loading web and networking engine")
    import socket, http, urllib, smtplib, webbrowser
elif choice == '3':
    print("Loading storage and files engine")
    import json, csv, sqlite3, pathlib, shutil
elif choice == '4':
    print("Loading dev tools engine")
    import itertools, functools, dataclasses, collections, re, enum
elif choice == '5':
    print("Loading utilities engine")
    import subprocess, time, datetime, random, argparse, builtins
elif choice == '6':
    print("Loading full engine, numpy as np, pandas as pd and matplotlib.pyplot as plt")
    import shutil, json, pathlib, subprocess, builtins, webbrowser, random
    import argparse, statistics, math, datetime, csv, sqlite3, socket, http
    import smtplib, re, enum, time, functools, urllib, itertools, dataclasses
    import collections, numpy as np, pandas as pd
    import matplotlib.pyplot as plt
else:
    print("Loading nothing, however OCEAB libs (sys and os) shall still be callable"),strip()   
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