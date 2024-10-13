from Node import Node

      
class Snake:
    def __init__(self, head: tuple, size: int, board, direction=(1,0)):

        self.board = board
        self.head = Node(head,None,None)
        self.size = size
        self.direction = direction
        current =  self.head
        for i in range(self.size-1):
            next_p = Node(self.move_direction(current.location, (direction[0], direction[1])),None,prev=current)
            current.next = next_p
            
            current = current.next
        
        self.tail = current

    def __contains__(self, loc: tuple):
        return loc in self.get_positions()
    def get_positions(self):

        results = []
        current = self.head
        while current != None:
            results.append(current.location)
            current = current.next
        return results
    
    def update_board(self,board):
        current =  self.head
        board.set_square(current.location, board.TILES["SNAKE_HEAD"])
        current = self.head.next
        while current != None:

            board.set_square(current.location, board.TILES["SNAKE"])
            current = current.next
            
    def move_forward(self,board):

        loc = self.move_direction(self.head.location,self.direction)

        if board.get_square(loc) == board.TILES["WALL"]:

            return -1
        elif  board.get_square(loc) == board.TILES["SNAKE"]:

            return -1
        elif board.get_square(loc) == board.TILES["APPLE"]:
            self.size = self.size + 1
            new_Node = Node(loc,self.head,None)
            self.head.prev = new_Node
            self.head = new_Node
            self.update_board(board)

            return 1
        else:
            board.set_square(self.tail.location, board.TILES["EMPTY"])

            self.tail = self.tail.prev
            self.tail.next = None

            new_Node = Node(loc,self.head,None)
            self.head.prev = new_Node
            self.head = new_Node

            self.update_board(board)
            return 0
            
            




    def move_direction(self,loc: tuple, dir: tuple):
        return loc[0] -  dir[0], loc[1] - dir[1]