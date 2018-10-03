import pygame
import sys
import random
from pygame.locals import *

FPS = 60
BOARD_HEIGHT = 4
BOARD_WIDTH = 4

BOX_SIZE = 100
GAP_SIZE = 5
MARGIN_SIZE = 20
INFO_SIZE = 0
WINDOW_WIDTH = (BOX_SIZE * BOARD_WIDTH) + ((GAP_SIZE * BOARD_WIDTH) - GAP_SIZE) + (MARGIN_SIZE * 2)
WINDOW_HEIGHT = (BOX_SIZE * BOARD_HEIGHT) + ((GAP_SIZE * BOARD_HEIGHT) - GAP_SIZE) + (MARGIN_SIZE * 2) + INFO_SIZE

SHUFFLE_MOVES = BOARD_HEIGHT * BOARD_WIDTH * 5
FONT_SIZE = 32
ANIMATE_SPEED = 20

ROW_INDEX = 0
CELL_INDEX = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BOX_COLOR = GREEN
FONT_COLOR = BLACK
BG_COLOR = BLUE

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

MOVES = []
SHOW_WIN = False


def main():
    global DISPLAY_SURFACE, FPSCLOCK, FONT
    pygame.init()

    FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sliding Puzzle")

    while True:
        play_game()
        play_win_screen()


def play_game():
    global BOARD, ORIGINAL_BOARD
    BOARD = [[cell + (row * BOARD_WIDTH) for cell in range(1, BOARD_WIDTH + 1)] for row in range(BOARD_HEIGHT)]
    BOARD[BOARD_HEIGHT - 1][BOARD_WIDTH - 1] = 0
    ORIGINAL_BOARD = [row[:] for row in BOARD]

    draw_board()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    move(UP)
                elif event.key == K_DOWN:
                    move(DOWN)
                elif event.key == K_LEFT:
                    move(LEFT)
                elif event.key == K_RIGHT:
                    move(RIGHT)
                elif event.key == K_s:
                    shuffle()
                elif event.key == K_z:
                    undo()
                elif event.key == K_r:
                    reset()
                elif event.key == K_RETURN:
                    game_start()

        if SHOW_WIN and BOARD == ORIGINAL_BOARD:
            print("win")
            return  # Display the win screen on win

        FPSCLOCK.tick(FPS)


def game_start():
    global SHOW_WIN
    if not SHOW_WIN:
        shuffle()
        SHOW_WIN = True


def draw_board():
    """Draws the game board"""
    DISPLAY_SURFACE.fill(BG_COLOR)
    for row in range(len(BOARD)):
        for cell in range(len(BOARD[row])):
            if BOARD[row][cell] > 0:
                x, y = get_box_position((row, cell))
                draw_box((x, y, BOX_SIZE, BOX_SIZE), BOARD[row][cell])


def get_box_position(box):
    """Returns the x and y coordinates of the specified box"""
    row = box[ROW_INDEX]
    cell = box[CELL_INDEX]

    x = MARGIN_SIZE + (BOX_SIZE * cell) + (GAP_SIZE * cell)
    y = MARGIN_SIZE + INFO_SIZE + (BOX_SIZE * row) + (GAP_SIZE * row)
    return x, y


def draw_box(rect, num):
    """Draws the rect, with the num in middle"""
    label = FONT.render(str(num), True, FONT_COLOR)
    label_rect = label.get_rect()
    box = pygame.Rect(rect)
    label_rect.center = box.center
    pygame.draw.rect(DISPLAY_SURFACE, BOX_COLOR, box)
    DISPLAY_SURFACE.blit(label, label_rect)


def move(direction):
    """Moves the appropriate box in the specified direction, if possible."""
    TOP = 0
    BOTTOM = BOARD_HEIGHT - 1
    LEFTMOST = 0
    RIGHTMOST = BOARD_WIDTH - 1

    blank = find_blank()
    row = blank[ROW_INDEX]
    cell = blank[CELL_INDEX]

    if direction == UP and row != BOTTOM:
        value = BOARD[row + 1][cell]
        BOARD[row + 1][cell] = 0
        animate((row + 1, cell), blank, value)
        BOARD[row][cell] = value
        MOVES.append(UP)
    elif direction == DOWN and row != TOP:
        value = BOARD[row - 1][cell]
        BOARD[row - 1][cell] = 0
        animate((row - 1, cell), blank, value)
        BOARD[row][cell] = value
        MOVES.append(DOWN)
    elif direction == LEFT and cell != RIGHTMOST:
        value = BOARD[row][cell + 1]
        BOARD[row][cell + 1] = 0
        animate((row, cell + 1), blank, value)
        BOARD[row][cell] = value
        MOVES.append(LEFT)
    elif direction == RIGHT and cell != LEFTMOST:
        value = BOARD[row][cell - 1]
        BOARD[row][cell - 1] = 0
        animate((row, cell - 1), blank, value)
        BOARD[row][cell] = value
        MOVES.append(RIGHT)

    draw_board()
    pygame.display.update()


