# This file implements the snake class

import numpy as np


class Snake:

    # Constructor 
    # Describe the input args here
    def __init__(self, name, color):

        self.color = color
        self.name = name 

        self.body_x = np.array( [5 ] ) 
        self.body_y = np.array( [5 ] )
    

