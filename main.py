# Main file !
from board import Board
from snake import Snake
from tqdm import tqdm
from Strategies.Cycles.cycle_prim import Strategy
import time
import numpy as np
score = 0


num_games = 100
steps_list = []
for i in range(num_games):
    b1 = Board(6,6)
    D1 = Strategy()
    start = (3,4)
    
    S1 = Snake(head=start,size=2,board=b1,direction=(0,1))
    S1.update_board(b1)
    S1.direction = (-1,0)
    steps = 0
    b1.spawn_apple()
    while True:
        steps = steps + 1
        if steps > 100:
            break
        #time.sleep(.1)
        #print("\033c")
        S1.direction = D1.update(b1,S1)
        result = S1.move_forward(b1)
        #print(b1)

        if result == -1:
            score = score + S1.size
            steps_list.append(steps)
            break
        elif result == 1:
            apple_result = b1.spawn_apple()
            if apple_result == 1:
                steps_list.append(steps)
                score = score + S1.size
                break



print(f"Average Score: {score/num_games}")
print(f"Average Steps: {np.mean(steps_list)}")


