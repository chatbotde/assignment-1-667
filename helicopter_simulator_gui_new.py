#!/usr/bin/env python3
"""
Helicopter Flight Simulator GUI - Modular Version
Entry point for the modular helicopter simulator GUI
"""

import tkinter as tk
import sys
import os

# Add GUI path
sys.path.append('.')

from gui.helicopter_gui_main import main

if __name__ == "__main__":
    main()