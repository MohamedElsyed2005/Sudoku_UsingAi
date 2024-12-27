import tkinter as tk
from tkinter import messagebox

def print_grid(arr):
    for i in range(9):
        for j in range(9):
            print(arr[i][j], end=" ")
        print()

def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if(arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False

def used_in_row(arr, row, num):
    for i in range(9):
        if(arr[row][i] == num):
            return True
    return False

def used_in_col(arr, col, num):
    for i in range(9):
        if(arr[i][col] == num):
            return True
    return False

def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if(arr[i + row][j + col] == num):
                return True
    return False

def check_location_is_safe(arr, row, col, num):
    return (not used_in_row(arr, row, num) and
            (not used_in_col(arr, col, num) and
             (not used_in_box(arr, row - row % 3,
                              col - col % 3, num))))

def is_board_valid(arr):
    for row in range(9):
        for col in range(9):
            num = arr[row][col]
            if num != 0:
                arr[row][col] = 0
                if not check_location_is_safe(arr, row, col, num):
                    arr[row][col] = num
                    return False
                arr[row][col] = num
    return True

def solve_sudoku(arr):
    l = [0, 0]
    if(not find_empty_location(arr, l)):
        return True
    row = l[0]
    col = l[1]

    for num in range(1, 10):
        if(check_location_is_safe(arr,
                                  row, col, num)):

            arr[row][col] = num

            if(solve_sudoku(arr)):
                return True

            arr[row][col] = 0
    return False

def create_sudoku_board():
    window = tk.Tk()
    window.title("Sudoku")

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
                bg="black" if (row // 3 + col // 3) % 2 == 0 else "grey",
            )
            frame.grid(row=row, column=col, padx=(2 if col % 3 == 0 else 1), pady=(2 if row % 3 == 0 else 1))

            entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
            entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    def get_board_from_entries():
        board = []
        for row_entries in entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                if value == "":
                    row.append(0)
                else:
                    try:
                        row.append(int(value))
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input! Use numbers only.")
                        return None
            board.append(row)
        return board

    def set_board_to_entries(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, str(board[i][j]))

    def solve_with_ai():
        board = get_board_from_entries()
        if board is None:
            return

        if solve_sudoku(board):
            set_board_to_entries(board)
            messagebox.showinfo("Sudoku", "Solved successfully!")
        else:
            messagebox.showerror("Sudoku", "No solution exists!")

    def validate_board():
        board = get_board_from_entries()
        if board is None:
            return

        if is_board_valid(board):
            messagebox.showinfo("Sudoku", "The board is valid!")
        else:
            messagebox.showerror("Sudoku", "The board is not valid!")

    solve_button = tk.Button(window, text="Solve with AI", command=solve_with_ai)
    solve_button.grid(row=10, column=0, columnspan=4, pady=10)

    validate_button = tk.Button(window, text="Validate Board", command=validate_board)
    validate_button.grid(row=10, column=5, columnspan=4, pady=10)

    window.mainloop()

create_sudoku_board()