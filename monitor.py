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
import argparse

is_saving = False
path_to_watch = os.path.dirname(os.path.abspath(__file__))

#####################
# Parse arguments for patterns and an optional --exec
#####################
def parse_args():
    parser = argparse.ArgumentParser(description="Monitor save files and launch a game.")
    parser.add_argument("patterns", nargs="*", help="Filename patterns (use '#' to match digits, or '*' to match all).")
    parser.add_argument("--exec", dest="exe", help="Path to the executable.")
    return parser.parse_args()

#####################
# Transform any pattern with '#' into a regex (e.g., 'save#' -> 'save\\d+')
#####################
def transform_pattern(pattern):
    # Replace all '#' with '\d+'
    if "#" in pattern:
        pattern = pattern.replace("#", "\\d+")

    # Replace all '?' with '.' for single-character matches
    if "?" in pattern:
        # This will match exactly one character
        pattern = pattern.replace("?", ".")

    # Replace '*' with '.*'
    if pattern == "*":
        pattern = ".*"

    return pattern  # If nothing matched, treat as literal

#####################
# Helper to check if a filename matches any pattern
#####################
def matches_any_pattern(filename, compiled_patterns):
    for pat in compiled_patterns:
        if pat.match(filename):
            return True
    return False

#####################
# Find the largest .exe in the current folder if no --exec is specified
#####################
def find_largest_exe(folder):
    largest_file = None
    largest_size = 0
    for f in os.listdir(folder):
        if f.lower().endswith(".exe"):
            size = os.path.getsize(os.path.join(folder, f))
            if size > largest_size:
                largest_size = size
                largest_file = f
    return os.path.join(folder, largest_file) if largest_file else None

#####################
# The event handler reacts to file changes or creations
#####################
class ChangeHandler(FileSystemEventHandler):
    def backup_on_change(self, event, is_created=False):
        global is_saving
        if is_saving:
            return
        name = os.path.basename(event.src_path)
        # Skip already-backed-up items
        if name.startswith("last_"):
            return
        if matches_any_pattern(name, compiled_patterns):
            action = "Created" if is_created else "Modified"
            print(f"{action}: {name}")
            backup_path = os.path.join(os.path.dirname(event.src_path), f"last_{name}")
            if os.path.isdir(event.src_path):
                if os.path.exists(backup_path) and os.path.isdir(backup_path):
                    shutil.rmtree(backup_path)
                shutil.copytree(event.src_path, backup_path)
            else:
                shutil.copyfile(event.src_path, backup_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.backup_on_change(event, is_created=False)

    def on_created(self, event):
        if not event.is_directory:
            self.backup_on_change(event, is_created=True)

#####################
# This function restores the last copied saves when triggered
#####################
def restore_saves(path):
    global is_saving
    is_saving = True
    print("Restoring To Last Save")

    for f in os.listdir(path):
        # Only restore if starts with 'last_' and no extra 'last_' inside the rest of the name
        if f.startswith("last_") and "last_" not in f[5:]:
            original = f[5:]
            if matches_any_pattern(original, compiled_patterns):
                backup = os.path.join(path, f)
                original_path = os.path.join(path, original)
                print(f"Restoring: {original}")
                if os.path.isdir(backup):
                    if os.path.isdir(original_path):
                        shutil.rmtree(original_path)
                    shutil.copytree(backup, original_path)
                else:
                    if os.path.exists(original_path):
                        os.remove(original_path)
                    shutil.copyfile(backup, original_path)
    
    # Let the script pause a bit before resuming
    time.sleep(1)
    is_saving = False

#####################
# Main
#####################
if __name__ == "__main__":
    args = parse_args()
    # print(args)

    #####################
    # Exit if no patterns are provided
    #####################
    if not args.patterns:
        print("No filename patterns specified. Exiting.")
        exit(1)

    # Compile provided patterns or use a default if none are given
    compiled_patterns = [re.compile(transform_pattern(p)) for p in args.patterns]

    # Determine which exe to launch
    if args.exe:
        path_to_exe = os.path.join(path_to_watch, args.exe)
    else:
        path_to_exe = find_largest_exe(path_to_watch)

    #####################
    # Start monitoring the directory for save file changes
    #####################
    observer = Observer()
    observer.schedule(ChangeHandler(), path=path_to_watch, recursive=True)
    observer.start()
    print(f"Monitoring directory: {path_to_watch}")

    #####################
    # Launch the process
    #####################
    if path_to_exe and os.path.exists(path_to_exe):
        process = subprocess.Popen([path_to_exe])
        print(f"Launching {path_to_exe}")
    else:
        print("No valid executable found or provided.")
        print("Ensure this script is in the correct folder or you specify the --exec argument.")
        exit()

    #####################
    # Listen for F8 presses to restore saves on demand
    #####################
    keyboard.on_press_key('f8', lambda _: restore_saves(path_to_watch))

    #####################
    # Wait for the game to exit and clean up
    #####################
    try:
        process.wait() # Wait for the game to exit
    except KeyboardInterrupt:
        observer.stop()
        process.terminate()

    observer.join()
