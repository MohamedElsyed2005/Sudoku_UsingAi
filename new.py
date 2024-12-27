board = [[0, 0, 0, 0, 0, 0, 0, 6, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 5, 0, 0, 0, 0, 0],
         [0, 0, 3, 0, 0, 0, 0, 0, 0],
         [2, 1, 0, 0, 0, 0, 8, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 7, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 9, 0, 0, 0, 0, 0, 0]]

def check_row(board, r, c):
    arrx = board[r]
    arry = [board[i][c] for i in range(9)]
    st = (r // 3) * 3
    endr = st + 3
    stc = (c // 3) * 3
    endc = stc + 3
    arrxy = []
    for row in range(st, endr):
        for col in range(stc, endc):
            arrxy.append(board[row][col])
    return arrx, arrxy, arry

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
    CSP_helper(board = board,r = 0,c=0, result = result)
    return result[0]

print(CSP(board))
