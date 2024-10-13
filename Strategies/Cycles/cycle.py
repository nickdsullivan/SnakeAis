"""
Cycle strat is knowing a hamiltonian cycle in the board and follow it.

This is NP complete so I am going to implement one on a board without walls

"""

class Strategy:
    def __init__(self):
        self.found_cycle = False
        self.cycle = {}
        pass


    def update(self,board,snake):
        if not self.found_cycle:
            self.find_cycle(board,snake)
            self.found_cycle = False


        return self.cycle[snake.head.location]  # this may not work all the time for all starting positions so add later

    def find_cycle(self,board,snake):
        current = (1,1)
        while current[1] < board.height -3:

           
            self.cycle[current] = (0,-1)
            current = self.down(current)
            
            for i in range(board.width-4):
               
                self.cycle[current] = (-1,0)
                current = self.right(current)

            self.cycle[current] = (0,-1)
            current = self.down(current)
            
            for i in range(board.width-4):
                self.cycle[current] = (1,0)
                current = self.left(current)
        self.cycle[current] = (0,-1)
        current = self.down(current)
            





                
        for i in range(board.width-3):
            self.cycle[current] = (-1,0)
            current = self.right(current)
            
        for i in range(board.height-3):
            self.cycle[current] = (0,1)
            current = self.up(current)
        print(current)
            
        for i in range(board.width-3):
            self.cycle[current] = (1,0)
            current = self.left(current)
            
        return 1




    def right(self,loc):
        return (loc[0] + 1, loc[1])
    def left(self,loc):
        return (loc[0] - 1, loc[1])
    def down(self,loc):
        return (loc[0], loc[1]+1)
    def up(self,loc):
        return (loc[0], loc[1]-1)
