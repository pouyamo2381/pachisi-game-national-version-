# Pachisi Game

A modern recreation of the traditional Pachisi board game, built with **Python** and **Pygame**.  
This is my first complete game project (2025-2026). It includes multiple national teams, sound effects, saving & loading, and different difficulty levels.

---

## Features
- Single-player gameplay with AI (Easy / Medium / Hard)
- 64 National Teams to choose from
- Different board themes and background options
- Save & Load game state
- Sound effects (with mute/unmute option)
- Settings menu (difficulty, fullscreen, sound toggle)
- Windowed or fullscreen modes
- Full Tournament mode with brackets and group stage

---

## Project Structure
- `game.py` -> Main game file: board rendering, game loop, UI screens, AI move logic
- `tournament.py` -> Tournament bracket engine (groups, advancement, round naming)
- `match_simulation.py` -> Headless match engine used to auto-resolve simulated matches
- `save_load.py` -> Save/load serialization for game state
- `assets/`
  - `sounds/` -> dice_roll.wav, piece_move.wav, piece_cut.wav, game_win.wav
---

## How to Run
1. Install requirements:
   ```bash
   pip install pygame
2. Run the game:
  python game.py
3. Build Executable
  You can create a .exe version using [PyInstaller]:
    pyinstaller --onefile --windowed pachisi_game.py

## Notes
- This is my first official project uploaded on GitHub.
- The game is focused on single-player mode for now.
- Online multiplayer and tournament modes may be added in future versions.

## Author
Created by Pouya Motallebi (Peter Smith), 2025-2026
Contact: pouyam81@outlook.com / pouyamo2002@gmail.com
