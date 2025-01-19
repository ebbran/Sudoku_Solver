Sudoku Solver
This project is a Sudoku Solver and interactive Sudoku Game built with Python's tkinter library. It includes:

A Backtracking Algorithm for solving Sudoku puzzles.
A Graphical User Interface (GUI) to play, solve, and manage puzzles.
Additional features like a timer, custom puzzle generation, and solution verification.
Features
Interactive Sudoku Board:

Enter numbers directly into cells.
Highlights the selected cell.
Automatic input validation for digits (1-9).
Puzzle Solver:

Uses a backtracking algorithm to find solutions.
Displays the solution instantly on the board.
New Puzzle Generation:

Generates new Sudoku puzzles with a customizable difficulty.
Ensures puzzles are solvable.
Timer:

Countdown timer for added challenge.
Ends the game and displays the solution if time runs out.
Controls:

New Game: Generates a fresh puzzle.
Solve: Automatically solves the current puzzle.
Clear: Clears the board to start over.
Installation
Clone the Repository:

bash
git clone https://github.com/ebbran/Sudoku_Solver.git
cd Sudoku_Solver
Install Python: Ensure Python 3.7+ is installed. You can download it from python.org.

Run the Application:

bash
python sudoku.py
How to Play
Launch the application by running sudoku.py.
Use the New Game button to generate a puzzle.
Click on any cell to enter a number (1-9).
Use the Solve button to view the solution, or the Clear button to reset the board.
Complete the puzzle before the timer runs out to win!
Code Overview
1. Sudoku Solver:
The BacktrackSudokuSolver class implements a backtracking algorithm to solve Sudoku puzzles by:

Finding empty cells.
Placing valid numbers (1-9) recursively.
Backtracking when a solution isn't possible.
2. GUI:
The SudokuGUI class manages the game interface:

Constructs the game board using tkinter.
Handles user input, validation, and visual updates.
Integrates the solver for auto-solving puzzles.
3. Puzzle Generator:
Generates solvable puzzles by:

Randomly filling diagonal 3x3 grids.
Using the solver to complete the board.
Removing cells to create a playable puzzle.
Future Improvements
Add difficulty levels with varying numbers of empty cells.
Include hints for players during gameplay.
Enhance the timer functionality with pause/resume features.
Implement a scoring system based on time and accuracy.
Contributions
Feel free to fork the repository and contribute! Submit a pull request for any enhancements or bug fixes.

License
This project is licensed under the MIT License.

