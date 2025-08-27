#Created by Pouya Motallebi (Peter Smith), 2025
import pygame
import random
import os
import math
import sys

from save_load import save_game, load_game

# PyInstaller Path Fix
if getattr(sys, 'frozen', False):
    # The application is frozen (e.g., in an .exe)
    application_path = sys._MEIPASS
else:
    # The application is not frozen
    application_path = os.path.dirname(__file__)
# End PyInstaller Path Fix

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up Display Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = None
pygame.display.set_caption(f"Pachisi Game")

# Define colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 128, 0)  # Background green for the board area
PATH_COLOR = (240, 240, 240)
SAFE_COLOR = (180, 180, 180)
HOME_COLOR = (100, 100, 100)

# Base colors
RED_BASE_COLOR = (200, 0, 0)
BLUE_BASE_COLOR = (0, 0, 200)
YELLOW_BASE_COLOR = (200, 200, 0)
ORANGE_BASE_COLOR = (255, 165, 0)

# Extra custom shades
LIGHT_YELLOW = (255, 255, 150)
MAROON = (128, 0, 32)
LIGHT_GREEN = (150, 255, 150)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 100, 0)
ARGENTINA_BLUE = (135, 206, 250)
LIGHT_BLUE = (173, 216, 230)
NAVY_BLUE = (0, 0, 139)
PURE_RED = (255, 0, 0)
NORWAY_RED = (200, 0, 0)
AQUA = (0, 255, 255)
TURQUOISE = (64, 224, 208)
DARK_RED = (139, 0, 0)
CRIMSON = (220, 20, 60)
GOLD = (255, 215, 0)

# Country Data (48 teams, alphabetically sorted)
ALL_COUNTRIES_DATA = [
    {"id": 0, "name": "Algeria", "color": DARK_GREEN},
    {"id": 1, "name": "Argentina", "color": ARGENTINA_BLUE},
    {"id": 2, "name": "Australia", "color": YELLOW_BASE_COLOR},
    {"id": 3, "name": "Austria", "color": CRIMSON},
    {"id": 4, "name": "Brazil", "color": GOLD},
    {"id": 5, "name": "Cambodia", "color": DARK_BLUE},
    {"id": 6, "name": "Canada", "color": PURE_RED},
    {"id": 7, "name": "Chile", "color": RED_BASE_COLOR},
    {"id": 8, "name": "China", "color": PURE_RED},
    {"id": 9, "name": "Czech Republic", "color": GRAY},
    {"id": 10, "name": "Denmark", "color": DARK_RED},
    {"id": 11, "name": "Ecuador", "color": YELLOW_BASE_COLOR},
    {"id": 12, "name": "Egypt", "color": MAROON},
    {"id": 13, "name": "Estonia", "color": LIGHT_BLUE},
    {"id": 14, "name": "Finland", "color": AQUA},
    {"id": 15, "name": "France", "color": BLUE_BASE_COLOR},
    {"id": 16, "name": "Germany", "color": GRAY},
    {"id": 17, "name": "India", "color": ORANGE_BASE_COLOR},
    {"id": 18, "name": "Iran", "color": WHITE},
    {"id": 19, "name": "Ireland", "color": LIGHT_GREEN},
    {"id": 20, "name": "Israel", "color": LIGHT_BLUE},
    {"id": 21, "name": "Italy", "color": BLUE_BASE_COLOR},
    {"id": 22, "name": "Japan", "color": BLUE_BASE_COLOR},
    {"id": 23, "name": "Kazakhstan", "color": LIGHT_YELLOW},
    {"id": 24, "name": "Mexico", "color": DARK_GREEN},
    {"id": 25, "name": "Morocco", "color": DARK_RED},
    {"id": 26, "name": "Nepal", "color": WHITE},
    {"id": 27, "name": "Netherlands", "color": ORANGE_BASE_COLOR},
    {"id": 28, "name": "New Zealand", "color": NAVY_BLUE},
    {"id": 29, "name": "Nigeria", "color": GREEN},
    {"id": 30, "name": "Norway", "color": NORWAY_RED},
    {"id": 31, "name": "Panama", "color": DARK_BLUE},
    {"id": 32, "name": "Poland", "color": WHITE},
    {"id": 33, "name": "Portugal", "color": CRIMSON},
    {"id": 34, "name": "Saudi Arabia", "color": DARK_GREEN},
    {"id": 35, "name": "South Africa", "color": GOLD},
    {"id": 36, "name": "South Korea", "color": RED_BASE_COLOR},
    {"id": 37, "name": "Spain", "color": ORANGE_BASE_COLOR},
    {"id": 38, "name": "Sweden", "color": YELLOW_BASE_COLOR},
    {"id": 39, "name": "Switzerland", "color": RED_BASE_COLOR},
    {"id": 40, "name": "Tajikistan", "color": WHITE},
    {"id": 41, "name": "Thailand", "color": DARK_BLUE},
    {"id": 42, "name": "Tunisia", "color": RED_BASE_COLOR},
    {"id": 43, "name": "Turkey", "color": PURE_RED},
    {"id": 44, "name": "Turkmenistan", "color": GREEN},
    {"id": 45, "name": "UAE", "color": DARK_GREEN},
    {"id": 46, "name": "UK", "color": CRIMSON},
    {"id": 47, "name": "USA", "color": BLUE_BASE_COLOR},
    {"id": 48, "name": "Uruguay", "color": AQUA}
]

# Map player IDs to their colors for easier lookup (THIS WILL BE DYNAMICALLY SET)
PLAYER_COLORS = {}

# Board Configuration 
BOARD_CELLS_PER_SIDE = 15
CELL_SIZE = 40
BOARD_PIXEL_SIZE = BOARD_CELLS_PER_SIDE * CELL_SIZE

# Adjust BOARD_START_X to leave space on the LEFT for UI
UI_PANEL_WIDTH = 250
BOARD_START_X = UI_PANEL_WIDTH + (SCREEN_WIDTH - UI_PANEL_WIDTH - BOARD_PIXEL_SIZE) // 2 # Board starts after UI panel, centered in remaining space
BOARD_START_Y = (SCREEN_HEIGHT - BOARD_PIXEL_SIZE) // 2

# Helper function to convert board (row, col) to pixel coordinates
def get_pixel_coords(row, col):
    x = BOARD_START_X + col * CELL_SIZE
    y = BOARD_START_Y + row * CELL_SIZE
    return x, y

# Helper for pixel coordinates of piece center
def get_piece_center_pixel_coords(row, col):
    x, y = get_pixel_coords(row, col)
    return x + CELL_SIZE // 2, y + CELL_SIZE // 2

# Define Board Layout 
RED_HOME_CELLS = [(11, 2), (11, 3), (12, 2), (12, 3)]
BLUE_HOME_CELLS = [(2, 11), (2, 12), (3, 11), (3, 12)]
YELLOW_HOME_CELLS = [(11, 11), (11, 12), (12, 11), (12, 12)]
ORANGE_HOME_CELLS = [(2, 2), (2, 3), (3, 2), (3, 3)]

PLAYER_HOME_CELLS_LAYOUT = {
    0: RED_HOME_CELLS,
    1: BLUE_HOME_CELLS,
    2: YELLOW_HOME_CELLS,
    3: ORANGE_HOME_CELLS
}

RED_START_SQUARE = (13, 6)
BLUE_START_SQUARE = (1, 8)
YELLOW_START_SQUARE = (8, 13)
ORANGE_START_SQUARE = (6, 1)

PLAYER_START_SQUARES = {
    0: RED_START_SQUARE,
    1: BLUE_START_SQUARE,
    2: YELLOW_START_SQUARE,
    3: ORANGE_START_SQUARE
}

# Main path, starting from Red's entry (6,1) and going clockwise
main_path_ordered = [
    (6, 1), (6, 2), (6, 3), (6, 4), (6, 5),
    (5, 6), (4, 6), (3, 6), (2, 6), (1, 6),
    (0, 6), (0, 7), (0, 8),
    (1, 8), (2, 8), (3, 8), (4, 8), (5, 8),
    (6, 9), (6, 10), (6, 11), (6, 12), (6, 13),
    (6, 14), (7, 14), (8, 14),
    (8, 13), (8, 12), (8, 11), (8, 10), (8, 9),
    (9, 8), (10, 8), (11, 8), (12, 8), (13, 8),
    (14, 8), (14, 7), (14, 6),
    (13, 6), (12, 6), (11, 6), (10, 6), (9, 6),
    (8, 5), (8, 4), (8, 3), (8, 2), (8, 1),
    (8, 0), (7, 0), (6, 0)
]

SAFE_SQUARES = [
    (13, 6), # Red's start
    (1, 8), # Blue's start
    (8, 13), # Yellow's start
    (6, 1), # Orange's start
    (1, 6), # Top-left star
    (6, 13), # Top-right star
    (13, 8), # Bottom-right star
    (8, 1)  # Bottom-left star
]

RED_FINAL_PATH = [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7), (7, 7)]
BLUE_FINAL_PATH = [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
YELLOW_FINAL_PATH = [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7)]
ORANGE_FINAL_PATH = [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]

