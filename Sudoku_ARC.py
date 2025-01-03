import tkinter as tk
from tkinter import messagebox
import random

def create_sudoku_board():
    window = tk.Tk()
    window.title("Sudoku Using CSP and AC-3")

    entries = []
    for row in range(9):
        row_entries = []
        for col in range(9):
            frame = tk.Frame(
                window,
                width=50,
                height=50,
                padx=1,
                pady=1,
                bg="black" if (row // 3 + col // 3) % 2 == 0 else "grey"
            )
            frame.grid(row=row, column=col, padx=(2 if col % 3 == 0 else 1), pady=(2 if row % 3 == 0 else 1))

            entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
            entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            entry.bind("<FocusOut>", lambda e, r=row, c=col: check_input(e, r, c))
            row_entries.append(entry)
        entries.append(row_entries)
    def validate_sudoku():
        try:
            board = []
            for row_entries in entries:
                row = []
                for entry in row_entries:
                    value = entry.get()
                    if value == "":
                        row.append(0)
                    else:
                        row.append(int(value))
                board.append(row)
            if is_valid_sudoku(board):
                messagebox.showinfo("Sudoku", "The Sudoku board is valid!")
            else:
                messagebox.showerror("Sudoku", "The Sudoku board is invalid!")
            return board
        except ValueError:
            messagebox.showerror("Error", "Please enter numbers only.")
    def is_valid_sudoku(board):
        def is_valid_group(group):
            numbers = [num for num in group if num != 0]
            return len(numbers) == len(set(numbers))

        for i in range(9):
            if not is_valid_group(board[i]):
                return False
            if not is_valid_group([board[j][i] for j in range(9)]):
                return False

        for box_row in range(3):
            for box_col in range(3):
                subgrid = [
                    board[r][c]
                    for r in range(box_row * 3, (box_row + 1) * 3)
                    for c in range(box_col * 3, (box_col + 1) * 3)
                ]
                if not is_valid_group(subgrid):
                    return False

        return True
    
    def check_input(event, row, col):
        value = event.widget.get()
        if not value.isdigit() or not (1 <= int(value) <= 9):
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 9.")
            event.widget.delete(0, tk.END)
        else:
            board = [[int(entry.get()) if entry.get().isdigit() else 0 for entry in row] for row in entries]
            if not is_valid_sudoku(board):
                messagebox.showerror("Invalid Input", "This number violates Sudoku rules.")
                event.widget.delete(0, tk.END)
    def AC3(board):
        domains = { (r, c): set(range(1, 10)) if board[r][c] == 0 else {board[r][c]}
                    for r in range(9) for c in range(9) }

        def get_neighbors(r, c):
            row_neighbors = [(r, col) for col in range(9) if col != c]
            col_neighbors = [(row, c) for row in range(9) if row != r]
            box_start_row, box_start_col = 3 * (r // 3), 3 * (c // 3)
            box_neighbors = [(box_start_row + i, box_start_col + j)
                             for i in range(3) for j in range(3)
                             if (box_start_row + i, box_start_col + j) != (r, c)]
            return set(row_neighbors + col_neighbors + box_neighbors)

        arcs = [(cell, neighbor) for cell in domains for neighbor in get_neighbors(*cell)]

        def revise(x, y):
            revised = False
            if len(domains[y]) == 1:
                y_value = next(iter(domains[y]))
                if y_value in domains[x]:
                    domains[x].remove(y_value)
                    revised = True
            return revised

        while arcs:
            x, y = arcs.pop(0)
            if revise(x, y):
                if not domains[x]:
                    return False
                for neighbor in get_neighbors(*x) - {y}:
                    arcs.append((neighbor, x))

        for r in range(9):
            for c in range(9):
                if len(domains[(r, c)]) == 1:
                    board[r][c] = next(iter(domains[(r, c)]))
        return True

    def CSP_helper(board, r, c, result):
        if result[0] is not None:
            return
        if r == 9:
            result[0] = [row[:] for row in board]
            return
        if board[r][c] != 0:
            if c < 8:
                CSP_helper(board, r, c + 1, result)
            else:
                CSP_helper(board, r + 1, 0, result)
            return

        for i in range(1, 10):
            if is_safe(board, r, c, i):
                board[r][c] = i
                if AC3(board):
                    if c < 8:
                        CSP_helper(board, r, c + 1, result)
                    else:
                        CSP_helper(board, r + 1, 0, result)
                board[r][c] = 0

    def is_safe(board, r, c, num):
        return num not in board[r] and num not in [board[i][c] for i in range(9)] and num not in [
            board[i][j]
            for i in range(r // 3 * 3, r // 3 * 3 + 3)
            for j in range(c // 3 * 3, c // 3 * 3 + 3)
        ]

    def CSP(board):
        result = [None]
        if AC3(board):
            CSP_helper(board, 0, 0, result)
        return result[0]

    def generate_random_puzzle(difficulty):
        filled_cells = {"easy": 35, "medium": 25, "hard": 17}[difficulty]
        board = [[0] * 9 for _ in range(9)]
        solution = CSP(board)
        if not solution:
            return generate_random_puzzle(difficulty)
        board = [row[:] for row in solution]
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        for _ in range(81 - filled_cells):
            r, c = cells.pop()
            board[r][c] = 0

        for r in range(9):
            for c in range(9):
                entries[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    entries[r][c].insert(0, str(board[r][c]))

    
    def solve_sudoku():
        try:
            board = validate_sudoku()
            if board is None:
                return
            solution = CSP(board)
            if solution is None:
                messagebox.showerror("Sudoku", "No solution exists!")
                return
            for r in range(9):
                for c in range(9):
                    entries[r][c].delete(0, tk.END)
                    if solution[r][c] != 0:
                        entries[r][c].insert(0, str(solution[r][c]))
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
    solve_button = tk.Button(window, text="Solve", command=lambda: solve_sudoku())
    solve_button.grid(row=10, column=3, columnspan=3, pady=10)
    tk.Button(window, text="Easy", command=lambda: generate_random_puzzle("easy")).grid(row=11, column=0, columnspan=3)
    tk.Button(window, text="Medium", command=lambda: generate_random_puzzle("medium")).grid(row=11, column=3, columnspan=3)
    tk.Button(window, text="Hard", command=lambda: generate_random_puzzle("hard")).grid(row=11, column=6, columnspan=3)

    window.mainloop()

create_sudoku_board()