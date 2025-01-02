import tkinter as tk
from tkinter import messagebox
import random

def create_sudoku_board():
    # Create the main window
    window = tk.Tk()
    window.title("Sudoku Using CSP")

    # Create a 9x9 grid of Entry widgets within 3x3 subgrids
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
#########################################################################################################################################################################
    
    def check_row(board, r, c):
        arrx = board[r]  
        arry = [board[i][c] for i in range(9)]  
        st = (r // 3) * 3  
        endr = st + 3  
        stc = (c // 3) * 3  
        endc = stc + 3  
        arrxy = [board[row][col] for row in range(st, endr) for col in range(stc, endc)]  
        return arrx, arrxy, arry
    
############################################################################################################################################

    def generate_random_puzzle(difficulty):
        board = [[0] * 9 for _ in range(9)]
        total_cells = 81
        empty_cells = int(total_cells * difficulty)

        for _ in range(total_cells - empty_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] != 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            value = random.randint(1, 9)
            board[row][col] = value
            if not is_valid_sudoku(board):
                board[row][col] = 0
                

        if CSP(board) is None:
                return generate_random_puzzle(difficulty)

        for r in range(9):
            for c in range(9):
                entries[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                     entries[r][c].insert(0, str(board[r][c]))

#######################################################################################################################################################################

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

#########################################################################################################################################################################
   
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

#########################################################################################################################################################################
   
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

        arrx, arrxy, arry = check_row(board, r, c)
        for i in range(1, 10):
            if i not in arrx and i not in arry and i not in arrxy:
                board[r][c] = i
                if c < 8:
                    CSP_helper(board, r, c + 1, result)
                else:
                    CSP_helper(board, r + 1, 0, result)
                board[r][c] = 0

    def CSP(board):
        result = [None]
        CSP_helper(board, 0, 0, result)
        return result[0]
    
#########################################################################################################################################################################

    # validate_button = tk.Button(window, text="Validate", command=validate_sudoku)
    # validate_button.grid(row=10, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(window, text="Solve", command=solve_sudoku)
    solve_button.grid(row=10, column=3, columnspan=3, pady=10)

    easy_button = tk.Button(window, text="Easy", command=lambda: generate_random_puzzle(0.5))
    easy_button.grid(row=11, column=0, columnspan=3, pady=10)

    medium_button = tk.Button(window, text="Medium", command=lambda: generate_random_puzzle(0.6))
    medium_button.grid(row=11, column=3, columnspan=3, pady=10)

    hard_button = tk.Button(window, text="Hard", command=lambda: generate_random_puzzle(0.75))
    hard_button.grid(row=11, column=6, columnspan=3, pady=10)

    window.mainloop()

create_sudoku_board()