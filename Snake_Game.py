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

moves = ["left", "left", "left", "left", "up", "up", "up", "up", "right", "right", "right", "right",  "down", "down", "down", "down" ]

# myGame.current_food = myGame.placeFood()

i = 0
while ( True ):
    
    for i in range(len(moves) ):

        # Update the snake's body
        # Updates the 
        # myGame.rectangles[0][0].setFill("purple")
        # myGame.rectangles[0].setFill()
            
        time.sleep(0.05)
        
        # Compute the next input vector
        # Forward prop the inputVector
        # Convert the NN's output to a direction
        # nextDirection = myGame.  
        
        # myGame.nextState( moves[i] )
         
        move = myGame.generate_NN_Move()
        
        myGame.nextState( move )


while(True):
    pass 

####################################
