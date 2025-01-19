import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from typing import List, Tuple
import copy


class BacktrackSudokuSolver:
    def solve_sudoku(self, board: List[List[str]]) -> bool:
        # Find empty cell
        empty = self.find_empty(board)
        if not empty:
            return True

        row, col = empty

        # Try digits 1-9
        for num in range(1, 10):
            # Check if number is valid in current position
            if self.is_valid(board, num, (row, col)):
                # Place the number
                board[row][col] = str(num)

                # Recursively try to solve rest of board
                if self.solve_sudoku(board):
                    return True

                # If placing number didn't lead to solution, backtrack
                board[row][col] = '.'

        return False

    def find_empty(self, board: List[List[str]]) -> Tuple[int, int]:
        # Find an empty cell (represented by '.')
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    return (i, j)
        return None

    def is_valid(self, board: List[List[str]], num: int, pos: Tuple[int, int]) -> bool:
        num_str = str(num)
        row, col = pos

        # Check row
        for j in range(9):
            if board[row][j] == num_str and j != col:
                return False

        # Check column
        for i in range(9):
            if board[i][col] == num_str and i != row:
                return False

        # Check 3x3 box
        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num_str and (i, j) != pos:
                    return False

        return True


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.cells = {}
        self.timer_running = False
        self.timer_value = 0
        self.timer_label = None
        self.selected_cell = None
        self.solution = None
        self.game_over = False
        self.TIME_LIMIT = 60  # 1 minute time limit
        self.initial_state = None  # Store initial puzzle state
        self.solver = BacktrackSudokuSolver()  # Create solver instance

        # Configure root window
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Create main container
        main_container = tk.Frame(root, bg='#f0f0f0')
        main_container.pack(padx=20, pady=20)

        # Create the timer label with modern styling
        self.timer_label = tk.Label(
            main_container,
            text="Time: 1:00",
            font=('Helvetica', 14, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.timer_label.pack(pady=(0, 10))

        # Create the game board
        self.create_board(main_container)

        # Create control buttons
        self.create_controls(main_container)

        # Bind keyboard events
        self.root.bind('<Key>', self.key_pressed)

    def create_board(self, parent):
        board_frame = tk.Frame(parent, bg='#333333', padx=2, pady=2)
        board_frame.pack()

        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(
                    board_frame,
                    borderwidth=1,
                    relief="solid",
                    width=50,
                    height=50,
                    bg='white'
                )
                cell_frame.grid_propagate(False)
                cell_frame.grid(row=i, column=j, padx=1, pady=1)

                # Create StringVar for validation
                cell_var = tk.StringVar()
                cell_var.trace('w', lambda *args, var=cell_var, i=i, j=j: self.validate_input(var, i, j))

                cell = tk.Entry(
                    cell_frame,
                    justify="center",
                    font=('Helvetica', 18),
                    bd=0,
                    highlightthickness=0,
                    textvariable=cell_var
                )
                cell.place(relx=0.5, rely=0.5, anchor="center")
                cell.bind('<FocusIn>', lambda e, i=i, j=j: self.cell_selected(i, j))
                cell.bind('<FocusOut>', lambda e, i=i, j=j: self.cell_focus_out(i, j))

                self.cells[(i, j)] = (cell, cell_var)

                # Thicker borders for 3x3 boxes
                if i % 3 == 0 and i != 0:
                    cell_frame.grid(pady=(3, 1))
                if j % 3 == 0 and j != 0:
                    cell_frame.grid(padx=(3, 1))

    def create_controls(self, parent):
        controls_frame = tk.Frame(parent, bg='#f0f0f0')
        controls_frame.pack(pady=20)

        button_style = {
            'font': ('Helvetica', 10),
            'width': 12,
            'height': 2,
            'bd': 0,
            'relief': 'flat'
        }

        tk.Button(
            controls_frame,
            text="New Game",
            command=self.load_sample,
            bg='#4CAF50',
            fg='white',
            **button_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls_frame,
            text="Solve",
            command=self.solve_current,
            bg='#2196F3',
            fg='white',
            **button_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls_frame,
            text="Clear",
            command=self.clear_board,
            bg='#f44336',
            fg='white',
            **button_style
        ).pack(side=tk.LEFT, padx=5)

    def validate_input(self, var, i, j):
        value = var.get()
        if value:
            # Only allow single digits 1-9
            if not value[-1].isdigit() or len(value) > 1 or value == '0':
                var.set(value[:-1])
            # Check if this cell was part of the initial puzzle
            elif self.initial_state and self.initial_state[i][j] != '.':
                var.set(self.initial_state[i][j])

    def cell_selected(self, i: int, j: int):
        if not self.game_over:
            self.selected_cell = (i, j)
            # Highlight selected cell
            self.cells[self.selected_cell][0].config(bg='#e1f5fe')

    def cell_focus_out(self, i: int, j: int):
        # Remove highlight
        self.cells[(i, j)][0].config(bg='white')

    def solve_current(self):
        if not self.solution:
            # Get current board state
            current_board = self.get_board()
            # Create a copy to solve
            board_to_solve = copy.deepcopy(current_board)
            # Try to solve it
            if self.solver.solve_sudoku(board_to_solve):
                self.solution = board_to_solve
            else:
                messagebox.showinfo("Error", "This puzzle has no solution!")
                return

        self.timer_running = False
        self.game_over = True
        self.set_board(self.solution)
        self.disable_all_cells()
        messagebox.showinfo("Solution", "Here's the solution for the puzzle!")

    def update_timer(self):
        if self.timer_running and not self.game_over:
            if self.timer_value > 0:
                self.timer_value -= 1
                minutes = self.timer_value // 60
                seconds = self.timer_value % 60
                self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
                self.root.after(1000, self.update_timer)
            else:
                self.game_over = True
                self.timer_running = False
                self.show_game_over()

    def show_game_over(self):
        current_board = self.get_board()
        if self.check_solution(current_board):
            messagebox.showinfo("Congratulations!", "You won! You solved the puzzle correctly!")
        else:
            messagebox.showinfo("Time's Up!", "Game Over! Here's the solution:")
            self.set_board(self.solution)
            self.disable_all_cells()

    def disable_all_cells(self):
        for cell, _ in self.cells.values():
            cell.config(state='disabled')

    def enable_all_cells(self):
        for cell, _ in self.cells.values():
            cell.config(state='normal')

    def set_initial_state(self, board):
        self.initial_state = copy.deepcopy(board)
        # Set background color for initial numbers
        for i in range(9):
            for j in range(9):
                if board[i][j] != '.':
                    self.cells[(i, j)][0].config(bg='#f5f5f5')

    def check_solution(self, board: List[List[str]]) -> bool:
        for i in range(9):
            for j in range(9):
                if board[i][j] != self.solution[i][j]:
                    return False
        return True

    def generate_puzzle(self) -> Tuple[List[List[str]], List[List[str]]]:
        # Start with empty grid
        empty_grid = [['.' for _ in range(9)] for _ in range(9)]

        # Fill diagonal boxes first for better generation
        for box in range(3):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for i in range(3):
                for j in range(3):
                    empty_grid[box * 3 + i][box * 3 + j] = str(numbers.pop())

        # Solve the rest using backtracking
        self.solver.solve_sudoku(empty_grid)
        solution = copy.deepcopy(empty_grid)

        # Remove numbers to create puzzle
        cells_to_remove = 40  # Adjust difficulty by changing this number
        while cells_to_remove > 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if empty_grid[i][j] != '.':
                empty_grid[i][j] = '.'
                cells_to_remove -= 1

        return empty_grid, solution

    def load_sample(self):
        self.clear_board()
        self.game_over = False
        self.enable_all_cells()

        puzzle, self.solution = self.generate_puzzle()
        self.set_initial_state(puzzle)
        self.set_board(puzzle)

        self.timer_value = self.TIME_LIMIT
        self.timer_running = True
        self.update_timer()

    def get_board(self) -> List[List[str]]:
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[(i, j)][0].get()
                row.append(value if value else '.')
            board.append(row)
        return board

    def set_board(self, board: List[List[str]]):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)][1].set('')  # Clear using StringVar
                if board[i][j] != '.':
                    self.cells[(i, j)][1].set(board[i][j])

    def clear_board(self):
        for cell, var in self.cells.values():
            var.set('')
            cell.config(bg='white')
        self.timer_running = False
        self.timer_value = self.TIME_LIMIT
        self.timer_label.config(text=f"Time: 1:00")
        self.game_over = False
        self.solution = None
        self.initial_state = None

    def key_pressed(self, event):
        if self.selected_cell and not self.game_over and event.char in '123456789':
            i, j = self.selected_cell
            if not self.initial_state or self.initial_state[i][j] == '.':
                self.cells[self.selected_cell][1].set(event.char)

                current_board = self.get_board()
                if all('.' not in row for row in current_board):
                    if self.check_solution(current_board):
                        self.game_over = True
                        self.timer_running = False
                        messagebox.showinfo("Congratulations!", "You won! You solved the puzzle correctly!")


def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()