import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# --- Configuration ---

DIFFICULTY_SETTINGS = {
    "EASY": {"GRID_SIZE": 6, "WORD_LENGTH": 4, "WORDS": ["BOAT", "FISH", "LUCK", "STAR", "WISH"]},
    "MEDIUM": {"GRID_SIZE": 8, "WORD_LENGTH": 5, "WORDS": ["APPLE", "BRAVE", "CRANE", "HEART", "WORLD"]},
    "HARD": {"GRID_SIZE": 10, "WORD_LENGTH": 6, "WORDS": ["FLIGHT", "SECRET", "VICTOR", "PUZZLE", "JOURNEY"]}
}

STATS_FILE = "lexi_sweeper_stats.json"

# --- Helper Functions for Persistence ---

def load_stats():
    """Loads win stats from a local JSON file or returns a default structure."""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file exists but is corrupted, return default
            pass
    
    # Default stats structure
    return {
        "EASY": {"wins": 0, "games": 0},
        "MEDIUM": {"wins": 0, "games": 0},
        "HARD": {"wins": 0, "games": 0}
    }

def save_stats(stats):
    """Saves the current win stats to the local JSON file."""
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=4)
    except IOError as e:
        print(f"Error saving stats: {e}")

def generate_random_letter():
    """Generates a random uppercase English letter."""
    return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# --- Game Class ---

