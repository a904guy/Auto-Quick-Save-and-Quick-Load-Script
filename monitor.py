#!/usr/bin/env python

#####################
# Try importing watchdog and define fallback if not installed
#####################
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("The 'watchdog' module is required. Install with 'pip install watchdog'")
    exit()

#####################
# Try importing keyboard and define fallback if not installed
#####################
try:
    import keyboard
except ImportError:
    print("The 'keyboard' module is required. Install with 'pip install keyboard'")
    exit()

import time
import os, re, shutil
import subprocess

is_saving = False
path_to_watch = os.path.dirname(os.path.abspath(__file__))
path_to_exe = os.path.join(path_to_watch, "jh.exe")

#####################
# The event handler reacts to file changes or creations
#####################
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global is_saving
        if not event.is_directory and not is_saving:
            filename = os.path.basename(event.src_path)
            # If this is a save file, back it up immediately
            if re.match(r"save\d+", filename) or filename == "default.rec":
                print(f"Modified: {filename}")
                shutil.copyfile(event.src_path, os.path.join(os.path.dirname(event.src_path), f"last_{filename}"))

    def on_created(self, event):
        global is_saving
        if not event.is_directory and not is_saving:
            filename = os.path.basename(event.src_path)
            # For newly created save files, also make a backup
            if re.match(r"save\d+", filename) or filename == "default.rec":
                print(f"Created: {filename}")
                shutil.copyfile(event.src_path, os.path.join(os.path.dirname(event.src_path), f"last_{filename}"))

#####################
# This function restores the last copied saves when triggered
#####################
def restore_saves(path):
    global is_saving
    is_saving = True
    print("Restoring To Last Save")
    # Copy saved data from backups
    for f in os.listdir(path):
        if re.match(r"last_save\d+", f) or f == "last_default.rec":
            suffix = f[5:]  # remove "last"
            print("Restoring: " + suffix)
            shutil.copyfile(
                os.path.join(path, f),
                os.path.join(path, suffix)
            )
    # Let the script pause a bit before resuming
    time.sleep(1)
    is_saving = False

#####################
# Start monitoring the directory for save file changes
#####################
observer = Observer()
observer.schedule(ChangeHandler(), path=path_to_watch, recursive=True)
observer.start()
print(f"Monitoring directory: {path_to_watch}")

#####################
# Launch Jupiter Hell and monitor its process
#####################
process = subprocess.Popen([path_to_exe])
print("Launching Jupiter Hell")

#####################
# Listen for F8 presses to restore saves on demand
#####################
keyboard.on_press_key('f8', lambda _: restore_saves(path_to_watch))

#####################
# Wait for Jupiter Hell to exit and clean up
#####################
try:
    process.wait() # Wait for Jupiter Hell to exit
    exit()
except KeyboardInterrupt:
    observer.stop()
    process.terminate()

observer.join()
