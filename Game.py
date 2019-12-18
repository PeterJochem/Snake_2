# This class implements a single game 
import graphics
import numpy as np
from snake import Snake
from graphics import *
from random import random

class Game: 
        
    def __init__(self, length_grid, width_grid, length_window, width_window):
        
        self.score = 0
        
        self.message = None

        self.length_grid = length_grid
        self.width_grid = width_grid
        self.board = np.zeros( (length_grid, width_grid) )
    
        self.length_window = length_window
        self.width_window = width_window

        self.window = GraphWin("Snake", self.length_window, self.width_window)
        
        self.snake = Snake("Peter", "Blue")
        
        # This also sets the methods board object
        self.drawBoard()
        
        self.id = 0

        # A tuple of the current food's location
        self.current_food = self.placeFood()
        

    def placeFood(self):
            
        # Place the food randomnly
        # Check that the spot is not occupied by the current snake
        
        while (True):
            new_x = int( random() * len(self.board[0] ) ) 
            new_y = int( random() * len(self.board ) )
        
            # Check that 
            for i in range(len( self.snake.body_x ) ):
                
                if ( (new_x == self.snake.body_x[i] ) and (new_y == self.snake.body_y[i] )  ):
                    continue
            
            if( self.id == 0):
                new_x = 5
                new_y = 7 
                self.id = 1
                return [new_x, new_y]
            elif(self.id == 1):
                new_x = 5
                new_y = 9    
                self.id = 2
                return [new_x, new_y]
            elif ( self.id == 2 ):
                new_x = 5
                new_y = 7
                self.id = 3
                return [new_x, new_y]
            else:
                return [new_x, new_y]

    
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
                
                Point_1 = Point( current_row * j , current_column * i )  
                Point_2 = Point( current_row * (j + 1) , current_column * (i + 1) )
                
                current_row_rectangles.append( Rectangle(Point_1, Point_2 ) )


            # Append the next row to the array
            self.rectangles.append(current_row_rectangles)

        
        # Traverse the list of the rectangles to change their fill colors
        for i in  range( len( self.rectangles  ) ):
            for j in range( len( self.rectangles[i] ) ):
                
                self.rectangles[i][j].draw(self.window)
                self.rectangles[i][j].setFill("black")
        

        self.board = self.rectangles

        # Draw lines over the original grid?
        
        # Draw the snake's body
        x = self.snake.body_x[0]
        y = self.snake.body_y[0]
        self.rectangles[y][x].setFill(self.snake.color)
        
        # Draw the name and the score
        self.message = Text( Point(50, 50), "Score: " + str(self.score) )
        self.message.setSize(18)
        self.message.setTextColor("white")
        self.message.draw(self.window)
       
        # Draw the food
        try:
            self.rectangles[ self.current_food[1] ][ self.current_food[0]  ].setFill("purple")
        except:
            pass

        # Make the food blink?? Kind of cool?
    
    # This moves the game from one state to the next
    # Input is either "left", "right", "up", "down"
    def nextState(self, command):
        
        # Re-draw the food
        self.rectangles[ self.current_food[1] ][ self.current_food[0]  ].setFill("purple")

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
        

        # Check if the food and the head collided
        head_x = newState_x[ len(newState_x) - 1]
        head_y = newState_y[  len(newState_y) - 1]
        if ( (self.current_food[0] == head_x ) and (self.current_food[1] == head_y )   ):
             
            print("The snake ate some food")
            
            # Draw the name and the score
            self.score = self.score + 1.0
            self.message.undraw()
            self.message = Text( Point(60, 30), "Score: " + str(self.score) )
            self.message.setSize(18)
            self.message.setTextColor("white")
            self.message.draw(self.window)
            

            # Add an item to the snake's body 
            self.snake.body_x = np.append(self.snake.body_x, self.current_food[0]  )  
            self.snake.body_y = np.append(self.snake.body_y, self.current_food[1]  )
            
            # Draw the new square
            x = self.snake.body_x[ len(self.snake.body_x) - 1]
            y = self.snake.body_y[ len(self.snake.body_y) - 1]
            self.rectangles[y][x].setFill("white") 

            # Place new food
            self.current_food = self.placeFood()

            return


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



