import tkinter as tk
from tkinter import messagebox

def create_sudoku_board():
    # Create the main window
    window = tk.Tk()
    window.title("Sudoku Using CSP")

    # Create a 9x9 grid of Entry widgets within 3x3 subgrids
    entries = []
    for row in range(9):
        row_entries = []
        for col in range(9):
            # Create a frame for each 3x3 block
            frame = tk.Frame(
                window,
                width=50,
                height=50,
                padx=1,
                pady=1,
                bg="black" if (row // 3 + col // 3) % 2 == 0 else "grey"
            )
            frame.grid(row=row, column=col, padx=(2 if col % 3 == 0 else 1), pady=(2 if row % 3 == 0 else 1))

            # Create the Entry widget inside the frame
            entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
            entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    # Function to validate the Sudoku board
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

    # Function to check Sudoku validity
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

    # Helper function to check valid numbers for a cell
    def check_row(board, r, c):
        arrx = board[r]
        arry = [board[i][c] for i in range(9)]
        st = (r // 3) * 3
        endr = st + 3
        stc = (c // 3) * 3
        endc = stc + 3
        arrxy = [board[row][col] for row in range(st, endr) for col in range(stc, endc)]
        return arrx, arrxy, arry

    # Recursive CSP function
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

    # CSP function
    def CSP(board):
        result = [None]
        CSP_helper(board, 0, 0, result)
        return result[0]

    # Function to solve Sudoku
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

    # Buttons for validation and solving
    validate_button = tk.Button(window, text="Validate", command=validate_sudoku)
    validate_button.grid(row=10, column=0, columnspan=4, pady=10)

    solve_button = tk.Button(window, text="Solve", command=solve_sudoku)
    solve_button.grid(row=10, column=5, columnspan=4, pady=10)

    window.mainloop()

# Run the function to create the Sudoku board
create_sudoku_board()
