import numpy as np

import random
class Board:
    def __init__(self, width = 21,height = 21):
        self.TILES = {
            "EMPTY": 0,
            "WALL": 1,
            "SNAKE": 2,
            "APPLE": 3,
            "SNAKE_HEAD": 4,
        }
        self.TILES2STR = {
            0: " ",
            1: "|",
            2: "o",
            3: "x",
            4: ">",
        }
        self.width = width
        self.height = height
        self.board = np.zeros((width,height))
        for i in range(width):
            self.board[0,i] = self.TILES["WALL"]
            self.board[width-1,i] = self.TILES["WALL"]
            self.board[i,0] = self.TILES["WALL"]
            self.board[i,width-1] = self.TILES["WALL"]
    def get_square(self,x,y):
        return self.board[x,y]
    def get_square(self,loc):
        return self.board[loc[0],loc[1]]
    def set_square(self,x,y, tile):
        self.board[x,y] = tile
    def set_square(self,loc, tile):
        self.board[loc[0],loc[1]] = tile
    def __str__(self):
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                result = result + self.TILES2STR[int(self.board[x,y])] + " "
            result = result + "\n"
        return result
    def spawn_apple(self):

        empties = []
        for x in range(self.height):
            for y in range(self.width):
                if self.board[x,y] == self.TILES["EMPTY"]:
                    empties.append((x,y))
        if len(empties) == 0:
            return 1
        self.set_square(random.choice(empties),self.TILES["APPLE"])
        return 0 





