from snake import Snake
from Game import Game
import numpy as np
import graphics
import time

############ Main ##################

# Create game 
# Run the game's logic
myGame = Game(20, 20, 600, 500)
myGame.drawBoard()

myGame.drawBoard()

moves = ["left", "left", "up", "up", "right", "right", "down", "down"]

i = 0
while ( True ):
    
    for i in range(len(moves) ):

        # Update the snake's body
        # Updates the 
        # myGame.rectangles[0][0].setFill("purple")
        # myGame.rectangles[0].setFill()
            
        time.sleep(1)
        myGame.nextState(moves[i] )
         

while(True):
    pass 

####################################
