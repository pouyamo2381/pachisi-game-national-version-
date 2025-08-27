# Pachisi Game

A modern recreation of the traditional Pachisi board game, built with **Python** and **Pygame**.  
This is my first complete game project (2025). It includes multiple national teams, sound effects, saving & loading, and different difficulty levels.

---

## Features
- Single-player gameplay with AI (Easy / Medium / Hard)
- 48 National Teams to choose from
- Different board themes and background options
- Save & Load game state
- Sound effects (with mute/unmute option)
- Settings menu (difficulty, fullscreen, sound toggle)
- Windowed or fullscreen modes

---

## Project Structure
- `pachisi_game.py` -> Main game file (all-in-one for simplicity)  
- `assets/` -> contains images, sounds, fonts, etc.  
  - `assets/sounds/`  
  - `assets/images/`

---

## How to Run
1. Install requirements:
   ```bash
   pip install pygame
2. Run the game:
  python pachisi_game.py
3. Build Executable
  You can create a .exe version using [PyInstaller]:
    pyinstaller --onefile --windowed pachisi_game.py

## Notes
- This is my first official project uploaded on GitHub.
- The game is focused on single-player mode for now.
- Online multiplayer and tournament modes may be added in future versions.

## Author
Created by Pouya Motallebi (Peter Smith), 2025
Contact: pouyam81@outlook.com / pouyamo2002@gmail.com
