# Jupiter Hell Auto Save Monitor

This script monitors your Jupiter Hell save files and makes quick backups by copying them to "last_{filename}".  
It also restores to the last backup if you press F8 at any time while the script is running.

To trigger a manual save, open the Jupiter Hell menu and select "Save and Exit." You can then load the new save file to rejoin your game.

Press F8 before returning to the main menu when you die so the "Load Game" option is still visible.  
If it's not shown, exit the game and restart to make the "Load Game" option appear in the main menu.

## How to Use
1. Ensure you have Python and the required modules installed. Check `requirements.txt` for details.
2. Launch the game and the observer by running `launch_game.bat`.  
   - Alternatively, run `monitor.py` directly if you prefer a Python command line.
3. Play Jupiter Hell as normal. Whenever a save file changes, a "last_" backup is created.
4. Press F8 to restore the last saved file.

## Notes
- Keep `monitor.py` running while Jupiter Hell is running.