# Auto Save Monitor, and Quick Load Script

This script monitors your game save files and makes quick backups. You then can restore to the last backup if you press F8 at any time. Originally for a specific game (Jupiter Hell), but I quickly realized it would function for most games well enough. Theoretically this can be used on Mac and Linux as well, I just haven't tested it. The coding is KISS, keep it stupid simple. I've commented on most functionality. If you want to hack away at it, Go ahead, and have fun. If you have improved functionality. Send a pull request!

## How to Use
1. Ensure Python and the required modules are installed. Check `requirements.txt` for details. [Read More On Install](#installation)
2. Launch the game and the observer by running the provided batch file, or run `monitor.py` directly. [Read More On Running](#running-the-script)
3. Whenever a save file changes, a backup is created.
4. Press F8 to restore to the last saved backup file.

## Installation

So for the tool to propery function you'll need to install some dependancies before you can run the tool.
Run the following command to install the required modules

```sh
python.exe -m pip install -r requirements.txt
```

## Running The Script

You'll need to run the python script, and supply it with the save game location pattern at the very least. A more complete command would include the --exec which specifies where the game's launch executable is.

```sh
python.exe monitor.py save_location_pattern [--exec gameExe]
```

## Notes
- Keep `monitor.py` running while you play. It (should) shut down when the game does automatically.
- If restoring doesn't show a Load option in-game, you may need to reload or restart the game.

## Jupiter Hell
You can quick launch both the game and script by putting them in the game folder's directory and using `launch_jupiter_hell.bat`
As soon as you die in Jupiter Hell, press F8 before returning to the main menu so that the "Load Game" option remains available.
Otherwise, you'll need to exit the game and restart it to see the "Load Game" menu option again.

## Advanced Functionality
- You can specify multiple patterns when running monitor.py (e.g., "monitor.py save# save* save? save_game").
- The script supports directories and files, creating backups of either named "last_{item}".
- Only items with a single "last_" prefix are restored on F8 press to avoid nested backups.
- Wildcards can be used for flexible matching:
  - "#" matches digits. (Example: save# == save1 )
  - "?" matches a single character. (Example: save1? == save1a)
  - "\*" matches any sequence of characters. (Example: save* == save1a_24fdsff )
- An optional "--exec" parameter launches a specified executable (If not provided the script will attempt to find the largest EXE and use it).