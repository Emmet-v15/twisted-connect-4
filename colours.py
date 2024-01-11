#!/usr/bin/env python

"""
    18/11/2023
    Programming Fundamentals - Assessment 1 - Colours module

    General Styling: https://peps.python.org/pep-0008/
    Docstring format: https://peps.python.org/pep-0257/
"""

__author__ = "Emmet Noman"
__email__ = "27587991@students.lincoln.ac.uk"

import sys

# ANSI color codes
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
RESET = "\033[0m"

if "idlelib.run" in sys.modules: # In idle, the colour codes do not function.
    print("Python IDLE is not a production environment, it is for development and testing.")
    print("Please use a different enviornment.")
    sys.exit() # Remove this if you want to see what breaks.
else:
    # Enable color codes to work in command prompt, if you are using an ansi-enabled terminal e.g. vscode integrated terminal, this is not necessary.
    sys.modules['os'].system('')


# Colour definitions, each of these make the string colour, and then reset the color to default.
def lime(string):
    return LIGHT_GREEN + str(string) + RESET

def red(string):
    return LIGHT_RED + str(string) + RESET

def yellow(string):
    return YELLOW + str(string) + RESET

def dark_gray(string):
    return DARK_GRAY + str(string) + RESET

def underline(string):
    return UNDERLINE + str(string) + RESET

def light_purple(string):
    return LIGHT_PURPLE + str(string) + RESET
