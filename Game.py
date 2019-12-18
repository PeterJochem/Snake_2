# This class implements a single game 

import graphics
import numpy as np
from snake import Snake
from graphics import *

class Game: 
        
    def __init__(self, length_grid, width_grid, length_window, width_window):

        self.length_grid = length_grid
        self.width_grid = width_grid
        self.board = np.zeros( (length_grid, width_grid) )
    
        self.length_window = length_window
        self.width_window = width_window

        self.window = GraphWin("Snake", self.length_window, self.width_window)
        
        self.snake = Snake("Peter", "Blue")


    # Draw the board to the screen
    def drawBoard(self):
         
        self.window.setBackground("white") 
        
        # draw everything once
        # Just set/re-set the colors to implement the gameplay
        # Put lines between each cell for a cleaner display
        
        # Store the lists of lists of graphics objects that is the grid
        rectangles = []
        
        # Store the list of points needed to draw the board
        points = [] 
        

        for i in range( self.length_grid ):
            
            current_row_rectangles = []
                
            Point_1 = Point( 0 , 0 ) 
            for j in range( self.width_grid ):
                
                current_row = float(self.length_window) / float(self.length_grid)
                current_column = float(self.width_window) / float(self.width_grid ) 
                
                # Point_2 = Point_1
                Point_1 = Point( current_row * i , current_column * j )  
                Point_2 = Point( current_row * (i + 1) , current_column * (j + 1) )
                
                current_row_rectangles.append( Rectangle(Point_1, Point_2 ) )


            # Append the next row to the array
            rectangles.append(current_row_rectangles)

        
        # Traverse the list of the rectangles to change their fill colors
        for i in  range( len( rectangles  ) ):
            for j in range( len(rectangles[i] ) ):
                
                rectangles[i][j].draw(self.window)
                rectangles[i][j].setFill("black")
        

        # Draw lines over the original grid?
        
        # Draw the snake's body
        x = self.snake.body_x[0]
        y = self.snake.body_y[0]
        rectangles[y][x].setFill(self.snake.color)
        
        # Draw the name and the score
        message = Text( Point(50, 50), "Score: 0" )
        message.setSize(18)
        message.setTextColor("white")
        message.draw(self.window)
       
        # Make the food blink?? Kind of cool?


