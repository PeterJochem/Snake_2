# This file implements the snake class

import numpy as np


class Snake:

    # Constructor 
    # Describe the input args here
    def __init__(self, name, color):

        self.color = color
        self.name = name 

        self.body_x = np.array( [10 ] ) 
        self.body_y = np.array( [10 ] )
    

    def isBody(self, x, y):
        
        # Traverse the snake's body to check for collisions
        for i in range(len( self.body_x ) ):
            
            if ( ( self.body_x[i] == x) and ( self.body_y[i] == y) ):
                return False
         
        return True

    # Input: 
    # Return Value: 
    def isLegal(self, move, x, y, maxX, maxY):
        
        # Check for error conditions
        if ( (move < 0) or (move > 4) ):
            print("Error: The input is out of range")

        newX = x
        newY = y
        if ( move == 0 ):
            move = "left"
            newX = x - 1

        elif ( move == 1 ):
            move = "right"
            newX = x + 1

        elif ( move == 2):
            move = "down"
            newY = y - 1

        elif ( move == 3 ):
            move = "up"
            newY = y + 1
        
        if ( (newX >= maxX) or (newY >= maxY) or (newX < 0) or (newY < 0) ):
            return False


        if ( (self.isBody(newX, newY) == True) ):
            return True
        else:
            return False
        
        

