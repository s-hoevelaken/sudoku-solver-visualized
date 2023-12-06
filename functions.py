import pygame
import sys
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
        return grid
    else:
        row, col = selected_cell

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku_using_backtracking(grid):
                return grid

            grid[row][col] = 0

    return False


def draw_grid(window, width, height, black):
    cell_size = width // 9
    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(window, black, (0, i * cell_size), (width, i * cell_size), thickness)
        pygame.draw.line(window, black, (i * cell_size, 0), (i * cell_size, height), thickness)

def draw_selected_cell(window, selected_cell, width, black):
    if selected_cell is not None:
        i, j = selected_cell
        cell_size = width // 9
        pygame.draw.rect(window, (0, 128, 255), (j * cell_size, i * cell_size, cell_size, cell_size), 3)

def draw_numbers(window, grid, width, black):
    font = pygame.font.Font(None, 36)
    cell_size = width // 9

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, black)
                x = j * cell_size + (cell_size - text.get_width()) // 2
                y = i * cell_size + (cell_size - text.get_height()) // 2
                window.blit(text, (x, y))


def solve_sudoku_using_backtracking_with_animation(grid, window, black, white, width, height):
    selected_cell = find_empty_cell(grid)

    if not selected_cell:
        return True
    else:
        row, col = selected_cell

    clock = pygame.time.Clock()
    animation_speed = 10

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            window.fill(white)
            draw_grid(window, width, height, black)
            draw_numbers(window, grid, width, black)
            draw_selected_cell(window, (row, col), width, black)
            pygame.display.flip()

            clock.tick(animation_speed)

            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if solve_sudoku_using_backtracking_with_animation(grid, window, black, white, width, height):
                return True

            grid[row][col] = 0

    return False



def show_mistake_prompt(window, black, white, width, height):
    font = pygame.font.Font(None, 36)
    text = font.render("Your board has mistakes. Choose an action:", True, black)
    rect = text.get_rect(center=(width // 2, height // 2 - 50))
    window.blit(text, rect)

    options = ["Reset the board completely", "Go back to the last correct board and keep trying", "Solve last correct board"]
    button_height = 50
    button_width = 603
    button_start_y = height // 2 + 20

    for i, option in enumerate(options):
        button_rect = pygame.Rect((width - button_width) // 2, button_start_y + i * button_height, button_width, button_height)
        pygame.draw.rect(window, white, button_rect)
        pygame.draw.rect(window, black, button_rect, 2)

        text = font.render(option, True, black)
        text_rect = text.get_rect(center=button_rect.center)
        window.blit(text, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    button_rect = pygame.Rect((width - button_width) // 2, button_start_y + i * button_height, button_width, button_height)
                    if button_rect.collidepoint(x, y):
                        return i + 1