import sys
import pygame
import random
import numpy as np

from constraints import *

# initialize pygame & screen
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

class Board:

    def __init__(self) -> None:
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0
    
    def final_state(self):
        ''' 
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        
        # HORIZONTAL wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        
        #desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        #asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0:
            return self.squares[1][1]
        
        return 0
            
        

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs
    
    def isfull (self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    
    def __init__(self, level=0, player=2):
         self.level = level
         self.player = player
    
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)
    
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            move = self.rnd(main_board)
            pass

        else:
            # minimax algorithim choice
            pass

        return move # row, col


class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.ai = AI()
        self.player = 1 #1-cross #2-circles
        self.gamemode = 'ai' #pvp or ai
        self.running = True
        self.show_lines()


    def show_lines(self):
        #vert lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE__WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE__WIDTH)
        #horizonatl lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE__WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE__WIDTH)

    def draw_fig(self, row, col):
        if self.player == 2:
            center = (col * SQSIZE +  SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
        
        elif self.player == 1:
            #diagoal down line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            #asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    def next_turn(self):
        self.player = self.player %2 + 1


def main():

    #game class
    game = Game()
    board = game.board
    ai = game.ai

    #gameplay loop
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row,col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
                    print(board.squares)
        
        if game.gamemode == 'ai' and game.player == ai.player:
            #update screen
            pygame.display.update()

            #ai methods
            row, col = ai.eval(board)
            
            board.mark_sqr(row, col, ai.player)
            game.draw_fig(row, col)
            game.next_turn()

        pygame.display.update()        

main()