def find_blank():
    """Finds the 0 on the board. Returns a tuple: (row, cell)"""
    for row in range(len(BOARD)):
        for cell in range(len(BOARD[row])):
            if BOARD[row][cell] == 0:
                return (row, cell)
    raise Exception("Was not able to find the blank cell")


def animate(start_box, end_box, num):
    """Animates the specified box moving in the specified direction"""
    x, y = get_box_position(start_box)
    end_x, end_y = get_box_position(end_box)
    delta_x, delta_y = end_x - x, end_y - y
    if delta_x + delta_y > 0:
        x_step = y_step = ANIMATE_SPEED
    else:
        x_step = y_step = -ANIMATE_SPEED

    if delta_x != 0:
        for new_x in range(x, end_x, x_step):
            draw_board()
            draw_box((new_x, y, BOX_SIZE, BOX_SIZE), num)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    elif delta_y != 0:
        for new_y in range(y, end_y, y_step):
            draw_board()
            draw_box((x, new_y, BOX_SIZE, BOX_SIZE), num)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    else:
        raise Exception("Nothing to animate")


def play_win_screen():
    """Displays a message informing the player that they won"""
    global SHOW_WIN
    SHOW_WIN = False
    DISPLAY_SURFACE.fill(BG_COLOR)
    you_win_font = pygame.font.Font("freesansbold.ttf", 60)
    press_key_font = pygame.font.Font("freesansbold.ttf", 30)
    you_win_label = you_win_font.render("You Win!", True, FONT_COLOR)
    press_key_label = press_key_font.render("Press any key to reset", True, FONT_COLOR)
    you_win_rect = you_win_label.get_rect()
    press_key_rect = press_key_label.get_rect()
    you_win_rect.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    press_key_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    DISPLAY_SURFACE.blit(you_win_label, you_win_rect)
    DISPLAY_SURFACE.blit(press_key_label, press_key_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    return


def shuffle():
    """Shuffles the board intelligently. Does not make invalid moves, or undo last move"""
    global ANIMATE_SPEED
    TOP = 0
    BOTTOM = BOARD_HEIGHT - 1
    LEFTMOST = 0
    RIGHTMOST = BOARD_WIDTH - 1
    blank_row, blank_cell = find_blank()

    moves = []
    for i in range(0, SHUFFLE_MOVES):
        previous_move = ""
        if i > 0:
            previous_move = moves[i - 1]
        choices = []
        if blank_row != TOP and previous_move != UP:
            choices.append(DOWN)
        if blank_row != BOTTOM and previous_move != DOWN:
            choices.append(UP)
        if blank_cell != LEFTMOST and previous_move != LEFT:
            choices.append(RIGHT)
        if blank_cell != RIGHTMOST and previous_move != RIGHT:
            choices.append(LEFT)

        moves.append(random.choice(choices))

        if moves[i] == UP:
            blank_row += 1
        elif moves[i] == DOWN:
            blank_row -= 1
        elif moves[i] == LEFT:
            blank_cell += 1
        elif moves[i] == RIGHT:
            blank_cell -= 1

    normal_animate_speed = ANIMATE_SPEED
    ANIMATE_SPEED = SHUFFLE_MOVES // 4
    i = 1
    for direction in moves:
        if len(pygame.event.get(QUIT)) > 0 or pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        move(direction)
    ANIMATE_SPEED = normal_animate_speed


def undo():
    if len(MOVES) > 0:
        previous_move = MOVES.pop()
        if previous_move == UP:
            move(DOWN)
        elif previous_move == DOWN:
            move(UP)
        elif previous_move == LEFT:
            move(RIGHT)
        elif previous_move == RIGHT:
            move(LEFT)

        del MOVES[len(MOVES) - 1]  # Delete the move we just added


def reset():
    global BOARD, MOVES
    print(BOARD)
    print(ORIGINAL_BOARD)
    BOARD = [row[:] for row in ORIGINAL_BOARD]
    MOVES = []
    draw_board()
    pygame.display.update()


main()
