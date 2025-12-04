🧠 Lexi-Sweeper (Minesweeper + Wordle)

Lexi-Sweeper is a unique desktop puzzle game developed in Python using Tkinter. It combines the grid exploration and adjacency clue mechanics of Minesweeper with the objective of revealing a hidden word, inspired by Wordle.

Instead of bombs, you are searching for letters that form a contiguous secret word. Clicking a non-letter cell reveals a number indicating how many adjacent cells (neighbors) contain a letter belonging to the hidden target word.

✨ Features

Hybrid Gameplay: Unique blend of grid traversal (Minesweeper) and word assembly (Wordle).

Difficulty Settings: Choose from Easy, Medium, and Hard, which adjust the grid size and word length.

Persistent Statistics: Win/loss records and win rates are tracked and saved locally for each difficulty level in lexi_sweeper_stats.json.

Minesweeper Flood-Fill: Zero-clue cells automatically clear adjacent cells until a numbered clue or a target letter is encountered.

User-Friendly GUI: Simple, responsive interface built with Tkinter.

💻 Prerequisites

To run this application, you need:

Python 3.x

Tkinter: Tkinter is usually included with standard Python installations, but if you encounter issues, you may need to install it separately (e.g., sudo apt-get install python3-tk on Linux).

🚀 Installation and Setup

Download the File: Save the provided Python code as lexi_sweeper_enhanced.py.

Run the Game: Open your terminal or command prompt, navigate to the directory where you saved the file, and execute the following command:

python lexi_sweeper_enhanced.py


The game window should open immediately. The game will automatically create the lexi_sweeper_stats.json file in the same directory to store your progress.

🕹️ How to Play

Start a Game: The game starts immediately on the Medium difficulty. You can change the difficulty using the dropdown menu at the top.

Objective: Reveal all the letters of the Target Word displayed above the grid.

Clicking Cells:

Click a Cell: Click any cell on the grid (marked with ?).

Result 1: Target Letter: If the cell contains a letter of the secret word, the letter is revealed (in green) and fills the corresponding slot in the Target Word display.

Result 2: Clue Number (1-8): If the cell is a random letter, it turns gray and reveals a number. This number tells you exactly how many of its 8 neighboring cells contain a target letter.

Result 3: Zero Clue: If the cell reveals a 0 (blank), it means none of its 8 neighbors contain a target letter. The game automatically reveals all adjacent zero-clue areas (Minesweeper flood-fill).

Winning: The game is won when the Target Word display is completely filled with the correct letters.

New Game: Use the "New Game" button to reset the board, which also updates your statistics
