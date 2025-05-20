import time
import json
import argparse
import os
from datetime import datetime
from pynput import mouse as pynput_mouse
import pyautogui
import mouse
import keyboard
import ctypes
import tkinter as tk
from tkinter import Canvas, Label

screen_width, screen_height = pyautogui.size()

print(f"Screen size: {screen_width}x{screen_height}")