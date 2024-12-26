import tkinter as tk
from tkinter import messagebox

def create_sudoku_board():
    # Create the main window
    window = tk.Tk()
    window.title("Sudoku")

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
                bg="black" if (row // 3 + col // 3) % 2 == 0 else "white",
                highlightbackground="blue",
                highlightthickness=2
            )
            frame.grid(row=row, column=col, padx=(2 if col % 3 == 0 else 1), pady=(2 if row % 3 == 0 else 1))

            # Create the Entry widget inside the frame
            entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
            entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    # Add a button to validate the Sudoku
    def validate_sudoku():
        try:
            # Collect the values from the grid
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

            # Simple validation for now (e.g., check for duplicates)
            if is_valid_sudoku(board):
                messagebox.showinfo("Sudoku", "The Sudoku board is valid!")
            else:
                messagebox.showerror("Sudoku", "The Sudoku board is invalid!")
        except ValueError:
            messagebox.showerror("Error", "Please enter numbers only.")

    def is_valid_sudoku(board):
        # Check rows, columns, and 3x3 subgrids for duplicates
        def is_valid_group(group):
            numbers = [num for num in group if num != 0]
            return len(numbers) == len(set(numbers))

        for i in range(9):
            if not is_valid_group(board[i]):  # Check rows
                return False
            if not is_valid_group([board[j][i] for j in range(9)]):  # Check columns
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


    middle_button = tk.Button(window, text=">", font=("Arial", 14), command=validate_sudoku)
    middle_button.grid(row=4, column=10, rowspan=2, padx=10)

    validate_button = tk.Button(window, text="Validate", command=validate_sudoku)
    validate_button.grid(row=10, column=0, columnspan=9, pady=10)


    window.mainloop()

# Run the function to create the Sudoku board
create_sudoku_board()
