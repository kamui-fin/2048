import pygame
from pygame.locals import *
import random
S_HEIGHT = 600 + 125
S_WIDTH = 600 + 125 + 50
BOARD_HEIGHT = 4
BOARD_WIDTH = 4
screen = pygame.display.set_mode((S_HEIGHT, S_WIDTH))
pygame.init()
pygame.font.init()
pygame.display.set_caption("h")
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e",
                         4096: "#eee4da", 8192: "#edc22e", 16384: "#f2b179",
                         32768: "#f59563", 65536: "#f67c5f", }
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2",
                   4096: "#776e65", 8192: "#f9f6f2", 16384: "#776e65",
                   32768: "#776e65", 65536: "#f9f6f2", }
font = pygame.font.SysFont("Verdana", 50, True)
class Cell:
    def __init__(self, rect, value):
        self.rect = rect
        self.value = value
        self.refresh_colors()
    def refresh_colors(self):
        if self.value:
            self.fg = pygame.Color(CELL_COLOR_DICT[self.value])
            self.bg = pygame.Color(BACKGROUND_COLOR_DICT[self.value])
        else:
            self.fg = ""
            self.bg = pygame.Color(BACKGROUND_COLOR_CELL_EMPTY)
class Board:
    def __init__(self):
        self._board = [[Cell("", 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
    def init_board(self):
        left_offset = 25
        top_offset = 25
        for h in range(BOARD_HEIGHT):
            for w in range(BOARD_WIDTH):
                self._board[h][w].rect = pygame.Rect((left_offset * h + (h * 150)) + 25,
                                                     (top_offset * w + (w * 150)) + 25, 150, 150)
        for _ in range(2):
            self.spawn_cell()
            
    def spawn_cell(self):
        random_h = random.randint(0, BOARD_HEIGHT - 1)
        random_w = random.randint(0, BOARD_WIDTH - 1)
        if not all([x.value != 0 for row in self._board for x in row]):
            while self._board[random_h][random_w].value != 0:
                random_w = random.randint(0, BOARD_WIDTH - 1)
                random_h = random.randint(0, BOARD_WIDTH - 1)
            rand_val =  random.choices([2,4],weights=[.85,.15],k=1)[0]
            self._board[random_h][random_w].value = rand_val
    def draw_board(self):
        global font
        for row in self._board:
            for cell in row:
                if cell.value == 0:
                    pygame.draw.rect(screen, cell.bg, cell.rect)
                else:
                    pygame.draw.rect(screen, cell.bg, cell.rect)
                    value_label = font.render(str(cell.value), True, cell.fg)
                    font = pygame.font.SysFont("Verdana", 55 - (len(str(cell.fg))), True)
                    screen.blit(value_label, ((cell.rect.left + 72) - 13 * len(str(cell.value)), cell.rect.top + 50))
                    score_font = pygame.font.SysFont("Verdana", 30, True)
                    score = score_font.render("Score:   " + str(self.score), True, (0,0,0))
                    screen.blit(score, (S_WIDTH / 12, 717))
        self.score = sum(x.value for row in self._board for x in row)

    def move_board(self, **kwargs):
        for i in range(4):
            for row_num in range(*kwargs["col_range"]):
                for num in range(*kwargs["row_range"]):
                    if self._board[row_num][num].value != 0 and num != kwargs["num_limit"] and row_num != kwargs["col_limit"]:
                        next_block = self._board[row_num + kwargs["col_int"]][num + kwargs["row_int"]]
                        curr_block = self._board[row_num][num]
                        if next_block.value == curr_block.value:
                            next_block.value += curr_block.value
                        elif next_block.value != 0:
                            continue
                        else:
                            next_block.value = curr_block.value
                        curr_block.value = 0
    def refresh(self):
        for row in self._board:
            for cell in row:
                cell.refresh_colors()
run = True
board = Board()
board.init_board()
clock = pygame.time.Clock()
left_info = {"col_range":(0,4,1),"row_range":(0,4,1), "col_int": -1, "row_int":0, "num_limit":-1, "col_limit":0}
up_info = {"col_range":(0,4,1),"row_range":(0,4,1), "col_int": 0, "row_int":-1, "num_limit":0, "col_limit":-1}
right_info = {"col_range":(3,-1,-1),"row_range":(0,4,1), "col_int": 1, "row_int":0, "num_limit":-1, "col_limit":3}
down_info = {"col_range":(0,4,1),"row_range":(3,-1,-1), "col_int": 0, "row_int":1, "num_limit":3, "col_limit":-1}
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                board.move_board(**left_info)
            elif event.key == K_RIGHT:
                board.move_board(**right_info)
            elif event.key == K_UP:
                board.move_board(**up_info)
            elif event.key == K_DOWN:
                board.move_board(**down_info)
            if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                board.spawn_cell()
    board.refresh()
    screen.fill(pygame.Color(BACKGROUND_COLOR_GAME))
    board.draw_board()
    pygame.display.flip()
pygame.quit()
