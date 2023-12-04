def print_board(grid):
    for row in grid:
        print(row)

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None


def used_in_row(grid, row, num):
    return num in grid[row]


def used_in_col(grid, col, num):
    return num in [grid[row][col] for row in range(9)]

def used_in_subgrid(grid, start_row, start_col, num):
    return num in [
        grid[i][j] for i in range(start_row, start_row + 3)
                    for j in range(start_col, start_col + 3)
    ]

def is_safe(grid, row, col, num):
    return (
        not used_in_row(grid, row, num) and
        not used_in_col(grid, col, num) and
        not used_in_subgrid(grid, row - row % 3, col - col % 3, num)
    )

def solve_sudoku_using_backtracking(grid):
    selected_cell = find_empty_cell(grid)

    if not selected_cell:
        return True

    row, col = selected_cell

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku_using_backtracking(grid):
                return True

            grid[row][col] = 0

    return False