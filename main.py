# Main file !
from board import Board
from snake import Snake
from tqdm import tqdm
from Strategies.naive import Strategy
import time
score = 0
num_games = 1
for i in range(num_games):
    b1 = Board(7,7)
    D1 = Strategy()
    start = (4,4)
    S1 = Snake(head=start,size=3,board=b1,direction=(1,0))
    S1.update_board(b1)
    S1.direction=(0,1)
    b1.spawn_apple()
    S1.direction = (-1,0)
    while True:

        print("\033c")
        print(b1)
        time.sleep(.2)
        print(S1.direction)
        S1.direction = D1.update(b1,S1)
        print(S1.direction)
        result = S1.move_forward(b1)

        if result == -1:
            score = score + S1.size
            break
        elif result == 1:
            b1.spawn_apple()

print(f"Average Score: {score/num_games}")


