from Node import Node

class Strategy:
    def __init__(self):
        pass


    def update(self,board,snake):
        head = snake.head
        direction = snake.direction
        for x in range(board.width):
            for y in range(board.height):
                if board.get_square((x,y)) == board.TILES["APPLE"]:
                    headx,heady = head.location
                   
                    if headx > x and direction != (-1,0):
                        return (1,0)
                    if headx < x and direction != (1,0):
                        
                        return (-1,0)
                    if heady < y and direction != (0,1):
                        return (0,-1)
                    if heady > y and direction != (0,-1):
                        return (0,1)
        return direction



                    