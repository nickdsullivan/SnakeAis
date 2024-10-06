"""
Simple first strategy.
Simply use DFS to find the closest apple.
"""
from Node import Node
import random 
class Strategy:
    def __init__(self):
        self.directions = []
        self.already_calculated = False
        self.head = None
        self.tail = None
    def update(self,board,snake):
        head = snake.head
        self.head = Node(head.location,None,None)
        current_node = self.head
        current_s1_node = head
        while current_s1_node.next != None:
            current_node.next = Node(current_s1_node.next.location, None, current_node)
            current_node = current_node
            current_s1_node = current_s1_node.next
        return self.get_single_direction(board,self.head)
    def get_single_direction(self,board,head):
        if self.directions == None:
            self.directions = self.calc_directions(board,head)
            return random.choice(
                    [
                        (1,0),
                        (0,1),
                        (-1,0),
                        (0,-1),
                    ]
                )

        if len(self.directions) == 0:
            self.directions = self.calc_directions(board,head)
            if self.directions == None:
                return random.choice(
                    [
                        (1,0),
                        (0,1),
                        (-1,0),
                        (0,-1),
                    ]
                )
        
        result = self.directions.pop(0)

        return result


    def calc_directions(self,board,head):
        goal = (0,0)
        for x in range(board.width):
            for y in range(board.height):
                if board.get_square((x,y)) == board.TILES["APPLE"]:
                    goal = (x,y)
                    last_node = self.dfs(board,head,goal)
                    if last_node == None:
                        return None

                    return self.get_directions_from_path(head,last_node)
        return None

    def get_directions_from_path(self,head,goal):
        current_node = goal
        while current_node.prev != head:
            current_node.prev.next = current_node
            current_node = current_node.prev
        head.next = current_node
        directions = []
        current_node = head
        while current_node != goal:
            directions.append(self.get_direction(current_node.location,current_node.next.location))
            current_node = current_node.next
        return directions


    def get_direction(self,loc: tuple, loc2: tuple):
        return loc[0]- loc2[0], loc[1]-loc2[1]

       
    def dfs(self,board,head,goal):
        path_node = None
        visited = []
        queue = []
        moves = self.get_moves(board,head.location)
        for move in moves:
            queue.append(Node(move, next= None,prev=head))
        if len(queue) == 0:
            return None
        while len(queue) != 0:

            current = queue.pop(0)

            if current.location in visited:
                continue
            visited.append(current.location)
            if board.get_square(current.location) ==  board.TILES["SNAKE"] or board.get_square(current.location) ==  board.TILES["WALL"]:
                continue
            if current.location ==  goal:

                return current
            moves = self.get_moves(board,current.location)
        
            
            for move in moves:
                
                queue.append(Node(move, next= None, prev = current))
                
        return current

            
    def get_moves(self,board,start):
        results = []
        if board.get_square((start[0]+ 1, start[1])) == board.TILES["APPLE"] or board.get_square((start[0]+ 1, start[1])) == board.TILES["EMPTY"]:
            results.append((start[0]+ 1, start[1]))


        if board.get_square((start[0] -1, start[1])) == board.TILES["APPLE"] or board.get_square((start[0]-1, start[1])) == board.TILES["EMPTY"]:
            results.append((start[0]- 1, start[1]))

        if board.get_square((start[0], start[1]+1)) == board.TILES["APPLE"] or board.get_square((start[0], start[1]+1)) == board.TILES["EMPTY"]:
            results.append((start[0], start[1]+1))

        if board.get_square((start[0], start[1]-1)) == board.TILES["APPLE"] or board.get_square((start[0], start[1]-1)) == board.TILES["EMPTY"]:
            results.append((start[0], start[1]-1))
        
        return results

