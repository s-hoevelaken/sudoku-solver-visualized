from functions import draw_grid, draw_selected_cell, draw_numbers, solve_sudoku_using_backtracking, is_safe, find_empty_cell, solve_sudoku_using_backtracking_with_animation, show_mistake_prompt
import pygame
import sys
import copy
import time


pygame.init()

width, height = 603, 603
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku!!")

white = (255, 255, 255)
black = (0, 0, 0)

initial_grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]


grid_to_solve = copy.deepcopy(initial_grid)

solved_successfully = solve_sudoku_using_backtracking(grid_to_solve)

if not solved_successfully:
    print("The provided Sudoku puzzle has no solution.")
    pygame.quit()
    sys.exit()


player_grid = [row[:] for row in initial_grid]

selected_cell = 0,0
mistake_count = 0
solving = False
last_correct_grid = []
has_mistakes = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cell_size = width // 9
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_cell = (mouseY // cell_size, mouseX // cell_size)
        elif event.type == pygame.KEYDOWN:
            i, j = selected_cell
            if event.key == pygame.K_SPACE:
                if has_mistakes:
                    choice = show_mistake_prompt(window, black, white, width, height)
                    if choice == 1:
                        player_grid = [row[:] for row in initial_grid]
                        mistake_count = 0
                        has_mistakes = False
                    elif choice == 2:
                        player_grid = copy.deepcopy(last_correct_grid)
                        mistake_count = 0
                        has_mistakes = False
                    elif choice == 3:
                        player_grid = copy.deepcopy(last_correct_grid)
                        solving = True
                else:
                    solving = True
            elif event.key == pygame.K_BACKSPACE and player_grid[i][j] != 0 and initial_grid[i][j] == 0:
                player_grid[i][j] = 0
            elif selected_cell is not None and pygame.K_1 <= event.key <= pygame.K_9:
                if initial_grid[i][j] == 0 and is_safe(player_grid, i, j, int(pygame.key.name(event.key))):
                    if int(pygame.key.name(event.key)) != solved_successfully[i][j]:
                        if has_mistakes is False:
                            last_correct_grid = copy.deepcopy(player_grid)
                            has_mistakes = True
                        mistake_count += 1
                    player_grid[i][j] = int(pygame.key.name(event.key))
                else:
                    mistake_count += 1


    window.fill(white)

    if solving:
        if solve_sudoku_using_backtracking_with_animation(player_grid, window, black, white, width, height):
            solving = False
            print('Congratulations! You solved the Sudoku.')
            print(f"Mistakes made: {mistake_count}")
            time.sleep(3)
            pygame.quit()
            sys.exit()

    draw_grid(window, width, height, black)
    draw_numbers(window, player_grid, width, black)
    draw_selected_cell(window, selected_cell, width, black)

    pygame.display.flip()

    if player_grid == solved_successfully:
        print('Congratulations! You solved the Sudoku.')
        print(f"Mistakes made: {mistake_count}")
        pygame.quit()
        sys.exit()