"""
Cycle strat is knowing a hamiltonian cycle in the board and follow it.

This is NP complete so I am going to implement one on a board without walls.

"""
import time
import math
from Directional_Node import DNode
class Strategy:
    def __init__(self):
        self.found_cycle = False
        self.cycle = {}

        self.DIR = {
            "UP":(0,1),
            "DOWN":(0,-1),
            "RIGHT":(-1,0),
            "LEFT":(1,0),
        }
        self.first = True

        self.dir2str = {
            (0,1):"UP",
            (0,-1):"DOWN",
            (-1,0):"RIGHT",
            (1,0):"LEFT",
        }


    def update(self,board,snake):
        self.board = board
        self.snake = snake
        if self.first:
            self.two_by_two(board,(3,3))
            self.first = False
        
        goal = self.get_apple_location(board)
        if goal not in self.cycle:
            self.prune(self.snake)
            result = self.find_cycle(board,snake,goal)
            self.found_cycle = True
            if self.found_cycle:
                self.found_cycle = False
                self.add_random()



        return self.cycle[snake.head.location].direction  # this may not work all the time for all starting positions so add later

   
    def add_random(self):
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.get_square((x,y)) == self.board.TILES["EMPTY"]:
                    goal=(x,y)
                    result = self.find_cycle(self.board,self.snake,goal)    
                    if result == 0:
                        return 0
                    else:
                        continue

        return 0
        


        
        

    # TIME TO PRUNE THIS IS HUGE FOR US THIS WILL MAKE IT VERY FAST
    # HURRAY
    def prune(self,snake):

        current = self.cycle[snake.tail.location]
        current = current.prev
        removable = False

        while current.location != snake.head.location:

           
            entrance_loc = current.prev.location
            exit_loc = current.next.next.location
            #self.print_cycle(self.board,self.snake)
            if current in snake or current.next.location in snake:
                    current = current.prev
                    continue

            removable = False
            try:
                if self.left(entrance_loc) == exit_loc:
                    self.cycle[entrance_loc].direction = self.DIR["LEFT"]
                    removable = True
                if self.right(entrance_loc) == exit_loc:
                    self.cycle[entrance_loc].direction = self.DIR["RIGHT"]
                    removable = True
                if self.down(entrance_loc) == exit_loc:
                    self.cycle[entrance_loc].direction = self.DIR["DOWN"]
                    removable = True
                if self.up(entrance_loc) == exit_loc:
                    self.cycle[entrance_loc].direction = self.DIR["UP"]
                    removable = True
            except:
                self.print_cycle(self.board,self.snake)
                print(entrance_loc)
                break
            if removable:
                break
            current = current.prev

        if removable:
            if current.location == self.snake.head.location or current.next.location == self.snake.head.location:
                return -2
            self.cycle[entrance_loc].next = self.cycle[exit_loc]
            self.cycle[exit_loc].prev = self.cycle[entrance_loc]
            
                
            del self.cycle[current.location]
            del self.cycle[current.next.location]

            return 0
        return -1
    """
    We are going to use find a hamiltonian cycle by simply taking a left every time!
    """
    def find_cycle(self,board,snake,goal):
        

        x,y = snake.head.location
        count = 0
        loc = (x,y)

        while goal not in self.cycle:
            count = count + 1
            loc = (x,y)
           
            if count > 30:
                return -1
            if x < goal[0]:
                x = x + 1
                loc = (x,y)
                if loc in self.cycle:
                    continue
                a = self.add_2_1d(board,loc,self.DIR["RIGHT"])
                

            if x > goal[0]:
                x = x - 1
                loc = (x,y)
                if loc in self.cycle:
                    continue
                a =self.add_2_1d(board,loc,self.DIR["LEFT"])
                
                
            if y < goal[1]:

                y = y + 1
                loc = (x,y)
                if y in self.cycle:
                    continue
                a = self.add_2_1d(board,loc,self.DIR["DOWN"])
                

            if y > goal[1]:

                y =y - 1
                loc = (x,y)
                if y in self.cycle:
                    continue
                a = self.add_2_1d(board,loc,self.DIR["UP"])
        
                


            
        return 0
    
    def two_by_two(self,board,top_left):
        start = DNode(top_left,None,None,self.DIR["DOWN"]) # Top left going down
        start.next = DNode(self.down(start.location),None,start,self.DIR["RIGHT"]) # Bottom left going right
        start.next.next = DNode(self.right(start.next.location),None,start.next,self.DIR["UP"]) # Bottom Right going up
        start.next.next.next = DNode(self.up(start.next.next.location),start,start.next.next,self.DIR["LEFT"]) # Top right going left
        start.prev = start.next.next.next

        self.cycle[top_left] = start
        self.cycle[start.next.location] = start.next
        self.cycle[start.next.next.location] = start.next.next
        self.cycle[start.next.next.next.location] = start.next.next.next

    

    def add_2(self,board,loc1,loc2,direction):
        if direction == self.DIR["UP"]:
            cycle_loc1 = self.down(loc1)
            cycle_loc2 = self.down(loc2)
            enter_dir = self.DIR["UP"]
            transfer_dir = self.DIR["RIGHT"]
            exit_dir = self.DIR["DOWN"]
            


        elif direction == self.DIR["DOWN"]:
            cycle_loc1 = self.up(loc1)
            cycle_loc2 = self.up(loc2)

            enter_dir = self.DIR["DOWN"]
            transfer_dir = self.DIR["RIGHT"]
            exit_dir = self.DIR["UP"]


        elif direction == self.DIR["LEFT"]:
            cycle_loc1 = self.right(loc1)
            cycle_loc2 = self.right(loc2)

            enter_dir = self.DIR["LEFT"]
            transfer_dir = self.DIR["DOWN"]
            exit_dir = self.DIR["RIGHT"]

        elif direction == self.DIR["RIGHT"]:

            cycle_loc1 = self.left(loc1)

            cycle_loc2 = self.left(loc2)

            enter_dir = self.DIR["RIGHT"]
            transfer_dir = self.DIR["DOWN"]
            exit_dir = self.DIR["LEFT"]

        
        # if we go from 2 -> 1 then 
        if self.cycle[cycle_loc2].next == self.cycle[cycle_loc1]:
            transfer_dir = self.opposite(transfer_dir)
            self.cycle[loc1] = DNode(loc1, None, None, direction=exit_dir)
            self.cycle[loc2] = DNode(loc2,None,None, direction=transfer_dir)
            # print("\n"*2)
            # print("?")
            # print("Start")
            # print(f"Direction: {self.dir2str[direction]}")
            # print(f"cycle_loc1: {self.cycle[cycle_loc1]}")
            # print(f"cycle_loc2: {self.cycle[cycle_loc2]}")
            # print(f"loc1: {self.cycle[loc1]}")
            # print(f"loc2: {self.cycle[loc2]}")
            # input("")
            self.cycle[cycle_loc2].direction = enter_dir
            self.cycle[loc2].prev = self.cycle[cycle_loc2]
            self.cycle[cycle_loc2].next = self.cycle[loc2]
            self.cycle[loc1].next = self.cycle[cycle_loc1]
            self.cycle[loc1].prev = self.cycle[loc2]
            self.cycle[loc2].next = self.cycle[loc1]
            self.cycle[cycle_loc1].prev = self.cycle[loc1]
            # ("End")
            # print(f"Direction: {self.dir2str[direction]}")
            # print(f"cycle_loc1: {self.cycle[cycle_loc1]}")
            # print(f"cycle_loc2: {self.cycle[cycle_loc2]}")
            # print(f"loc1: {self.cycle[loc1]}")
            # print(f"loc2: {self.cycle[loc2]}")
            # input("")

        elif self.cycle[cycle_loc1].next == self.cycle[cycle_loc2]:
            # same as if cycle_dir2 == self.DIR["DOWN"] or (cycle_dir1 == self.DIR["RIGHT"] and cycle_dir2 == self.DIR["RIGHT"])
            

            
            self.cycle[loc1] = DNode(loc1, None, None, direction=transfer_dir)
            self.cycle[loc2] = DNode(loc2,None,None, direction=exit_dir)
            # print("\n"*2)
            # print("!")
            # print("Start")
            # print(f"Direction: {self.dir2str[direction]}")
            # print(f"cycle_loc1: {self.cycle[cycle_loc1]}")
            # print(f"cycle_loc2: {self.cycle[cycle_loc2]}")
            # print(f"loc1: {self.cycle[loc1]}")
            # print(f"loc2: {self.cycle[loc2]}")
            # input("")
            self.cycle[cycle_loc1].direction = enter_dir
            self.cycle[loc1].prev = self.cycle[cycle_loc1]
            self.cycle[cycle_loc1].next = self.cycle[loc1]
            self.cycle[loc2].next = self.cycle[cycle_loc2]
            self.cycle[loc2].prev = self.cycle[loc1]
            self.cycle[loc1].next = self.cycle[loc2]
            self.cycle[cycle_loc2].prev = self.cycle[loc2]
            # print("End")
            # print(f"Direction: {self.dir2str[direction]}")
            # print(f"cycle_loc1: {self.cycle[cycle_loc1]}")
            # print(f"cycle_loc2: {self.cycle[cycle_loc2]}")
            # print(f"loc1: {self.cycle[loc1]}")
            # print(f"loc2: {self.cycle[loc2]}")
            # input("")
        else:
            # THIS LOCATION IS INVALID MUST SKIP
            return -1

        return 0
        

            
    def opposite(self,dir):
        if dir == self.DIR["LEFT"]:
            return  self.DIR["RIGHT"]
        if dir == self.DIR["RIGHT"]:
            return  self.DIR["LEFT"]
        if dir == self.DIR["UP"]:
            return  self.DIR["DOWN"]
        if dir == self.DIR["DOWN"]:
            return  self.DIR["UP"]


    def get_apple_location(self,board):
        for x in range(board.width):
            for y in range(board.height):
                if board.get_square((x,y)) == board.TILES["APPLE"]:
                    return(x,y)

    def to_string(self,head):
        start = self.cycle[head.location]
        result = ""
        result = result + str(start) + "\n"
        current = start.next 
        while current != start:
             result = result + str(current) + "\n"
             current = current.next
        return result





            





        



    def is_valid(self,board,loc):
        if board.get_square(loc) == board.TILES["APPLE"] or board.get_square(loc) == board.TILES["EMPTY"]:
            return True
        return False
    def right(self,loc):
        return (loc[0] + 1, loc[1])
    def left(self,loc):
        return (loc[0] - 1, loc[1])
    def down(self,loc):
        return (loc[0], loc[1]+1)
    def up(self,loc):
        return (loc[0], loc[1]-1)



    """
    If statement hell
    """

    def add_2_1d(self,board,x,direction):
        if direction == self.DIR["UP"]:
            candidate = self.left(x)
            # Check if the left_candidate is in bounds
            if self.is_valid(board,candidate):
                # Check if left candiate is not already in our cycle
                if candidate not in self.cycle:
                    # Check if it is valid to add to the cycle
                    if self.down(x) in self.cycle and self.down(candidate) in self.cycle:
                        if self.cycle[self.down(x)].next == self.cycle[self.down(candidate)] or self.cycle[self.down(candidate)].next == self.cycle[self.down(x)]:
                            return self.add_2(board,candidate,x,direction)

            candidate = self.right(x)
            
            # Check if the left_candidate is in bounds
            if self.is_valid(board,candidate):
                # Check if left candiate is not already in our cycle
                if candidate not in self.cycle:
                    # Check if it is valid to add to the cycle
                    if self.down(x) in self.cycle and self.down(candidate) in self.cycle:
                        if self.cycle[self.down(x)].next == self.cycle[self.down(candidate)] or self.cycle[self.down(candidate)].next == self.cycle[self.down(x)]:

                            return self.add_2(board,x,candidate,direction)

        if direction == self.DIR["DOWN"]:
            candidate = self.left(x)
            # Check if the left_candidate is in bounds
            if self.is_valid(board,candidate):
                # Check if left candiate is not already in our cycle
                if candidate not in self.cycle:
                    # Check if it is valid to add to the cycle
                    if self.up(x) in self.cycle and self.up(candidate) in self.cycle:
                        if self.cycle[self.up(x)].next == self.cycle[self.up(candidate)] or self.cycle[self.up(candidate)].next == self.cycle[self.up(x)]:

                            return self.add_2(board,candidate,x,direction)

            candidate = self.right(x)
            # Check if the left_candidate is in bounds
            if self.is_valid(board,candidate):
                # Check if left candiate is not already in our cycle
                if candidate not in self.cycle:
                    # Check if it is valid to add to the cycle
                    if self.up(x) in self.cycle and self.up(candidate) in self.cycle:
                        if self.cycle[self.up(x)].next == self.cycle[self.up(candidate)] or self.cycle[self.up(candidate)].next == self.cycle[self.up(x)]:
                            return self.add_2(board,x,candidate,direction)
                    

        if direction == self.DIR["LEFT"]:
            candidate = self.up(x)
            # Check if the left_candidate is in bounds
            if self.is_valid(board,candidate):
                # Check if left candiate is not already in our cycle
                if candidate not in self.cycle:
                    # Check if it is valid to add to the cycle
                    if self.right(x) in self.cycle and self.right(candidate) in self.cycle:
                        if self.cycle[self.right(x)].next == self.cycle[self.right(candidate)] or self.cycle[self.right(candidate)].next == self.cycle[self.right(x)]:
                            return self.add_2(board,candidate,x,direction)

            candidate = self.down(x)
            # Check if the left_candidate is in bounds
            if self.is_valid(board,candidate):
                # Check if left candiate is not already in our cycle
                if candidate not in self.cycle:
                    # Check if it is valid to add to the cycle
                    if self.right(x) in self.cycle and self.right(candidate) in self.cycle:
                        if self.cycle[self.right(x)].next == self.cycle[self.right(candidate)] or self.cycle[self.right(candidate)].next == self.cycle[self.right(x)]:
                            return self.add_2(board,x,candidate,direction)
        
        if direction == self.DIR["RIGHT"]:
            candidate = self.up(x)
            if self.is_valid(board,candidate):
                if candidate not in self.cycle:
                    if self.left(x) in self.cycle and self.left(candidate) in self.cycle:
                        if self.cycle[self.left(x)].next == self.cycle[self.left(candidate)] or self.cycle[self.left(candidate)].next == self.cycle[self.left(x)]:
                            return self.add_2(board,candidate,x,direction)
            candidate = self.down(x)
            if self.is_valid(board,candidate):
                if candidate not in self.cycle:
                    if self.left(x) in self.cycle and self.left(candidate) in self.cycle:
                        if self.cycle[self.left(x)].next == self.cycle[self.left(candidate)] or self.cycle[self.left(candidate)].next == self.cycle[self.left(x)]:

                            return self.add_2(board,x,candidate,direction)


        return -1
    


    
    def get_dir_snake(self,loc1,loc2):
        if loc1[0] > loc2[0]:
            return (1,0)
        if loc1[0] < loc2[0]:
            return (-1,0)
        if loc1[1] > loc2[1]:
            return (0,1)
        if loc1[1] < loc2[1]:
            return (0,-1)
        
    def print_cycle(self,board,snake):
        goal = self.get_apple_location(board)
        current= self.cycle[snake.head.location]
        print(snake.head.location)
        print(f"{current} HEAD")
        current =current.next
        count = 0
        while current.location !=  snake.head.location:
            count = count +1

            print(current)


            current = current.next
            if count > 20:
                print("Something is wrong")
                break
        print(f"{current} HEAD")