PLAYER_FINAL_PATHS = {
    0: RED_FINAL_PATH,
    1: BLUE_FINAL_PATH,
    2: YELLOW_FINAL_PATH,
    3: ORANGE_FINAL_PATH
}

# The entry point on the main_path_ordered that leads to a player's final path
PLAYER_FINAL_PATH_ENTRY_POINTS = {
    0: (14, 7), # Cell (7,0) is immediately before Red's final path (7,1)
    1: (0, 7), # Cell (0,7) is immediately before Blue's final path (1,7)
    2: (7, 14),# Cell (7,14) is immediately before Yellow's final path (7,13)
    3: (7, 0) # Cell (14,7) is immediately before Orange's final path (13,7)
}

CENTER_HOME_SQUARE = (7, 7)

# Piece animation speed constant (now represents time per *single cell* move)
PIECE_ANIMATION_DURATION_MS = 150 # How long in milliseconds a piece takes to move one cell/step
MIN_ANIMATION_DURATION_TOTAL_MS = 200 # Minimum total duration for a move, even if 1 step

# Dice animation constants
DICE_ANIMATION_DURATION_MS = 700  # Total time the dice rolls before showing final value
DICE_ANIMATION_FRAME_RATE_MS = 50 # How often the random number on the dice changes during animation

# Sound Effects
SOUNDS = {}

save_notification = ""
save_notification_time = 0

# Globals
is_muted = False

def load_sounds():
    global SOUNDS
    try:
        SOUNDS['dice_roll'] = pygame.mixer.Sound(os.path.join(application_path, 'assets','sounds', 'dice_roll.wav'))
        SOUNDS['piece_move'] = pygame.mixer.Sound(os.path.join(application_path, 'assets','sounds', 'piece_move.wav'))
        SOUNDS['piece_cut'] = pygame.mixer.Sound(os.path.join(application_path, 'assets','sounds', 'piece_cut.wav'))
        SOUNDS['game_win'] = pygame.mixer.Sound(os.path.join(application_path, 'assets','sounds', 'game_win.wav'))
        print("Sounds loaded successfully!")
    except pygame.error as e:
        print(f"Error loading sound: {e}. Make sure sound files are in the 'sounds' folder.")
        # Create dummy sound objects to prevent crashes if files are missing
        SOUNDS['dice_roll'] = pygame.mixer.Sound(pygame.sndarray.make_sound([[0]])) # Silence
        SOUNDS['piece_move'] = pygame.mixer.Sound(pygame.sndarray.make_sound([[0]]))
        SOUNDS['piece_cut'] = pygame.mixer.Sound(pygame.sndarray.make_sound([[0]]))
        SOUNDS['game_win'] = pygame.mixer.Sound(pygame.sndarray.make_sound([[0]]))

load_sounds()

all_sounds = [
    SOUNDS['dice_roll'],
    SOUNDS['piece_move'],
    SOUNDS['piece_cut'],
    SOUNDS['game_win']
]


