from snake import Snake
from Game import Game
import numpy as np
import graphics
import time
import random

############ Main ##################

# Create game 
# Run the game's logic

def generation_0( numGames ):

    allGames = [  ]

    for i in range(numGames):
        # print("Game: " + str(i) )
        myGame = Game(20, 20, 600, 500, False)
        allGames.append(myGame)
        myGame.drawBoard()

        while ( True ):    
            # time.sleep(0.4)
            move = myGame.generate_NN_Move() 
            if ( myGame.isOver == True):
                if(myGame.neural_network.checkDirections() == True):
                    print("ALL 4 directions found!!")
                break
            else:
                myGame.nextState( move )

    # Find the best nets in the set - take the ones with the most moves
    doubles = []
    maxIndex = 0
    secondIndex = 1 
    for i in range(1, len(allGames) ):
        if ( allGames[i].neural_network.checkMoves() > 1.0  ):
            if ( allGames[i].moveNumber < 900 ):
                doubles.append( allGames[i].neural_network )

    print("")
    print("The percentage of doubles is " + str( float( len(doubles) ) / float( len( allGames)  )   ) )
    print("")
    # Take the two best NN and mutate them

    return doubles



def nextGeneration(doubles, rate): 

    children = []
    for i in range(len(doubles) - 1 ):
            
        # Change how pairs are made
        children_new = doubles[i].crossOver(doubles[i + 1], rate)
        children.extend(children_new)

    
    allGames = []
    # Run a game for each child
    for i in range( len(children)  ):
        # print("Game: " + str(i) )
        myGame = Game(20, 20, 600, 500, False)
            
        myGame.neural_network = children[i]

        allGames.append(myGame)

        myGame.drawBoard()


        while ( True ):
            # time.sleep(0.4)
            move = myGame.generate_NN_Move()
            if ( myGame.isOver == True):
                if(myGame.neural_network.checkDirections() == True):
                    print("ALL 4 directions found!!")
                break
            else:
                myGame.nextState( move )

    doubles = []
    for i in range(1, len(allGames) ):
        if ( allGames[i].neural_network.checkMoves() > 1.0  ):
            if ( allGames[i].moveNumber < 900 ):
                if ( allGames[i].score > 0  ):
                    doubles.append( allGames[i].neural_network )
        
        if (allGames[i].score > 2.0   ):
            print("NN scored! " + str( allGames[i].score  ) )


    print("")
    print("The percentage of doubles is " + str( float( len(doubles) ) / float( len( allGames)  )   ) )
    print("")

    return doubles


numGenerations = 10

gen_now = generation_0(100)

for i in range( numGenerations ):
    print("Generation: " + str(i) )
    gen_now = nextGeneration( gen_now, 1 )

random. shuffle(gen_now)


numGames = 1
for i in range(numGames):
    # print("Game: " + str(i) )
    myGame = Game(20, 20, 600, 500, True)
    
    myGame.neural_network = gen_now[0]
    
    myGame.drawBoard()

    while ( True ):
        time.sleep(0.4)
        move = myGame.generate_NN_Move()
        if ( myGame.isOver == True):
            break
        else:
            myGame.nextState( move )





####################################
