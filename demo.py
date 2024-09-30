import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 300, 400  # Added extra space for displaying messages
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // 3
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Fonts
font = pygame.font.Font(None, 36)

# Board variables
board = [0] * 9

# Draw grid lines
def draw_lines():
    screen.fill(BG_COLOR)
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

# Draw X or O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row * 3 + col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row * 3 + col] == -1:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Check if someone has won
def check_win():
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            return board[combo[0]]  # Return the player who won (1 or -1)
    return 0  # No one has won yet

# Check if the board is full (game draw)
def is_board_full():
    return 0 not in board

# Minimax functions for the computer's turn
def minimax(board, player):
    winner = check_win()
    if winner != 0:
        return winner * player

    move = -1
    value = -2
    for i in range(9):
        if board[i] == 0:
            board[i] = player
            score = -minimax(board, -player)
            board[i] = 0
            if score > value:
                value = score
                move = i
    if move == -1:
        return 0
    return value

def CompTurn():
    move = -1
    value = -2
    for i in range(9):
        if board[i] == 0:
            board[i] = 1
            score = -minimax(board, -1)
            board[i] = 0
            if score > value:
                value = score
                move = i
    board[move] = 1

# Handle user input
def UserTurn(pos, current_player):
    if board[pos] == 0:
        board[pos] = current_player

# Restart the game
def restart():
    global board
    board = [0] * 9
    draw_lines()
    draw_figures() 
    pygame.display.update()

# Display winner or draw and ask for new game
def display_result(result_text):
    screen.fill(BG_COLOR)
    text = font.render(result_text, True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

# Game mode selection screen
def select_game_mode():
    screen.fill(BG_COLOR)
    text_1v1 = font.render("Press 1 for 1v1", True, RED)
    text_1vComp = font.render("Press 2 for 1vComp", True, RED)
    screen.blit(text_1v1, (WIDTH // 2 - text_1v1.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(text_1vComp, (WIDTH // 2 - text_1vComp.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    
                    return '1v1'
                elif event.key == pygame.K_2:
                    
                    return '1vcomp'

# Main game loop
def main_game_loop(mode):
    draw_lines()
    draw_figures()  # Draw the initial empty board

    current_player = -1  # Player 1 starts as -1 (X), Player 2 (or Computer) as 1 (O)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]  # x
                mouseY = event.pos[1]  # y

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                pos = clicked_row * 3 + clicked_col

                if board[pos] == 0:
                    UserTurn(pos, current_player)
                    draw_figures()
                    pygame.display.update()

                    # Check for win or draw after each move
                    winner = check_win()
                    if winner == -1:
                        pygame.time.wait(500)
                        display_result("Player 1 wins!" if mode == '1v1' else "You win!")
                        pygame.time.wait(2000)
                        return
                    elif winner == 1:
                        pygame.time.wait(500)
                        display_result("Player 2 wins!" if mode == '1v1' else "Computer wins!")
                        pygame.time.wait(2000)
                        return
                    elif is_board_full():
                        pygame.time.wait(500)
                        display_result("It's a draw!")
                        pygame.time.wait(2000)
                        return

                    # Toggle turns
                    current_player *= -1

                    # If 1vComp mode and it's computer's turn, let the computer move
                    if mode == '1vcomp' and current_player == 1:
                        CompTurn()
                        draw_figures()
                        pygame.display.update()

                        # Check for computer win
                        winner = check_win()
                        if winner == 1:
                            pygame.time.wait(500)
                            display_result("Computer wins!")
                            pygame.time.wait(2000)
                            return
                        elif is_board_full():
                            pygame.time.wait(500)
                            display_result("It's a draw!")
                            pygame.time.wait(2000)
                            return

                        # After computer move, toggle back to player
                        current_player = -1

# Start the game
while True:
    mode = select_game_mode()  # Select game mode (1v1 or 1vcomp)
    restart()  # Restart game immediately to ensure board is drawn
    main_game_loop(mode)  # Play the game
