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
        
        self.board = np.array([])

    # Draw the board to the screen
    def drawBoard(self):
         
        self.window.setBackground("white") 
        
        # draw everything once
        # Just set/re-set the colors to implement the gameplay
        # Put lines between each cell for a cleaner display
        
        # Store the lists of lists of graphics objects that is the grid
        
        self.rectangles = []
        
        # Store the list of points needed to draw the board
        points = [] 
        

        for i in range( self.length_grid ):
            
            current_row_rectangles = []
                
            Point_1 = Point( 0 , 0 ) 
            for j in range( self.width_grid ):
                
                current_row = float(self.length_window) / float(self.length_grid)
                current_column = float(self.width_window) / float(self.width_grid ) 
                
                Point_1 = Point( current_row * i , current_column * j )  
                Point_2 = Point( current_row * (i + 1) , current_column * (j + 1) )
                
                current_row_rectangles.append( Rectangle(Point_1, Point_2 ) )


            # Append the next row to the array
            self.rectangles.append(current_row_rectangles)

        
        # Traverse the list of the rectangles to change their fill colors
        for i in  range( len( self.rectangles  ) ):
            for j in range( len( self.rectangles[i] ) ):
                
                self.rectangles[i][j].draw(self.window)
                self.rectangles[i][j].setFill("black")
        

        # Draw lines over the original grid?
        
        # Draw the snake's body
        x = self.snake.body_x[0]
        y = self.snake.body_y[0]
        self.rectangles[y][x].setFill(self.snake.color)
        
        # Draw the name and the score
        message = Text( Point(50, 50), "Score: 0" )
        message.setSize(18)
        message.setTextColor("white")
        message.draw(self.window)
       
        # Make the food blink?? Kind of cool?
    
    # This moves the game from one state to the next
    # Input is either "left", "right", "up", "down"
    def nextState(self, command):

        # Update the internal data structures 
        newState_x = self.snake.body_x.copy() 
        newState_y = self.snake.body_y.copy()
        

        if ( command == "left" ):
            newState_x = np.append( newState_x,  newState_x[ len(newState_x) - 1] - 1 )
            newState_y = np.append( newState_y,  newState_y[ len(newState_y) - 1]   )
        
        elif ( command == "right" ):
            newState_x = np.append( newState_x,  newState_x[ len(newState_x) - 1] + 1 )
            newState_y = np.append( newState_y,  newState_y[ len(newState_y) - 1]   )    
        
        elif ( command == "up" ):
            newState_x = np.append( newState_x,  newState_x[ len(newState_x) - 1]    )
            newState_y = np.append( newState_y,  newState_y[ len(newState_y) - 1] + 1)

        elif ( command == "down" ):
            newState_x = np.append( newState_x,  newState_x[ len(newState_x) - 1]  )
            newState_y = np.append( newState_y,  newState_y[ len(newState_y) - 1] - 1 )
        
        
        # This is the caboose of the snake and will be deleted
        # We delete by changing the fill to the background color
        delete_x = newState_x[0]
        delete_y = newState_y[0]
        self.rectangles[delete_y][delete_x].setFill("black")


        newState_x = np.delete(newState_x, 0)
        newState_y = np.delete(newState_y, 0)
        


        # Change the snake's data structures 
        self.snake.body_x = newState_x.copy()
        self.snake.body_y = newState_y.copy()


        # Re-draw the data 
        # Change the fill on the old states
        # Change the fill on the new states
        # Traverse the list of the rectangles to change their fill colors
        for i in  range( len( newState_x  ) ):
             
            x = newState_x[i]
            y = newState_y[i]

            # self.rectangles[y][x].draw(self.window)
            self.rectangles[y][x].setFill("white")