# Piece Class
class Piece:
    def __init__(self, player_id, piece_id, initial_pos):
        self.player_id = player_id
        self.piece_id = piece_id
        self.logical_pos = initial_pos
        self.current_pos = initial_pos

        self.color = PLAYER_COLORS[player_id]
        
        # Animation state variables
        self.is_animating = False
        self.animation_start_time = 0
        self.animation_path = []
        self.last_sound_path_index = -1

        self.in_base = True
        self.on_path = False
        self.in_final_path = False
        self.is_home = False
        self.steps_on_main_path = -1
        self.steps_on_final_path = -1
        self.highlight = False

    def draw(self, surface):
        if self.is_home:
            return

        draw_row, draw_col = self.current_pos
        pixel_x, pixel_y = get_pixel_coords(draw_row, draw_col)

        center_x = pixel_x + CELL_SIZE // 2
        center_y = pixel_y + CELL_SIZE // 2

        piece_radius = CELL_SIZE // 3
        
        if self.highlight:
            highlight_radius = piece_radius + 5
            highlight_color = (255, 255, 0)
            pygame.draw.circle(surface, highlight_color, (center_x, center_y), highlight_radius)

        pygame.draw.circle(surface, self.color, (center_x, center_y), piece_radius)
        pygame.draw.circle(surface, BLACK, (center_x, center_y), piece_radius, 1)

    def start_animation(self, path_of_steps):
        if not path_of_steps:
            self.is_animating = False
            return

        self.animation_path = path_of_steps
        self.animation_start_time = pygame.time.get_ticks()
        self.is_animating = True
        self.last_sound_path_index = -1 # Reset when animation starts

    def update_animation(self):
        if not self.is_animating:
            return False

        elapsed_time = pygame.time.get_ticks() - self.animation_start_time
        
        # Calculate how many segments there are in the animation path
        # If there are N points, there are N-1 segments.
        num_segments = max(0, len(self.animation_path) - 1)
        
        # Total duration is num_segments * time_per_segment. 
        # For single point moves (e.g., just appearing), use a minimum duration.
        if num_segments == 0:
            total_duration = MIN_ANIMATION_DURATION_TOTAL_MS 
        else:
            total_duration = num_segments * PIECE_ANIMATION_DURATION_MS

        # Check if animation has finished
        if elapsed_time >= total_duration:
            if self.animation_path:
                self.current_pos = self.animation_path[-1] # Snap to final position
            self.is_animating = False
            self.animation_path = []
            self.last_sound_path_index = -1 
            return True # Animation just finished
        
        # Determine current segment for interpolation and sound
        progress_in_segments = 0
        if num_segments > 0: # Avoid division by zero
            progress_in_segments = min(num_segments, elapsed_time / PIECE_ANIMATION_DURATION_MS)

        # The index of the *start* point of the current segment for interpolation
        current_segment_start_index = math.floor(progress_in_segments) 
        
        # Play sound for each new logical step/cell crossed
        # Only play if we've moved to a new segment start index that we haven't played a sound for yet
        # and ensure it's a valid index in the path.
        if current_segment_start_index > self.last_sound_path_index and current_segment_start_index < len(self.animation_path):
            SOUNDS['piece_move'].play()
            self.last_sound_path_index = current_segment_start_index
            
        # Interpolate position
        start_index_for_interp = current_segment_start_index
        # The end point for interpolation is the next point in the path, unless we are at the very end
        end_index_for_interp = min(len(self.animation_path) - 1, start_index_for_interp + 1)

        start_row, start_col = self.animation_path[start_index_for_interp]
        start_pixel_x, start_pixel_y = get_piece_center_pixel_coords(start_row, start_col)
        
        # If we are at the very last point of a multi-segment path, or it's a single-point path
        if start_index_for_interp == end_index_for_interp:
            self.current_pos = start_row, start_col # Just snap to it for drawing accuracy
        else:
            end_row, end_col = self.animation_path[end_index_for_interp]
            end_pixel_x, end_pixel_y = get_piece_center_pixel_coords(end_row, end_col)

            # progress within current segment (0 to 1)
            segment_elapsed_time = elapsed_time - (current_segment_start_index * PIECE_ANIMATION_DURATION_MS)
            segment_progress = min(1.0, segment_elapsed_time / PIECE_ANIMATION_DURATION_MS)

            interp_x = start_pixel_x + (end_pixel_x - start_pixel_x) * segment_progress
            interp_y = start_pixel_y + (end_pixel_y - start_pixel_y) * segment_progress
            
            # Update current_pos for drawing interpolated position
            # This is a bit of a hack to keep current_pos in logical (row, col) format
            # for consistency, even though it's interpolated pixel-based.
            self.current_pos = ((interp_y - BOARD_START_Y) // CELL_SIZE, (interp_x - BOARD_START_X) // CELL_SIZE)

        return False # Animation still ongoing

    def move_out_of_base(self):
        if self.in_base:
            old_logical_pos = self.logical_pos
            self.logical_pos = PLAYER_START_SQUARES[self.player_id]
            self.in_base = False
            self.on_path = True
            try:
                self.steps_on_main_path = main_path_ordered.index(self.logical_pos)
            except ValueError:
                print(f"Error: Player {self.player_id} start square {self.logical_pos} not found in main_path_ordered.")
                self.steps_on_main_path = -1

            self.start_animation([old_logical_pos, self.logical_pos])
            return True
        return False

    def get_potential_move_pos(self, steps):
        """
        Calculates the potential new position for the piece after 'steps' moves.
        Returns (target_pos, new_main_path_index, new_final_path_index).
        Returns (None, -1, -1) if the move is invalid (e.g., overshoots home).
        """
        if self.is_home:
            return None, -1, -1

        if self.in_base:
            if steps == 6:
                start_square_index = main_path_ordered.index(PLAYER_START_SQUARES[self.player_id])
                return PLAYER_START_SQUARES[self.player_id], start_square_index, -1
            return None, -1, -1
        
        elif self.on_path:
            current_index_on_main = self.steps_on_main_path
            
            if not (0 <= current_index_on_main < len(main_path_ordered)):
                print(f"Error: Piece {self.player_id}-{self.piece_id} has invalid steps_on_main_path: {current_index_on_main}")
                return None, -1, -1

            final_path_entry_pos = PLAYER_FINAL_PATH_ENTRY_POINTS[self.player_id]
            
            try:
                final_path_main_entry_index = main_path_ordered.index(final_path_entry_pos)
            except ValueError:
                print(f"Error: Player {self.player_id} final path entry {final_path_entry_pos} not found in main_path_ordered.")
                return None, -1, -1

            # Calculate steps to reach the final path entry point (including landing on it)
            # This accounts for wrapping around the board
            steps_to_reach_entry = 0
            if final_path_main_entry_index >= current_index_on_main:
                steps_to_reach_entry = final_path_main_entry_index - current_index_on_main
            else:
                steps_to_reach_entry = len(main_path_ordered) - current_index_on_main + final_path_main_entry_index

            if steps <= steps_to_reach_entry:
                # Move stays on the main path
                target_index = (current_index_on_main + steps) % len(main_path_ordered)
                return main_path_ordered[target_index], target_index, -1
            else:
                # Move enters or passes into the final path
                steps_into_final_path = steps - (steps_to_reach_entry + 1) # +1 for the entry square itself
                
                final_path = PLAYER_FINAL_PATHS[self.player_id]
                
                if steps_into_final_path >= len(final_path):
                    return None, -1, -1 # Overshot the final home
                
                target_pos_on_final = final_path[steps_into_final_path]
                return target_pos_on_final, -1, steps_into_final_path

        elif self.in_final_path:
            final_path = PLAYER_FINAL_PATHS[self.player_id]
            target_index_on_final = self.steps_on_final_path + steps
            
            if target_index_on_final >= len(final_path):
                return None, -1, -1 # Overshot the final home
            
            target_pos_on_final = final_path[target_index_on_final]
            return target_pos_on_final, -1, target_index_on_final
            
        return None, -1, -1

    def apply_move(self, target_pos, target_main_path_index=-1, target_final_path_index=-1):
        old_logical_pos = self.logical_pos

        animation_path_coords = []
        animation_path_coords.append(old_logical_pos) # Start animation from current position

        if self.in_base:
            # Only one step from base to start square
            animation_path_coords.append(target_pos)
            self.in_base = False
            self.on_path = True
            self.steps_on_main_path = target_main_path_index
            self.steps_on_final_path = -1 
        elif self.on_path:
            current_main_path_index = self.steps_on_main_path
            
            if target_main_path_index != -1: # Still on main path
                if target_main_path_index >= current_main_path_index:
                    for i in range(current_main_path_index + 1, target_main_path_index + 1):
                        animation_path_coords.append(main_path_ordered[i])
                else: # Wrapped around the board
                    for i in range(current_main_path_index + 1, len(main_path_ordered)):
                        animation_path_coords.append(main_path_ordered[i])
                    for i in range(target_main_path_index + 1):
                        animation_path_coords.append(main_path_ordered[i])
                
                self.on_path = True
                self.in_final_path = False
                self.steps_on_main_path = target_main_path_index
                self.steps_on_final_path = -1

            elif target_final_path_index != -1: # Moving from main path to final path
                final_path_entry_pos = PLAYER_FINAL_PATH_ENTRY_POINTS[self.player_id]
                final_path_main_entry_index = main_path_ordered.index(final_path_entry_pos)

                # Add main path steps leading to the final path entry
                if final_path_main_entry_index >= current_main_path_index:
                    for i in range(current_main_path_index + 1, final_path_main_entry_index + 1):
                        animation_path_coords.append(main_path_ordered[i])
                else: # Wrapped around
                    for i in range(current_main_path_index + 1, len(main_path_ordered)):
                        animation_path_coords.append(main_path_ordered[i])
                    for i in range(final_path_main_entry_index + 1):
                        animation_path_coords.append(main_path_ordered[i])

                # Add final path steps
                final_path = PLAYER_FINAL_PATHS[self.player_id]
                for i in range(target_final_path_index + 1): # +1 because range is exclusive upper bound
                    animation_path_coords.append(final_path[i])
                
                self.on_path = False
                self.in_final_path = True
                self.steps_on_main_path = -1
                self.steps_on_final_path = target_final_path_index
            else:
                 print(f"Error: Piece {self.player_id}-{self.piece_id} on main path but invalid target type for {target_pos}")
                 animation_path_coords.append(target_pos) # Fallback

        elif self.in_final_path:
            final_path = PLAYER_FINAL_PATHS[self.player_id]
            for i in range(self.steps_on_final_path + 1, target_final_path_index + 1):
                animation_path_coords.append(final_path[i])
            
            self.on_path = False
            self.in_final_path = True
            self.steps_on_main_path = -1
            self.steps_on_final_path = target_final_path_index

        # Update logical position and state *after* path generation
        self.logical_pos = target_pos 

        if self.logical_pos == CENTER_HOME_SQUARE:
            self.on_path = False
            self.in_final_path = False
            self.is_home = True
            self.steps_on_main_path = -1
            self.steps_on_final_path = -1
            global pieces_at_home_count
            pieces_at_home_count[self.player_id] += 1
        
        # Ensure the final position is included in the animation path if it wasn't already
        if not animation_path_coords or animation_path_coords[-1] != self.logical_pos:
            animation_path_coords.append(self.logical_pos)
            
        self.start_animation(animation_path_coords)

# Global Game State Variables 
all_pieces = []
num_players = 4

current_player = 0
dice_value = 0
dice_roll_final_value = 0
current_animating_dice_value = 1
dice_animation_start_time = 0
last_dice_animation_frame_time = 0

game_state = 'MAIN_MENU'
can_roll_again = False 

pieces_per_player = 4
pieces_at_home_count = {player_id: 0 for player_id in range(num_players)}

# Game Settings (defaults for player selection screen)
game_settings = {
    'num_active_players': 4,
    'selected_country_ids': [15, 17, 47, 36],
    'player_types': ['Human', 'AI', 'Human', 'AI'],
    'ai_difficulty_level': 'Medium',
    'background_theme': 'Default',
    'fullscreen': False 
    }
# Set up display based on fullscreen preference
if game_settings.get('fullscreen'):
    display_flags |= pygame.FULLSCREEN
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Backgrounds (Simplified for Beta)
BACKGROUND_IMAGE_PATHS = {
    'Default': None,
}
current_background_image = None

# AI Turn Timing
AI_THINK_TIME_MS = 800
ai_turn_start_time = 0
ai_action_scheduled = False


# Game Initialization Function (called when starting a new game) 
def start_new_game():
    global all_pieces, num_players, current_player, dice_value, game_state, can_roll_again, pieces_at_home_count, PLAYER_COLORS, current_background_image, ai_action_scheduled
    global dice_roll_final_value, current_animating_dice_value, dice_animation_start_time, last_dice_animation_frame_time

    num_players = game_settings['num_active_players']

    PLAYER_COLORS.clear()
    for i in range(num_players):
        country_id = game_settings['selected_country_ids'][i]
        PLAYER_COLORS[i] = ALL_COUNTRIES_DATA[country_id]['color']
    
    all_pieces = []
    for player_id in range(num_players):
        home_cells_for_player = PLAYER_HOME_CELLS_LAYOUT[player_id]
        for i in range(pieces_per_player):
            initial_pos = home_cells_for_player[i]
            piece = Piece(player_id, i, initial_pos)
            all_pieces.append(piece)
    
    current_player = 0
    dice_value = 0
    dice_roll_final_value = 0
    current_animating_dice_value = 1
    dice_animation_start_time = 0
    last_dice_animation_frame_time = 0

    game_state = 'ROLL_DICE'
    can_roll_again = False
    pieces_at_home_count = {player_id: 0 for player_id in range(num_players)}
    ai_action_scheduled = False

    if game_settings['background_theme'] and BACKGROUND_IMAGE_PATHS[game_settings['background_theme']]:
        try:
            path = BACKGROUND_IMAGE_PATHS[game_settings['background_theme']]
            current_background_image = pygame.image.load(path).convert()
            current_background_image = pygame.transform.scale(current_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Warning: Could not load background image {path}. Error: {e}")
            current_background_image = None
    else:
        current_background_image = None

    print(f"New game started with {num_players} players.")
    for i in range(num_players):
        country_id = game_settings['selected_country_ids'][i]
        player_type = game_settings['player_types'][i]
        if "AI" in player_type:
            print(f"Player {i+1}: {ALL_COUNTRIES_DATA[country_id]['name']} ({player_type} - {game_settings['ai_difficulty_level']})")
        else:
            print(f"Player {i+1}: {ALL_COUNTRIES_DATA[country_id]['name']} ({player_type})")

def recreate_display_mode():
    global SCREEN
    if game_settings['fullscreen']:
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Dice Drawing and Logic 
DICE_SIZE = CELL_SIZE * 2
# Dice position moved to UI panel on the LEFT
# DICE_POS_X and DICE_POS_Y will now be calculated dynamically inside draw_game_ui_elements
# to place them relative to the end of the player info list.

def roll_dice():
    global dice_roll_final_value, game_state, dice_animation_start_time, last_dice_animation_frame_time, ai_action_scheduled
    
    dice_roll_final_value = random.randint(1, 6)
    game_state = 'DICE_ROLL_ANIMATION'
    dice_animation_start_time = pygame.time.get_ticks()
    last_dice_animation_frame_time = pygame.time.get_ticks()
    ai_action_scheduled = False
    print(f"Player {current_player+1} is rolling the dice...")
    SOUNDS['dice_roll'].play()

def draw_dice(surface, roll_value_to_display, x, y): # Added x, y parameters
    dice_rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
    pygame.draw.rect(surface, WHITE, dice_rect, 0, 5)
    pygame.draw.rect(surface, BLACK, dice_rect, 2, 5)

    dot_radius = DICE_SIZE // 10
    center_x, center_y = dice_rect.center
    offset = DICE_SIZE // 4

    # Dice dot drawing logic (unchanged, as it's correct)
    if roll_value_to_display == 1: pygame.draw.circle(surface, BLACK, (center_x, center_y), dot_radius)
    elif roll_value_to_display == 2:
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y + offset), dot_radius)
    elif roll_value_to_display == 3:
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x, center_y), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y + offset), dot_radius)
    elif roll_value_to_display == 4:
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y + offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y + offset), dot_radius)
    elif roll_value_to_display == 5:
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y + offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y + offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x, center_y), dot_radius)
    elif roll_value_to_display == 6:
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y - offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x - offset, center_y + offset), dot_radius)
        pygame.draw.circle(surface, BLACK, (center_x + offset, center_y + offset), dot_radius)


