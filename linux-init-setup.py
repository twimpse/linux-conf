#!/usr/bin/python3
import os
import subprocess
import re

print("Main Setup Starting")

bashrc_path = os.path.expanduser("~/.bashrc")
alias_line = "alias ls='ls --color=auto'"

try:
    with open(bashrc_path, 'r') as file:
        content = file.read()
        
        # Check for common ls alias patterns with color
        if "alias ls=" in content and "--color" in content:
            print("✓Found ls alias with color in .bashrc")
        else:
            print("No color alias found for ls in .bashrc")
            with open(bashrc_path, 'a') as file:
                file.write(f"{alias_line}  # Added by linux-conf\n")
            
except FileNotFoundError:
    print(f"File not found: {bashrc_path}")
except Exception as e:
    print(f"Error reading file: {e}")
