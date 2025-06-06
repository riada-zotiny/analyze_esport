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

def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def countdown_animation(root):
    canvas = Canvas(root, width=screen_width, height=screen_height, bg="white", highlightthickness=0)
    canvas.pack()
    countdown_label = Label(canvas, text="", font=("Hellvetica", 16, "bold"), fg="black")
    countdown_label.place(relx=0.5, rely=0.5, anchor="center")
    if root.mode == "record":
        countdown_label.config(text="Enregistrement de Souris et de Clavier")
    elif root.mode == "replay":
        countdown_label.config(text="Relancement des actions")
    root.update()
    time.sleep(1)
    canvas.destroy()

def count_down_animation_config(mode):
    print(f"{mode.capitalize()} will start in:")
    root = tk.Tk()
    root.attributes("-transparentcolor", "white")
    root.overrideredirect(1)
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.attributes('-topmost', 1)
    root.mode = mode
    countdown_animation(root)
    root.withdraw()

def get_next_filename(base_dir="dataMouseKeybord", base_name="mouse_keyboard_actions"):
    today = datetime.now().strftime("%Y-%m-%d")
    i = 1
    while True:
        filename = f"{base_name}_{today}_num{i}.json"
        full_path = os.path.join(base_dir, filename)
        if not os.path.exists(full_path):
            return filename
        i += 1

def record(should_stop_callback=lambda: False, filename=None):
    count_down_animation_config("record")
    print("Recording started. Move the mouse around, perform actions, and type on the keyboard.")

    actions = []
    previous_time = time.time()
    time_diff_container = [0]

    def on_move(x, y):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "move",
                "position": (x, y),
                "time_diff": time_diff_container[0],
                "timestamp": datetime.now().isoformat()
            })

    def on_click(x, y, button, pressed):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "press" if pressed else "release",
                "button": str(button),
                "position": (x, y),
                "time_diff": time_diff_container[0],
                "timestamp": datetime.now().isoformat(),
            })        



    def on_scroll(x, y, dx, dy):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "scroll",
                "position": (x, y),
                "scroll": dy,
                "time_diff": time_diff_container[0],
                "timestamp": datetime.now().isoformat()
            })

    def on_key_event(event):
        actions.append({
            "action": "key",
            "key": event.name,
            "event_type": event.event_type,
            "time_diff": time_diff_container[0],
            "timestamp": datetime.now().isoformat()
        })

    listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    listener.start()
    keyboard.hook(on_key_event)

    if filename is None:
        filename = get_next_filename()
    path = os.path.join("dataMouseKeybord", filename)

    try:
        while not should_stop_callback():
            current_time = time.time()
            time_diff_container[0] = current_time - previous_time
            previous_time = current_time
            x, y = mouse.get_position()
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))

            set_cursor_pos(x, y)
            time.sleep(0.05)  # FAIRE ATTETION POUR POUVOIR  VOIR LE TEMPS ECOULE !
    finally:
        listener.stop()
        keyboard.unhook_all()
        os.makedirs("dataMouseKeybord", exist_ok=True)
        with open(path, 'w') as file:
            json.dump(actions, file, indent=2)
        print(f"Actions saved to: {path}")
        return filename
def replay(filename, key_delay=0.1, on_finish=None):
    count_down_animation_config("replay")
    with open("dataMouseKeybord/" + filename, 'r') as file:
        actions = json.load(file)
        print("Replaying mouse movements and keyboard inputs...")

        last_click_time = 0
        double_click_threshold = 0.3

        for action in actions:
            if action["action"] == "move":
                mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.00001)

            elif action["action"] == "press":
                current_time = action["time_diff"]
                if current_time - last_click_time <= double_click_threshold:
                    if action["button"] == "Button.left":
                        pyautogui.mouseDown(button='left')
                        print("double click")
                    elif action["button"] == "Button.right":
                        pyautogui.mouseDown(button='right')
                        print("double right click")
                else:
                    if action["button"] == "Button.left":
                        pyautogui.mouseDown(button='left')
                        print("holding mode")
                    elif action["button"] == "Button.right":
                        pyautogui.mouseDown(button='right')
                        print("holding right mode")

                last_click_time = current_time

            elif action["action"] == "release":
                if action["button"] == "Button.left":
                    pyautogui.mouseUp(button='left')
                    print("normal click")
                elif action["button"] == "Button.right":
                    pyautogui.mouseUp(button='right')
                    print("normal right click")

            elif action["action"] == "scroll":
                time.sleep(0.01)
                mouse.wheel(delta=action["scroll"])

            elif action["action"] == "key":
                if action["event_type"] == "down":
                    keyboard.press(action["key"])
                    print(f"Key pressed: {action['key']}")
                elif action["event_type"] == "up":
                    keyboard.release(action["key"])
                    print(f"Key released: {action['key']}")
                time.sleep(key_delay)

        print("Replay complete.")
        if on_finish:
            on_finish()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mouse and Keyboard Recorder/Replayer')
    parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
    parser.add_argument('--file', help='File to replay from (only for replay mode)')
    args = parser.parse_args()

    if args.command == 'record':
        record()
    elif args.command == 'replay':
        if args.file:
            replay(args.file)
        else:
            print("Please provide a --file argument for replay mode.")