# Helper Functions for Game Logic
def get_pieces_at_position(pos, exclude_piece=None):
    pieces_at_pos = []
    for piece in all_pieces:
        if piece.logical_pos == pos and not piece.is_home and piece != exclude_piece:
            pieces_at_pos.append(piece)
    return pieces_at_pos

def is_safe_square(pos):
    return pos in SAFE_SQUARES

def can_any_piece_move(player_id, roll_value):
    for piece in all_pieces:
        if piece.player_id == player_id and not piece.is_home:
            potential_pos, _, _ = piece.get_potential_move_pos(roll_value)
            if potential_pos:
                return True
    return False

def check_for_winner():
    global pieces_at_home_count
    for player_id in range(num_players):
        count = sum(1 for piece in all_pieces if piece.player_id == player_id and piece.is_home) 
        pieces_at_home_count[player_id] = count
        
        if pieces_at_home_count[player_id] == pieces_per_player:
            return True
    return False

def end_player_turn():
    global current_player, dice_value, game_state, can_roll_again, ai_action_scheduled
    
    if check_for_winner():
        game_state = 'GAME_OVER'
        print(f"Player {current_player+1} ({ALL_COUNTRIES_DATA[game_settings['selected_country_ids'][current_player]]['name']}) wins!")
        SOUNDS['game_win'].play()
        return

    if can_roll_again:
        print(f"Player {current_player+1} gets to roll again!")
        dice_value = 0
        game_state = 'ROLL_DICE'
        can_roll_again = False # Reset for the next time
        ai_action_scheduled = False
    else:
        current_player = (current_player + 1) % num_players
        while current_player >= game_settings['num_active_players']:
            current_player = (current_player + 1) % num_players

        dice_value = 0
        game_state = 'ROLL_DICE'
        can_roll_again = False
        ai_action_scheduled = False
        print(f"Turn ended. Next player: {current_player+1}.")

# AI Logic Implementation
def is_position_vulnerable(pos, current_player_id):
    if is_safe_square(pos) or pos == CENTER_HOME_SQUARE:
        return False

    for opponent_player_id in range(game_settings['num_active_players']):
        if opponent_player_id == current_player_id:
            continue

        for opp_piece in all_pieces:
            if opp_piece.player_id == opponent_player_id and not opp_piece.is_home and not opp_piece.in_base:
                for roll in range(1, 7): 
                    potential_opp_target, _, _ = opp_piece.get_potential_move_pos(roll)
                    if potential_opp_target == pos:
                        return True
    return False


def choose_ai_move(player_id, roll_value, difficulty_level):
    possible_moves = []

    for piece in all_pieces:
        if piece.player_id == player_id and not piece.is_home:
            potential_pos, main_idx, final_idx = piece.get_potential_move_pos(roll_value)

            if potential_pos:
                current_move_score = 0
                
                if piece.in_base and roll_value == 6:
                    current_move_score = 1000 
                else: 
                    if potential_pos == CENTER_HOME_SQUARE:
                         current_move_score = max(current_move_score, 990) 

                    pieces_at_target = get_pieces_at_position(potential_pos, exclude_piece=piece) 
                    for opp_piece in pieces_at_target:
                        if opp_piece.player_id != player_id and not is_safe_square(potential_pos):
                            current_move_score = max(current_move_score, 900) 
                
                if difficulty_level == 'Easy':
                    if current_move_score < 100: 
                         current_move_score = 50 
                    
                elif difficulty_level == 'Medium' or difficulty_level == 'Hard':
                    if final_idx != -1: 
                         current_move_score = max(current_move_score, 700)
                         current_move_score += final_idx * 10 

                    if is_safe_square(potential_pos):
                        current_move_score = max(current_move_score, 600)

                    current_move_score = max(current_move_score, 300) 
                    if main_idx != -1:
                        current_move_score += (main_idx / len(main_path_ordered)) * 100 

                    if not is_safe_square(potential_pos) and is_position_vulnerable(potential_pos, player_id):
                        current_move_score -= 500 
                
                current_move_score += random.uniform(0, 4.9) 

                possible_moves.append((piece, potential_pos, main_idx, final_idx, current_move_score))

    possible_moves.sort(key=lambda x: x[4], reverse=True)

    if possible_moves:
        chosen_move = possible_moves[0]
        return chosen_move[0], chosen_move[1], chosen_move[2], chosen_move[3]
    else:
        return None, None, -1, -1 


# Font for text
# Adjusted font sizes for better fit
font = pygame.font.Font(None, 30) # Slightly smaller
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 22) # Significantly smaller for scores etc.

# UI Elements (Buttons)
class Button:
    def __init__(self, rect, text, font, color, text_color, action=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action
        self.enabled = enabled

    def draw(self, surface):
        draw_color = self.color if self.enabled else GRAY
        draw_text_color = self.text_color if self.enabled else (100, 100, 100) # Darker for disabled

        pygame.draw.rect(surface, draw_color, self.rect, 0, 5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, 5)
        text_surf = self.font.render(self.text, True, draw_text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)

# Menu Drawing Functions
def draw_main_menu():
    SCREEN.fill(BLACK)
    
    title_surf = title_font.render("Pachisi Game", True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    SCREEN.blit(title_surf, title_rect)

    # چک کنیم فایل سیو وجود داره یا نه
    save_exists = os.path.exists("savegame.json")

    start_button = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 120, 200, 60),
                      "Start Game", button_font, BLUE_BASE_COLOR, WHITE,
                      action=lambda: set_game_state('PLAYER_SELECT'))

    settings_button = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 60),
                         "Settings", button_font, YELLOW_BASE_COLOR, WHITE,
                         action=lambda: set_game_state('SETTINGS'))

    load_button = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40, 200, 60),
                     "Load Game", button_font, ORANGE_BASE_COLOR, WHITE,
                     action=lambda: load_game_into_state("savegame.json"),
                     enabled=save_exists)   # ← فقط فعال میشه اگه فایل سیو وجود داشته باشه

    quit_button = Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 60),
                     "Quit", button_font, RED_BASE_COLOR, WHITE,
                     action=lambda: set_running(False))

    # Draw the buttons
    start_button.draw(SCREEN)
    settings_button.draw(SCREEN)
    load_button.draw(SCREEN)
    quit_button.draw(SCREEN)

    # Credits at the bottom
    credit_font = pygame.font.Font(None, 24)
    credit_text = credit_font.render("Created by Pouya Motallebi (Peter Smith), 2025", True, (180, 180, 180))
    credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
    SCREEN.blit(credit_text, credit_rect)

    email_text = credit_font.render("Contact: pouyam81@outlook.com", True, (150, 150, 150))
    email_rect = email_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT -45))
    SCREEN.blit(email_text, email_rect)

    return [start_button, settings_button, load_button, quit_button]


def toggle_fullscreen_setting():
    game_settings['fullscreen'] = not game_settings['fullscreen']
    recreate_display_mode()
    print("Fullscreen mode is now", "ON" if game_settings['fullscreen'] else "OFF")

