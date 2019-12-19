from snake import Snake
from Game import Game
import numpy as np
import graphics
import time

############ Main ##################

# Create game 
# Run the game's logic

allGames = [  ]

numGames = 1000
for i in range(numGames):
    myGame = Game(20, 20, 600, 500, False)
    allGames.append(myGame)
    myGame.drawBoard()

    while ( True ):    
            # time.sleep(0.4)
            move = myGame.generate_NN_Move() 
            if ( myGame.isOver == True):
                break
            else:
                myGame.nextState( move )

learned = False
for i in range( numGames ):
    
    if ( allGames[i].score > 2 ):
        print(allGames[i].score )
        learned = True

if ( learned == False ):
    print("No game scored more than two points")


####################################