class LexiSweeper:
    def __init__(self, master):
        self.master = master
        master.title("Lexi-Sweeper (Minesweeper + Wordle)")
        master.resizable(False, False)
        
        self.stats = load_stats()
        self.current_difficulty = "MEDIUM"
        self.game_settings = DIFFICULTY_SETTINGS[self.current_difficulty]
        
        # Core game state
        self.target_word = ""
        self.grid_content = []
        self.cell_is_revealed = []
        self.word_slots = []
        self.target_letter_positions = []
        self.cell_buttons = []
        self.is_game_over = False
        
        # Setup UI
        self.setup_ui_layout()
        self.initialize_game()

    # --- UI Setup ---

    def setup_ui_layout(self):
        """Creates the persistent parts of the UI (stats, controls, main frame)."""
        
        self.control_frame = tk.Frame(self.master, padx=10, pady=10, bg='#2c3e50')
        self.control_frame.pack(fill='x')
        
        # Difficulty Selector
        self.difficulty_var = tk.StringVar(self.master)
        self.difficulty_var.set(self.current_difficulty)
        
        difficulty_label = tk.Label(self.control_frame, text="Difficulty:", font=('Inter', 12, 'bold'), fg='white', bg='#2c3e50')
        difficulty_label.pack(side=tk.LEFT, padx=(0, 5))

        difficulty_menu = tk.OptionMenu(self.control_frame, self.difficulty_var, *DIFFICULTY_SETTINGS.keys(), self.change_difficulty)
        difficulty_menu.config(bg='#3498db', fg='white', activebackground='#2980b9', relief=tk.FLAT)
        difficulty_menu["menu"].config(bg='white', fg='#2c3e50')
        difficulty_menu.pack(side=tk.LEFT, padx=(0, 20))

        # Reset/New Game Button
        tk.Button(self.control_frame, text="New Game", command=self.reset_game,
                  font=('Inter', 12, 'bold'), bg='#e74c3c', fg='white', relief=tk.RAISED,
                  padx=10, pady=5).pack(side=tk.RIGHT)
        
        # Word Display Area
        self.word_frame = tk.Frame(self.master, padx=10, pady=5, bg='#2c3e50')
        self.word_frame.pack(fill='x')
        tk.Label(self.word_frame, text="Target Word:", font=('Inter', 14, 'bold'), fg='#f1c40f', bg='#2c3e50').pack()
        self.word_label = tk.Label(self.word_frame, font=('Consolas', 28, 'bold'), fg='white', bg='#2c3e50', pady=5)
        self.word_label.pack()

        # Stats Label
        self.stats_label = tk.Label(self.master, font=('Inter', 10), fg='#bdc3c7', bg='#2c3e50', pady=5)
        self.stats_label.pack(fill='x', padx=10)

        # Main Grid Frame (will be updated on difficulty change)
        self.grid_container = tk.Frame(self.master, padx=10, pady=10, bg='#2c3e50')
        self.grid_container.pack()

    # --- Game Logic ---

    def change_difficulty(self, new_difficulty):
        """Updates settings and starts a new game with the chosen difficulty."""
        if self.current_difficulty != new_difficulty:
            self.current_difficulty = new_difficulty
            self.game_settings = DIFFICULTY_SETTINGS[new_difficulty]
            self.reset_game()

    def update_stats_display(self):
        """Refreshes the win/loss record shown in the UI."""
        stats = self.stats.get(self.current_difficulty, {"wins": 0, "games": 0})
        wins = stats["wins"]
        games = stats["games"]
        win_rate = (wins / games * 100) if games > 0 else 0
        self.stats_label.config(text=f"Difficulty: {self.current_difficulty} | Wins: {wins} / {games} | Win Rate: {win_rate:.1f}%")

    def initialize_game(self):
        """Sets up the grid content and state for a new game."""
        
        # Clear existing grid UI
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.is_game_over = False
        self.cell_buttons = []
        GRID_SIZE = self.game_settings["GRID_SIZE"]
        WORD_LENGTH = self.game_settings["WORD_LENGTH"]
        
        self.target_word = random.choice(self.game_settings["WORDS"])
        
        self.grid_content = [[generate_random_letter() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cell_is_revealed = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.word_slots = ["_"] * WORD_LENGTH
        self.target_letter_positions = []

        # Place the hidden word contiguously
        start_row = random.randint(0, GRID_SIZE - 1)
        start_col = random.randint(0, GRID_SIZE - WORD_LENGTH)

        for i in range(WORD_LENGTH):
            r, c = start_row, start_col + i
            self.grid_content[r][c] = self.target_word[i]
            self.target_letter_positions.append((r, c))

        # Build the grid buttons
        for r in range(GRID_SIZE):
            row_buttons = []
            for c in range(GRID_SIZE):
                btn = tk.Button(self.grid_container, text="?", width=4, height=2,
                                command=lambda r=r, c=c: self.handle_cell_click(r, c),
                                font=('Inter', 12, 'bold'), bg='#3498db', fg='white',
                                activebackground='#2980b9', relief=tk.RAISED, bd=3)
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.cell_buttons.append(row_buttons)
            
        self.word_label.config(text=" ".join(self.word_slots), fg='white')
        self.update_stats_display()

    def is_target_letter_cell(self, r, c):
        """Checks if a cell is one of the hidden word letters."""
        return (r, c) in self.target_letter_positions

    def count_adjacent_target_letters(self, r, c):
        """Counts how many neighboring cells are part of the target word."""
        count = 0
        GRID_SIZE = self.game_settings["GRID_SIZE"]
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if self.is_target_letter_cell(nr, nc):
                        count += 1
        return count

    def update_word_slots(self, r, c):
        """If a word letter is found, update the display."""
        for i, (wr, wc) in enumerate(self.target_letter_positions):
            if r == wr and c == wc:
                self.word_slots[i] = self.target_word[i]
                self.word_label.config(text=" ".join(self.word_slots))
                break

    def handle_cell_click(self, r, c):
        """Handles a click on a grid cell, initiating reveal or flood-fill."""
        if self.is_game_over or self.cell_is_revealed[r][c] == 1:
            return

        self.cell_is_revealed[r][c] = 1
        btn = self.cell_buttons[r][c]
        
        if self.is_target_letter_cell(r, c):
            # Found a target letter
            letter = self.grid_content[r][c]
            btn.config(text=letter, state=tk.DISABLED, bg='#27ae60', fg='white') # Green
            self.update_word_slots(r, c)
            self.check_win()
        else:
            # Hit a clue cell
            count = self.count_adjacent_target_letters(r, c)
            if count > 0:
                btn.config(text=str(count), state=tk.DISABLED, bg='#bdc3c7', fg='#34495e') 
            else:
                btn.config(text=" ", state=tk.DISABLED, bg='#ecf0f1') # Blank for 0 count
                self.reveal_adjacent_zeros(r, c) # Minesweeper Flood-Fill

    def reveal_adjacent_zeros(self, r, c):
        """Recursively reveals adjacent cells if count is 0 (Minesweeper flood fill)."""
        GRID_SIZE = self.game_settings["GRID_SIZE"]
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                
                # Boundary check and check if cell is already revealed
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.cell_is_revealed[nr][nc] == 0:
                    
                    if self.is_target_letter_cell(nr, nc):
                         # If flood-fill hits a letter, reveal it (win condition handles itself)
                         self.handle_cell_click(nr, nc)
                    else:
                        adj_count = self.count_adjacent_target_letters(nr, nc)
                        
                        self.cell_is_revealed[nr][nc] = 1
                        btn = self.cell_buttons[nr][nc]
                        
                        if adj_count == 0:
                            btn.config(text=" ", state=tk.DISABLED, bg='#ecf0f1')
                            self.reveal_adjacent_zeros(nr, nc) # Recurse
                        else:
                            btn.config(text=str(adj_count), state=tk.DISABLED, bg='#bdc3c7', fg='#34495e')

    def check_win(self):
        """Checks win condition and updates stats."""
        if "".join(self.word_slots) == self.target_word:
            self.is_game_over = True
            
            # Update stats
            current_stats = self.stats.get(self.current_difficulty, {"wins": 0, "games": 0})
            current_stats["wins"] += 1
            current_stats["games"] += 1
            self.stats[self.current_difficulty] = current_stats
            save_stats(self.stats)
            self.update_stats_display()

            # Disable buttons and show message
            for row in self.cell_buttons:
                for btn in row:
                    btn.config(state=tk.DISABLED)
            
            self.word_label.config(fg='#2ecc71') # Highlight word green
            messagebox.showinfo("VICTORY!", f"You've swept the board and found the word: {self.target_word}!")
            
    def reset_game(self):
        """Starts a new game, updating game count if the previous one wasn't finished."""
        if not self.is_game_over:
             # Count unfinished games as losses for the stats
            current_stats = self.stats.get(self.current_difficulty, {"wins": 0, "games": 0})
            current_stats["games"] += 1
            self.stats[self.current_difficulty] = current_stats
            save_stats(self.stats)

        self.initialize_game()


# --- Main Execution ---
if __name__ == "__main__":
    try:
        # Tkinter window setup
        root = tk.Tk()
        # Set a unified background color for the root window
        root.configure(bg='#2c3e50') 
        game = LexiSweeper(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