def draw_settings_menu():
    SCREEN.fill(BLACK)
    
    title_surf = title_font.render("Game Settings", True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    SCREEN.blit(title_surf, title_rect)

    buttons = []
    y_offset = SCREEN_HEIGHT // 3
    spacing = 80   
    big_spacing = 150  

    # AI Difficulty Setting
    difficulty_levels = ['Easy', 'Medium', 'Hard']
    current_difficulty_idx = difficulty_levels.index(game_settings['ai_difficulty_level'])
    difficulty_text = f"AI Difficulty: {game_settings['ai_difficulty_level']}"

    difficulty_button_width = 250
    arrow_button_width = 40
    arrow_spacing = 10
    total_difficulty_row_width = arrow_button_width + arrow_spacing + difficulty_button_width + arrow_spacing + arrow_button_width
    start_x_difficulty_row = (SCREEN_WIDTH - total_difficulty_row_width) // 2

    prev_difficulty_button = Button((start_x_difficulty_row, y_offset, arrow_button_width, 50),
                                    "<", font, LIGHT_GRAY, BLACK,
                                    action=lambda: cycle_ai_difficulty(-1))
    prev_difficulty_button.draw(SCREEN)
    buttons.append(prev_difficulty_button)

    difficulty_display_button = Button((start_x_difficulty_row + arrow_button_width + arrow_spacing, y_offset, difficulty_button_width, 50),
                                       difficulty_text, font, LIGHT_GRAY, BLACK)
    difficulty_display_button.draw(SCREEN)
    buttons.append(difficulty_display_button)

    next_difficulty_button = Button((start_x_difficulty_row + arrow_button_width + arrow_spacing + difficulty_button_width + arrow_spacing,
                                     y_offset, arrow_button_width, 50),
                                    ">", font, LIGHT_GRAY, BLACK,
                                    action=lambda: cycle_ai_difficulty(1))
    next_difficulty_button.draw(SCREEN)
    buttons.append(next_difficulty_button)

    y_offset += spacing

    # Fullscreen Toggle
    fullscreen_status = "ON" if game_settings['fullscreen'] else "OFF"
    fullscreen_text = f"Fullscreen: {fullscreen_status}"
    fullscreen_color = (0, 200, 0) if game_settings['fullscreen'] else (200, 0, 0)

    fullscreen_button = Button(
        (SCREEN_WIDTH // 2 - 100, y_offset, 200, 55),
        fullscreen_text,
        font,
        fullscreen_color,
        WHITE,
        action=toggle_fullscreen_setting
    )
    fullscreen_button.draw(SCREEN)
    buttons.append(fullscreen_button)

    y_offset += spacing

    # Mute Button
    mute_button = Button(
        (SCREEN_WIDTH // 2 - 100, y_offset, 200, 55),
        "Mute" if not is_muted else "Unmute",
        button_font,
        ORANGE_BASE_COLOR,
        WHITE,
        action=toggle_mute
    )
    mute_button.draw(SCREEN)
    buttons.append(mute_button)

    y_offset += big_spacing

    # Back Button
    back_button = Button((SCREEN_WIDTH // 2 - 75, y_offset, 150, 50),
                         "Back", button_font, GRAY, WHITE,
                         action=lambda: set_game_state('MAIN_MENU'))
    back_button.draw(SCREEN)
    buttons.append(back_button)

    return buttons

def draw_player_select_screen():
    SCREEN.fill(BLACK)
    
    title_surf = title_font.render("Select Players", True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    SCREEN.blit(title_surf, title_rect)

    buttons = []
    y_offset = SCREEN_HEIGHT // 4

    # Number of Players Toggle
    num_players_text = f"Active Players: {game_settings['num_active_players']}"
    num_players_button = Button((SCREEN_WIDTH // 2 - 150, y_offset, 300, 50), num_players_text, font, LIGHT_GRAY, BLACK, action=toggle_num_players)
    num_players_button.draw(SCREEN)
    buttons.append(num_players_button)
    y_offset += 70

    # Player Country and Type Selection
    player_selection_y = y_offset + 10
    for i in range(4):
        is_active = (i < game_settings['num_active_players'])
        
        row_y = player_selection_y + i * 70
        country_button_width = 200
        type_button_width = 100
        arrow_button_width = 40
        spacing = 10

        total_row_width = arrow_button_width + spacing + country_button_width + spacing + arrow_button_width + spacing + type_button_width
        start_x = (SCREEN_WIDTH - total_row_width) // 2

        prev_arrow_x = start_x
        country_btn_x = prev_arrow_x + arrow_button_width + spacing
        next_arrow_x = country_btn_x + country_button_width + spacing
        type_btn_x = next_arrow_x + arrow_button_width + spacing
        
        if is_active:
            player_color = ALL_COUNTRIES_DATA[game_settings['selected_country_ids'][i]]['color']
            text_color = BLACK
            country_name = ALL_COUNTRIES_DATA[game_settings['selected_country_ids'][i]]['name']
            country_btn = Button((country_btn_x, row_y, country_button_width, 50), 
                                f"P{i+1}: {country_name}", 
                                font, player_color, text_color,
                                action=lambda p_idx=i: cycle_player_country(p_idx))
            country_btn.draw(SCREEN)
            buttons.append(country_btn)
            
            prev_button = Button((prev_arrow_x, row_y, arrow_button_width, 50), "<", font, LIGHT_GRAY, BLACK, action=lambda p_idx=i: cycle_player_country(p_idx, direction=-1))
            prev_button.draw(SCREEN)
            buttons.append(prev_button)

            next_button = Button((next_arrow_x, row_y, arrow_button_width, 50), ">", font, LIGHT_GRAY, BLACK, action=lambda p_idx=i: cycle_player_country(p_idx, direction=1))
            next_button.draw(SCREEN)
            buttons.append(next_button)

            player_type_text = game_settings['player_types'][i]
            type_btn_color = (0, 150, 0) if player_type_text == 'Human' else (150, 0, 0)
            type_btn = Button((type_btn_x, row_y, type_button_width, 50),
                              player_type_text,
                              font,
                              type_btn_color,
                              WHITE,
                              action=lambda p_idx=i: toggle_player_type(p_idx))
            type_btn.draw(SCREEN)
            buttons.append(type_btn)
        else:
            inactive_text = f"P{i+1}: Inactive"
            inactive_color = GRAY
            inactive_text_color = LIGHT_GRAY
            inactive_rect = (prev_arrow_x, row_y, arrow_button_width + spacing + country_button_width + spacing + arrow_button_width, 50) 
            inactive_button = Button(inactive_rect, inactive_text, font, inactive_color, inactive_text_color)
            inactive_button.draw(SCREEN)

    y_offset = player_selection_y + 4 * 70 + 20

    start_game_button = Button((SCREEN_WIDTH // 2 - 120, y_offset, 240, 60), "Start Game", button_font, GREEN, WHITE, action=lambda: start_game_from_select())
    start_game_button.draw(SCREEN)
    buttons.append(start_game_button)
    y_offset += 80

    back_button = Button((SCREEN_WIDTH // 2 - 75, y_offset, 150, 50), "Back", button_font, GRAY, WHITE, action=lambda: set_game_state('MAIN_MENU'))
    back_button.draw(SCREEN)
    buttons.append(back_button)

    return buttons

# Function to draw the Game Over screen with scores
def draw_game_over_screen():
    SCREEN.fill(BLACK)

    buttons = []
    
    # Title
    title_surf = title_font.render("Game Over!", True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    SCREEN.blit(title_surf, title_rect)

    # Winner Display
    winner_country_id = game_settings['selected_country_ids'][current_player]
    winner_country_name = ALL_COUNTRIES_DATA[winner_country_id]['name']
    winner_text = button_font.render(f"Winner: Player {current_player+1} ({winner_country_name})", True, PLAYER_COLORS[current_player])
    winner_text_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 20))
    SCREEN.blit(winner_text, winner_text_rect)

    # Scoreboard
    scoreboard_title_surf = font.render("Final Scores:", True, WHITE)
    scoreboard_title_rect = scoreboard_title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(scoreboard_title_surf, scoreboard_title_rect)

    # Prepare player data for sorting
    player_scores_data = []
    for player_id in range(game_settings['num_active_players']):
        country_id = game_settings['selected_country_ids'][player_id]
        country_name = ALL_COUNTRIES_DATA[country_id]['name']
        player_type_display = game_settings['player_types'][player_id]
        if player_type_display == 'AI':
            player_type_display = f"AI ({game_settings['ai_difficulty_level']})"
        
        score = pieces_at_home_count.get(player_id, 0)
        player_scores_data.append({
            'player_id': player_id,
            'country_name': country_name,
            'player_type': player_type_display,
            'score': score,
            'color': PLAYER_COLORS[player_id]
        })

    # Sort players by score (descending) - FIXED: Used 'score' key
    player_scores_data.sort(key=lambda x: x['score'], reverse=True) 

    score_y_offset = SCREEN_HEIGHT // 2
    for i, player_data in enumerate(player_scores_data):
        score_text = font.render(
            f"#{i+1}: P{player_data['player_id']+1} {player_data['country_name']} ({player_data['player_type']}) - Pieces Home: {player_data['score']}/{pieces_per_player}",
            True, player_data['color']
        )
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, score_y_offset + i * 40))
        SCREEN.blit(score_text, score_rect)
    
    # Buttons
    button_y_start = score_y_offset + len(player_scores_data) * 40 + 30
    
    main_menu_button = Button((SCREEN_WIDTH // 2 - 120, button_y_start, 240, 60), "Main Menu", button_font, BLUE_BASE_COLOR, WHITE, action=lambda: set_game_state('MAIN_MENU'))
    main_menu_button.draw(SCREEN)
    buttons.append(main_menu_button)

    quit_button = Button((SCREEN_WIDTH // 2 - 75, button_y_start + 70, 150, 50), "Quit", button_font, RED_BASE_COLOR, WHITE, action=lambda: set_running(False))
    quit_button.draw(SCREEN)
    buttons.append(quit_button)

    return buttons

# Menu Action Functions
def set_game_state(state):
    global game_state
    game_state = state
    
def toggle_mute():
    global is_muted
    is_muted = not is_muted
    volume = 0.0 if is_muted else 1.0
    pygame.mixer.music.set_volume(volume)

    for s in all_sounds:  
        s.set_volume(volume)

    print("Muted" if is_muted else "Unmuted")

def set_running(val):
    global running
    running = val

def load_game_into_state(filename):
    global game_settings, current_player, dice_value, can_roll_again
    global pieces_at_home_count, all_pieces, PLAYER_COLORS, num_players
    global ai_action_scheduled, current_background_image
    global dice_roll_final_value, current_animating_dice_value
    global dice_animation_start_time, last_dice_animation_frame_time

    # Read the raw data without instantiating Piece objects.
    (game_settings, current_player, dice_value, can_roll_again,
    pieces_at_home_count, pieces_data, schema_version) = load_game(filename)

    if isinstance(pieces_at_home_count, dict):
        pieces_at_home_count = {int(k): v for k, v in pieces_at_home_count.items()}
    else:
        # If the data was saved as a list, convert it to a dictionary.
        pieces_at_home_count = {i: val for i, val in enumerate(pieces_at_home_count)}

    num_players = game_settings['num_active_players']
    PLAYER_COLORS.clear()
    for i in range(num_players):
        country_id = game_settings['selected_country_ids'][i]
        PLAYER_COLORS[i] = ALL_COUNTRIES_DATA[country_id]['color']

    # With PLAYER_COLORS ready, create the Piece objects.
    all_pieces = []
    for pdata in pieces_data:
        logical_pos = tuple(pdata["logical_pos"]) if pdata["logical_pos"] is not None else None
        p = Piece(pdata["player_id"], pdata["piece_id"], logical_pos)

        # Set the remaining fields.
        p.in_base = pdata["in_base"]
        p.on_path = pdata["on_path"]
        p.in_final_path = pdata["in_final_path"]
        p.is_home = pdata["is_home"]
        p.steps_on_main_path = pdata["steps_on_main_path"]
        p.steps_on_final_path = pdata["steps_on_final_path"]

        # Synchronize with the rendering engine.
        p.current_pos = p.logical_pos
        p.is_animating = False
        p.animation_path = []
        p.last_sound_path_index = -1
        p.highlight = False
        all_pieces.append(p)

    # Reset transient states for the dice and AI.
    dice_roll_final_value = 0
    current_animating_dice_value = 1
    dice_animation_start_time = 0
    last_dice_animation_frame_time = 0
    ai_action_scheduled = False

    # Reload the background, similar to a new game.
    if game_settings.get('background_theme') and BACKGROUND_IMAGE_PATHS.get(game_settings['background_theme']):
        try:
            path = BACKGROUND_IMAGE_PATHS[game_settings['background_theme']]
            current_background_image = pygame.image.load(path).convert()
            current_background_image = pygame.transform.scale(current_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Warning: Could not load background image {path}. Error: {e}")
            current_background_image = None
    else:
        current_background_image = None

    # Revert to the start of a turn.
    set_game_state('ROLL_DICE')
    print("Save loaded and state restored.")

def cycle_ai_difficulty(direction):
    global game_settings
    difficulty_levels = ['Easy', 'Medium', 'Hard']
    current_idx = difficulty_levels.index(game_settings['ai_difficulty_level'])
    new_idx = (current_idx + direction + len(difficulty_levels)) % len(difficulty_levels)
    game_settings['ai_difficulty_level'] = difficulty_levels[new_idx]
    print(f"AI Difficulty set to: {game_settings['ai_difficulty_level']}")

def toggle_num_players():
    global game_settings
    current_num = game_settings['num_active_players']
    next_num = (current_num % 4) + 1
    if next_num == 1:
        next_num = 2
    game_settings['num_active_players'] = next_num
    print(f"Number of active players set to: {game_settings['num_active_players']}")

    while len(game_settings['selected_country_ids']) < 4:
        game_settings['selected_country_ids'].append(0) 
    while len(game_settings['player_types']) < 4:
        game_settings['player_types'].append('AI') 

    for i in range(game_settings['num_active_players'], 4):
        game_settings['player_types'][i] = 'AI'
    
    current_country_ids = list(game_settings['selected_country_ids'])
    assigned_ids = set()
    new_selected_country_ids = []

    for i in range(game_settings['num_active_players']):
        if i < len(current_country_ids) and current_country_ids[i] not in assigned_ids:
            new_selected_country_ids.append(current_country_ids[i])
            assigned_ids.add(current_country_ids[i])
        else:
            found_unique = False
            for country_data in ALL_COUNTRIES_DATA:
                if country_data['id'] not in assigned_ids:
                    new_selected_country_ids.append(country_data['id'])
                    assigned_ids.add(country_data['id'])
                    found_unique = True
                    break
            if not found_unique:
                new_selected_country_ids.append(ALL_COUNTRIES_DATA[0]['id'])
                assigned_ids.add(ALL_COUNTRIES_DATA[0]['id'])

    game_settings['selected_country_ids'] = new_selected_country_ids + [0] * (4 - game_settings['num_active_players'])
    
    print(f"Player types after toggle_num_players: {game_settings['player_types']}")


def toggle_player_type(player_slot_index):
    global game_settings
    if player_slot_index < game_settings['num_active_players']: 
        if game_settings['player_types'][player_slot_index] == 'Human':
            game_settings['player_types'][player_slot_index] = 'AI'
        else:
            game_settings['player_types'][player_slot_index] = 'Human'
        print(f"Player {player_slot_index+1} set to: {game_settings['player_types'][player_slot_index]}")

def cycle_player_country(player_slot_index, direction=1):
    global game_settings
    if player_slot_index >= game_settings['num_active_players']:
        return

    current_country_id = game_settings['selected_country_ids'][player_slot_index]
    
    current_idx_in_all = -1
    for i, country_data in enumerate(ALL_COUNTRIES_DATA):
        if country_data['id'] == current_country_id:
            current_idx_in_all = i
            break
    
    if current_idx_in_all != -1:
        num_countries = len(ALL_COUNTRIES_DATA)
        
        for _ in range(num_countries):
            current_idx_in_all = (current_idx_in_all + direction + num_countries) % num_countries
            next_country_id = ALL_COUNTRIES_DATA[current_idx_in_all]['id']
            
            is_unique = True
            for i in range(game_settings['num_active_players']):
                if i != player_slot_index and game_settings['selected_country_ids'][i] == next_country_id:
                    is_unique = False
                    break
            
            if is_unique:
                game_settings['selected_country_ids'][player_slot_index] = next_country_id
                print(f"Player {player_slot_index+1} is now {ALL_COUNTRIES_DATA[next_country_id]['name']}")
                return
        
        print("Could not find an unassigned unique country for this slot.")

def start_game_from_select():
    active_country_ids = game_settings['selected_country_ids'][:game_settings['num_active_players']]
    if len(set(active_country_ids)) != len(active_country_ids):
        print("Warning: Duplicate countries detected among active players. Attempting to assign unique defaults.")
        default_unique_ids = []
        for i in range(game_settings['num_active_players']):
            chosen = False
            for country_data in ALL_COUNTRIES_DATA:
                if country_data['id'] not in default_unique_ids:
                    default_unique_ids.append(country_data['id'])
                    chosen = True
                    break
            if not chosen:
                default_unique_ids.append(0)

        game_settings['selected_country_ids'] = default_unique_ids + [0] * (4 - game_settings['num_active_players'])
        print(f"Assigned unique countries: {game_settings['selected_country_ids'][:game_settings['num_active_players']]}")

    start_new_game()

# Function to draw the player information panel
def draw_player_info_panel(surface):
    # Panel is now on the left side
    panel_x = 0
    panel_y = BOARD_START_Y
    panel_width = UI_PANEL_WIDTH # Use the full UI panel width
    panel_height = BOARD_PIXEL_SIZE

    # Background for the panel
    pygame.draw.rect(surface, LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height), 0, 5)
    pygame.draw.rect(surface, BLACK, (panel_x, panel_y, panel_width, panel_height), 2, 5)

    current_y = panel_y + 10 # Start drawing slightly down from the top of the panel
    text_indent = 10 # Small indent from the left edge of the panel
    color_box_size = 15 # Size of the small colored square

    # Current Player Info
    if PLAYER_COLORS and current_player < num_players: 
        player_country_id_in_settings = game_settings['selected_country_ids'][current_player]
        player_country_name = ALL_COUNTRIES_DATA[player_country_id_in_settings]['name']
        
        player_type_name = game_settings['player_types'][current_player]
        if player_type_name == 'AI':
            player_type_name = f"AI ({game_settings['ai_difficulty_level']})"

        # Always render text in BLACK for readability
        turn_text_surf = font.render("CURRENT TURN:", True, BLACK)
        surface.blit(turn_text_surf, (panel_x + text_indent, current_y))
        current_y += 30

        # Player name text in black
        player_name_surf = font.render(f"P{current_player+1}: {player_country_name}", True, BLACK)
        name_x = panel_x + text_indent
        name_y = current_y
        surface.blit(player_name_surf, (name_x, name_y))
        
        # Draw small color indicator next to player name
        color_box_x = name_x + player_name_surf.get_width() + 5 # 5 pixel gap
        color_box_y = name_y + (font.get_height() - color_box_size) // 2
        pygame.draw.rect(surface, PLAYER_COLORS[current_player], (color_box_x, color_box_y, color_box_size, color_box_size))
        pygame.draw.rect(surface, BLACK, (color_box_x, color_box_y, color_box_size, color_box_size), 1) # Border

        current_y += 30

        player_type_surf = small_font.render(f"({player_type_name})", True, BLACK)
        surface.blit(player_type_surf, (panel_x + text_indent, current_y))
        current_y += 40

    # Game State
    state_text = small_font.render(f"State: {game_state.replace('_', ' ').title()}", True, BLACK)
    surface.blit(state_text, (panel_x + text_indent, current_y))
    current_y += 40

    # Player Scores
    score_title_surf = font.render("Scores:", True, BLACK)
    surface.blit(score_title_surf, (panel_x + text_indent, current_y))
    current_y += 30

    for player_id in range(game_settings['num_active_players']):
        country_name = ALL_COUNTRIES_DATA[game_settings['selected_country_ids'][player_id]]['name']
        
        count = pieces_at_home_count.get(player_id, 0)
        
        score_text_str = f"P{player_id+1} {country_name}: {count}/{pieces_per_player}"
        score_text = small_font.render(score_text_str, True, BLACK) # Always black text
        score_x = panel_x + text_indent
        score_y = current_y

        surface.blit(score_text, (score_x, score_y))
        
        # Draw small color indicator next to score
        color_box_x = score_x + score_text.get_width() + 5
        color_box_y = score_y + (small_font.get_height() - color_box_size) // 2
        pygame.draw.rect(surface, PLAYER_COLORS[player_id], (color_box_x, color_box_y, color_box_size, color_box_size))
        pygame.draw.rect(surface, BLACK, (color_box_x, color_box_y, color_box_size, color_box_size), 1) # Border

        current_y += 25
    
    # Return the current_y, so other elements can be drawn below the scores.
    return current_y

# Draw in-game UI elements (dice and action buttons)
def draw_game_ui_elements(surface):
    buttons = []
    
    # Calculate starting Y position for dice and buttons below the player info
    # We pass the return value from draw_player_info_panel to this function
    # Let's define a fixed area for these at the bottom of the UI panel for now
    
    # UI Panel is from panel_y (BOARD_START_Y) to panel_y + panel_height
    # The bottom space for dice and buttons should be enough
    ui_panel_bottom_y = BOARD_START_Y + BOARD_PIXEL_SIZE
    
    # Calculate starting Y for dice and buttons from the bottom of the panel
    # We want some padding from the bottom as well
    padding_from_bottom = 20
    button_height = 40
    button_spacing = 15
    dice_button_section_height = DICE_SIZE + button_height * 2 + button_spacing * 2 + 10 # Estimate needed space
    
    current_y = ui_panel_bottom_y - dice_button_section_height - padding_from_bottom
    
    # Dice Position: Centered horizontally in the UI panel
    dice_x = (UI_PANEL_WIDTH - DICE_SIZE) // 2
    dice_y = current_y + 10 # Add a little padding from the top of its section
    draw_dice(surface, current_animating_dice_value if game_state == 'DICE_ROLL_ANIMATION' else dice_value, dice_x, dice_y)

    current_y = dice_y + DICE_SIZE + button_spacing

    # Roll Dice Button
    roll_button_width = 150
    roll_button_height = 50
    roll_button_x = (UI_PANEL_WIDTH - roll_button_width) // 2

    roll_button_text = ""
    roll_button_enabled = False
    roll_button_color = GRAY
    roll_button_text_color = WHITE

    if game_settings['player_types'][current_player] == 'Human':
        if game_state == 'ROLL_DICE':
            roll_button_text = f"ROLL ({dice_value})" if dice_value != 0 else "ROLL DICE"
            roll_button_enabled = True
            roll_button_color = BLUE_BASE_COLOR
        elif game_state == 'DICE_ROLL_ANIMATION':
            roll_button_text = "ROLLING..."
            roll_button_enabled = False
            roll_button_color = GRAY
        elif game_state == 'MOVE_PIECE' or game_state == 'ANIMATING_MOVE':
            roll_button_text = f"ROLL ({dice_value})"
            roll_button_enabled = False # Can't roll again until turn ends or piece moved
            roll_button_color = GRAY
    else: # AI turn
        if game_state == 'ROLL_DICE':
            roll_button_text = "AI's Turn..."
            roll_button_enabled = False
            roll_button_color = GRAY
        elif game_state == 'DICE_ROLL_ANIMATION':
            roll_button_text = "AI ROLLING..."
            roll_button_enabled = False
            roll_button_color = GRAY
        elif game_state == 'MOVE_PIECE':
            roll_button_text = f"AI MOVES ({dice_value})"
            roll_button_enabled = False
            roll_button_color = GRAY
        elif game_state == 'ANIMATING_MOVE':
            roll_button_text = "AI MOVING..."
            roll_button_enabled = False
            roll_button_color = GRAY

    roll_dice_button = Button((roll_button_x, current_y, roll_button_width, roll_button_height),
                              roll_button_text, font, roll_button_color, roll_button_text_color,
                              action=roll_dice, enabled=roll_button_enabled)
    roll_dice_button.draw(surface)
    buttons.append(roll_dice_button)
    
    #current_y += roll_button_height + button_spacing

    # End Turn Button (only visible/enabled for human player in MOVE_PIECE state)
    end_turn_button_width = 150
    end_turn_button_height = 40
    end_turn_button_x = (UI_PANEL_WIDTH - end_turn_button_width) // 2

    end_turn_enabled = (game_state == 'MOVE_PIECE' and 
                        game_settings['player_types'][current_player] == 'Human' and 
                        not can_any_piece_move(current_player, dice_value))
    
    end_turn_button = Button((end_turn_button_x, current_y, end_turn_button_width, end_turn_button_height), 
                             "End Turn", small_font, GRAY, BLACK, 
                             action=end_player_turn, enabled=end_turn_enabled)

    current_y += end_turn_button_height + button_spacing

    # Main Menu Button
    main_menu_button_width = 150
    main_menu_button_height = 50
    main_menu_button_x = (UI_PANEL_WIDTH - main_menu_button_width) // 2

    def confirm_main_menu():
        set_game_state('MAIN_MENU')

    # Save Button
    save_button = Button(
        (main_menu_button_x, current_y, main_menu_button_width, main_menu_button_height),
        "Save Game",
        small_font,
        GREEN,
        WHITE,
        action=lambda: (
            save_game("savegame.json", game_settings, current_player,
                      dice_value, can_roll_again, pieces_at_home_count, all_pieces),
            set_save_notification("Game Saved!")
        )
    )
    save_button.draw(surface)
    buttons.append(save_button)
    current_y += main_menu_button_height + button_spacing

    # If the notification is active and less than 2 seconds have passed.
    if save_notification and pygame.time.get_ticks() - save_notification_time < 2000:
        notif_font = pygame.font.Font(None, 32)
        notif_text = notif_font.render(save_notification, True, WHITE)
        notif_rect = notif_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT// 49))
        surface.blit(notif_text, notif_rect)

    # Main Menu Button
    main_menu_button = Button(
        (main_menu_button_x, current_y, main_menu_button_width, main_menu_button_height),
        "Main Menu",
        small_font,
        RED_BASE_COLOR,
        WHITE,
        action=confirm_main_menu
    )
    main_menu_button.draw(surface)
    buttons.append(main_menu_button)
    return buttons

def set_save_notification(message):
    global save_notification, save_notification_time
    save_notification = message
    save_notification_time = pygame.time.get_ticks()  # Current time (in milliseconds)

# Main Game Loop 
running = True
active_buttons = []

while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                game_settings['fullscreen'] = not game_settings['fullscreen']
                recreate_display_mode()
            if event.key == pygame.K_SPACE:
                if game_settings['player_types'][current_player] == 'Human' and game_state == 'ROLL_DICE':
                    roll_dice()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if game_state in ['MAIN_MENU', 'SETTINGS', 'PLAYER_SELECT', 'GAME_OVER']:
                for button in active_buttons:
                    if button.is_clicked((mouse_x, mouse_y)):
                        if button.action:
                            button.action()
                        break
            
            elif game_state in ['ROLL_DICE', 'MOVE_PIECE'] and game_settings['player_types'][current_player] == 'Human': 
                # Check interaction with in-game buttons
                for button in active_buttons:
                    if button.is_clicked((mouse_x, mouse_y)):
                        if button.action:
                            button.action()
                            # If a button action changes game state, avoid further piece selection
                            if button.action == roll_dice or button.action == end_player_turn:
                                break 
                
                # If it's a human's turn to move a piece, and they click outside buttons
                if game_state == 'MOVE_PIECE' and game_settings['player_types'][current_player] == 'Human':
                    moved_a_piece_this_turn = False
                    for piece in all_pieces:
                        if piece.player_id == current_player and not piece.is_home:
                            # Use piece's current_pos for click detection during animation (if any) or logical_pos
                            piece_pixel_x, piece_pixel_y = get_pixel_coords(piece.logical_pos[0], piece.logical_pos[1])
                            piece_click_rect = pygame.Rect(piece_pixel_x, piece_pixel_y, CELL_SIZE, CELL_SIZE)

                            if piece_click_rect.collidepoint(mouse_x, mouse_y):
                                potential_new_pos, main_idx, final_idx = piece.get_potential_move_pos(dice_value)

                                if potential_new_pos:
                                    print(f"Player {current_player+1} successfully selected piece {piece.piece_id}.")
                                    
                                    if piece.in_base and dice_value == 6:
                                        piece.move_out_of_base()
                                    else:
                                        piece.apply_move(potential_new_pos, main_idx, final_idx)
                                    
                                    game_state = 'ANIMATING_MOVE'
                                    
                                    for p in all_pieces:
                                        p.highlight = False
                                    
                                    moved_a_piece_this_turn = True
                                    break 
                                else:
                                    print(f"Cannot move selected piece {piece.piece_id} {dice_value} steps. Invalid target or rule restriction.")
                    
                    if not moved_a_piece_this_turn and game_state != 'ANIMATING_MOVE':
                        print("No piece moved with the rolled value. Player can try another piece or end turn.")

    # AI Turn Logic (runs outside event loop)
    if game_state == 'ROLL_DICE' and game_settings['player_types'][current_player] == 'AI':
        if not ai_action_scheduled:
            ai_turn_start_time = pygame.time.get_ticks() 
            ai_action_scheduled = True
            print(f"AI Player {current_player+1} is thinking (roll)...")
        
        if pygame.time.get_ticks() - ai_turn_start_time >= AI_THINK_TIME_MS:
            roll_dice()
    
    elif game_state == 'DICE_ROLL_ANIMATION':
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - dice_animation_start_time

        if elapsed_time >= DICE_ANIMATION_DURATION_MS:
            dice_value = dice_roll_final_value
            can_roll_again = (dice_value == 6) # Grant extra turn if a 6 is rolled
            print(f"Player {current_player+1} rolled {dice_value}. Can roll again: {can_roll_again}")
            
            if not can_any_piece_move(current_player, dice_value):
                print(f"Player {current_player+1} has no valid moves for roll {dice_value}. Ending turn.")
                end_player_turn()
            else:
                game_state = 'MOVE_PIECE'

        elif current_time - last_dice_animation_frame_time >= DICE_ANIMATION_FRAME_RATE_MS:
            current_animating_dice_value = random.randint(1, 6)
            last_dice_animation_frame_time = current_time

    elif game_state == 'MOVE_PIECE' and game_settings['player_types'][current_player] == 'AI':
        if not ai_action_scheduled:
            ai_turn_start_time = pygame.time.get_ticks() 
            ai_action_scheduled = True
            print(f"AI Player {current_player+1} is thinking (move)...")

        if pygame.time.get_ticks() - ai_turn_start_time >= AI_THINK_TIME_MS:
            piece_to_move, target_pos, main_idx, final_idx = choose_ai_move(current_player, dice_value, game_settings['ai_difficulty_level'])
            
            if piece_to_move:
                print(f"AI Player {current_player+1} chose to move piece {piece_to_move.piece_id}.")
                if piece_to_move.in_base and dice_value == 6:
                    piece_to_move.move_out_of_base()
                else:
                    piece_to_move.apply_move(target_pos, main_idx, final_idx)
                
                game_state = 'ANIMATING_MOVE'
            else:
                print(f"AI Player {current_player+1} found no valid moves, ending turn.")
                end_player_turn()

            ai_action_scheduled = False 

    elif game_state == 'ANIMATING_MOVE':
        all_animations_done = True
        for piece in all_pieces:
            if piece.is_animating:
                piece.update_animation() # `update_animation` now handles its own sound
                all_animations_done = False
        
        if all_animations_done:
            pieces_that_just_landed = [p for p in all_pieces if not p.is_animating and p.logical_pos == p.current_pos and p.player_id == current_player]
            
            cut_occurred = False
            for piece_that_landed in pieces_that_just_landed:
                if piece_that_landed.on_path and not is_safe_square(piece_that_landed.logical_pos):
                    opp_pieces_at_pos = get_pieces_at_position(piece_that_landed.logical_pos, exclude_piece=piece_that_landed)
                    for opp_piece in opp_pieces_at_pos:
                        if opp_piece.player_id != piece_that_landed.player_id:
                            print(f"Player {piece_that_landed.player_id+1} cut opponent piece {opp_piece.player_id+1}-{opp_piece.piece_id}!")
                            
                            old_opp_pos = opp_piece.logical_pos
                            opp_piece.logical_pos = PLAYER_HOME_CELLS_LAYOUT[opp_piece.player_id][opp_piece.piece_id % pieces_per_player]
                            opp_piece.in_base = True
                            opp_piece.on_path = False
                            opp_piece.in_final_path = False
                            opp_piece.is_home = False
                            opp_piece.steps_on_main_path = -1
                            opp_piece.steps_on_final_path = -1
                            opp_piece.current_pos = old_opp_pos
                            opp_piece.start_animation([old_opp_pos, opp_piece.logical_pos])
                            
                            SOUNDS['piece_cut'].play()
                            cut_occurred = True
                            can_roll_again = True

            all_animations_done_after_cuts = True
            for p in all_pieces:
                if p.is_animating:
                    all_animations_done_after_cuts = False
                    break
            
            if all_animations_done_after_cuts:
                end_player_turn()


    # Drawing
    SCREEN.fill(BLACK)

    if current_background_image:
        SCREEN.blit(current_background_image, (0, 0))
    else:
        # Draw the board background (green area)
        pygame.draw.rect(SCREEN, GREEN, (BOARD_START_X, BOARD_START_Y, BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE))

        # Draw individual cells and paths
        for row in range(BOARD_CELLS_PER_SIDE):
            for col in range(BOARD_CELLS_PER_SIDE):
                x, y = get_pixel_coords(row, col)
                current_cell = (row, col)

                fill_color = None
                if current_cell in main_path_ordered:
                    fill_color = PATH_COLOR
                elif current_cell in RED_FINAL_PATH:
                    fill_color = RED_BASE_COLOR
                elif current_cell in BLUE_FINAL_PATH:
                    fill_color = BLUE_BASE_COLOR
                elif current_cell in YELLOW_FINAL_PATH:
                    fill_color = YELLOW_BASE_COLOR
                elif current_cell in ORANGE_FINAL_PATH:
                    fill_color = ORANGE_BASE_COLOR
                elif current_cell == CENTER_HOME_SQUARE:
                    fill_color = HOME_COLOR
                
                if fill_color:
                    pygame.draw.rect(SCREEN, fill_color, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

                # Draw base areas (always for 4 players for board layout)
                if current_cell in PLAYER_HOME_CELLS_LAYOUT[0]:
                    pygame.draw.rect(SCREEN, RED_BASE_COLOR, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
                elif current_cell in PLAYER_HOME_CELLS_LAYOUT[1]:
                    pygame.draw.rect(SCREEN, BLUE_BASE_COLOR, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
                elif current_cell in PLAYER_HOME_CELLS_LAYOUT[2]:
                    pygame.draw.rect(SCREEN, YELLOW_BASE_COLOR, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
                elif current_cell in PLAYER_HOME_CELLS_LAYOUT[3]:
                    pygame.draw.rect(SCREEN, ORANGE_BASE_COLOR, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

                pygame.draw.rect(SCREEN, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

                if current_cell in SAFE_SQUARES:
                    center_x = x + CELL_SIZE // 2
                    center_y = y + CELL_SIZE // 2
                    pygame.draw.circle(SCREEN, BLACK, (center_x, center_y), CELL_SIZE // 4, 2)


    # Render based on game state
    if game_state == 'MAIN_MENU':
        active_buttons = draw_main_menu()
    elif game_state == 'SETTINGS':
        active_buttons = draw_settings_menu()
    elif game_state == 'PLAYER_SELECT':
        active_buttons = draw_player_select_screen()
    elif game_state == 'GAME_OVER':
        active_buttons = draw_game_over_screen()

    else: # Game states: ROLL_DICE, DICE_ROLL_ANIMATION, MOVE_PIECE, ANIMATING_MOVE
        active_buttons = [] # Reset for in-game buttons

        if game_state == 'MOVE_PIECE' and game_settings['player_types'][current_player] == 'Human':
            for piece in all_pieces:
                piece.highlight = False
                if piece.player_id == current_player and not piece.is_home:
                    potential_pos, _, _ = piece.get_potential_move_pos(dice_value)
                    if potential_pos:
                        piece.highlight = True
        else:
            for piece in all_pieces:
                piece.highlight = False

        for piece in all_pieces:
            piece.draw(SCREEN)

        # Draw the new player info panel (now on the left)
        draw_player_info_panel(SCREEN)

        # Draw the separate game UI elements (dice and buttons)
        active_buttons.extend(draw_game_ui_elements(SCREEN))


    # Update Display 
    pygame.display.flip()

# Quit Pygame
pygame.quit()
print("Game window closed.")
