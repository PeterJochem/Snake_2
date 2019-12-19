# This class implements a single game 
import graphics
import numpy as np
from snake import Snake
from graphics import *
from random import random
from Neural_Network import Neural_Network

class Game: 
        
    def __init__(self, length_grid, width_grid, length_window, width_window, display):
        
        self.score = 0
        
        self.isOver = False

        self.message = None

        self.length_grid = length_grid
        self.width_grid = width_grid
        self.board = np.zeros( (length_grid, width_grid) )
    
        self.length_window = length_window
        self.width_window = width_window
        
        if ( display == True ):
            self.window = GraphWin("Snake", self.length_window, self.width_window)
        else:
            self.window = None

        self.snake = Snake("Peter", "Blue")
        
        # This also sets the methods board object
        self.drawBoard()
        
        self.id = 0

        # A tuple of the current food's location
        self.current_food = self.placeFood()
        
        # FIX ME!!
        self.neural_network = Neural_Network( 16, 16, 4  )

    # Retrurn the normalized distance
    def distance_wall(self, x, y, priorX, priorY):

        maxLength = -1.0

        if ( (x - priorX == 1) ):
            maxLength = float(self.width_grid)
        elif( (x - priorX == -1) ):
            maxLength = float(-1 * self.width_grid)
        elif( y - priorY == 1  ):
             maxLength = float(-1 * self.length_grid)
        else:
            maxLength = float(-1 * self.length_grid) 

        # Check that the (x, y) pair is legal
        if ( (x < 0) or (y < 0) ):
             return 0.0   
        elif ( (x >= self.width_grid) or (y >= self.length_grid) ):
            # EXPLAIN THIS
            return maxLength
        
        # Normal cases 
        if ( (x - priorX != 0) ):
            # Moving to the right/left
            return (maxLength - x) / maxLength

        else:
            return (maxLength - y) / maxLength 

         
    # Describe the inputs
    # FIX ME - add the diagonals!!!!!
    def distance_body(self, x, y, forward):
        
        maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )
        # Check that the (x, y) pair is legal    
        if ( (x < 0) or (y < 0) ):
            return [0.0, 0.0]    
        
        elif ( (x >= self.width_grid) or (y >= self.length_grid) ):
            return [maxLength, maxLength]
       
        # Traverse in this direction to see how far we are to any body part
        # Set this to the high value to avoid discontinuity in the statistic!
        # -1 is good, 0 is the worst, larger from there is better
        linear_to_body_x_forward = maxLength
        linear_to_body_y_forward = maxLength
        linear_to_body_x_backwards = maxLength
        linear_to_body_y_backwards = maxLength


        # Traverse the x-dimension forwards
        for i in range( self.length_grid - x ):
            
            if ( self.snake.isBody(x + i, y) == False  ):
                linear_to_body_x_forward = float(i) / maxLength
                break  
        
        # Traverse the x-dimension backwards
        for i in range( x ):

            if ( self.snake.isBody(x - i, y) == False ):
                linear_to_body_x_backwards = float(i) / maxLength
                break
        
        # Traverse the y-dimension forwards
        for i in range( self.width_grid - y ):

            if ( self.snake.isBody(x, y + i) == False ):
                linear_to_body_y_forward = float(i) / maxLength                    
                break

        # Traverse the y-dimension backwards
        for i in range( y ):

            if ( self.snake.isBody(x, y - i) == False ):
                linear_to_body_y_backwards = float(i) / maxLength
                break
        
        # Return the tuple
        return [linear_to_body_x_forward, linear_to_body_y_forward] 



    def distance_food(self, x, y, priorX, priorY):
        
        # This computes the actual distance
        #maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )  
        # Check that the (x,y) pair is legal
        #if ( (x < 0) or (y < 0) or (x >= self.width_grid) or (y >= self.length_grid) ):
        #    return -1
        #return np.sqrt( ( (x - self.current_food[0])**2) + ( (y - self.current_food[1])**2) ) / maxLength


        # maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) ) 
        maxLength = self.width_grid
        # Check that the (x,y) pair is legal
        if ( (x < 0) or (y < 0) or (x >= self.length_grid) or (y >= self.width_grid) ):
            return -1
        
        deltaX = x - priorX
        deltaY = y - priorY
       
        if ( (deltaX == 1) and ( abs(x - self.current_food[0]) < abs(priorX - self.current_food[0])  )  ):
            return abs(x - self.current_food[0])
        elif ( (deltaY == 1) and (  abs(y - self.current_food[1]) < abs(priorY - self.current_food[1])  )  ):
            return  abs(y - self.current_food[1])
        else:
            return 0.0
        

    
    def generate_4_Neighbors(self, x, y):

        return [ [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1] ]

        

    
    # This method takes the game state and computes the in vector
    # that will go to the neural network
    # Input: 
    # Output: N x ? np.array
    def compute_In_Vector(self, x, y):
        
        # FIX ME!!
        # Let's start with just the 4 neighbor
        numNeighbors = 4
        numStats = 4
        length = numNeighbors * numStats
        returnVector = np.zeros( (length, 1) )

        # Statistics
        # One-dimensional Distance to wall in that direction
        # Distance to food if we move to that location
        # Distance to the body? 
            # 0 if no such body part in that direction
        
        # Create a list of tuples of each of the x and y locations
        # The statistic methods will check if the locations are legal or not 
        neighbors_list = self.generate_4_Neighbors(x, y) 
 
        vectorIndex = 0
        forward = [True, False, True, False]
        for i in range( len(neighbors_list) ):
            
            prior_x = self.snake.body_x[-1] 
            prior_y =  self.snake.body_y[-1]
            x = neighbors_list[i][0] 
            y = neighbors_list[i][1]
            
            # Compute distance to it's tail? 
            # Compute the statisitcs for the given neighbor
            returnVector[vectorIndex] = 10.0 * self.distance_food( x, y, prior_x, prior_y ) 
            returnVector[vectorIndex + 1] =  10.0 * self.distance_wall( x, y, prior_x, prior_y )
            returnVector[vectorIndex + 2] =  10.0 *  (self.distance_body( x, y, forward[i] ) )[0]
            returnVector[vectorIndex + 3] =  10.0 *  (self.distance_body( x, y, forward[i] ) )[1]

            vectorIndex = vectorIndex + 4
        
        #print("")
        #print("The inVector is " )
        #print(returnVector)
        #print("")
        return returnVector
        

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
        
        if (self.window != None ):
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
        if ( self.window != None ):
            for i in  range( len( self.rectangles  ) ):
                for j in range( len( self.rectangles[i] ) ):
                    
                    self.rectangles[i][j].draw(self.window)
                    self.rectangles[i][j].setFill("black")
        

        self.board = self.rectangles

        # Draw lines over the original grid?
        
        # Draw the snake's body
        x = self.snake.body_x[0]
        y = self.snake.body_y[0]
        if ( self.window != None ):
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
        if ( self.window != None ):
            self.rectangles[ self.current_food[1] ][ self.current_food[0]  ].setFill("purple")

        # Update the internal data structures 
        newState_x = self.snake.body_x.copy() 
        newState_y = self.snake.body_y.copy()
        

        if ( command == "left" ):
            newState_x = np.append( newState_x,  newState_x[ -1] - 1 )
            newState_y = np.append( newState_y,  newState_y[ -1]   )
        
        elif ( command == "right" ):
            newState_x = np.append( newState_x,  newState_x[ -1] + 1 )
            newState_y = np.append( newState_y,  newState_y[ -1]   )    
        
        elif ( command == "up" ):
            newState_x = np.append( newState_x,  newState_x[ -1]    )
            newState_y = np.append( newState_y,  newState_y[ -1] + 1)

        elif ( command == "down" ):
            newState_x = np.append( newState_x,  newState_x[-1]  )
            newState_y = np.append( newState_y,  newState_y[-1] - 1 )
        

        # Check if the food and the head collided
        head_x = newState_x[-1]
        head_y = newState_y[-1]
        if ( (self.current_food[0] == head_x ) and (self.current_food[1] == head_y )   ):
             
            self.score = self.score + 1.0

            # Draw the name and the score
            if ( self.window != None ):
                self.message.undraw()
                self.message = Text( Point(60, 30), "Score: " + str(self.score) )
                self.message.setSize(18)
                self.message.setTextColor("white")
                self.message.draw(self.window)
            

            # Add an item to the snake's body 
            # FIX ME - am I appending in the wrong order?
            # The head is at the end of the list
            self.snake.body_x = np.append(self.snake.body_x, self.current_food[0]  )  
            self.snake.body_y = np.append(self.snake.body_y, self.current_food[1]  )
             
            # Draw the new square
            x = self.snake.body_x[-1]
            y = self.snake.body_y[-1]
            
            if ( self.window != None ):
                self.rectangles[y][x].setFill("white") 

            # Place new food
            self.current_food = self.placeFood()

            return


        # This is the caboose of the snake and will be deleted
        # We delete by changing the fill to the background color
        delete_x = newState_x[0]
        delete_y = newState_y[0]
        if ( self.window != None ):
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
        if ( self.window != None ):
            for i in range( len( newState_x  ) ):
             
                x = newState_x[i]
                y = newState_y[i]

                # self.rectangles[y][x].draw(self.window)
                self.rectangles[y][x].setFill("white")

    # Let the neural net generate a move
    def generate_NN_Move(self):

        x = self.snake.body_x[ -1 ]
        y = self.snake.body_y[ -1 ]
        
        inputVector = self.compute_In_Vector(x, y)
              
        outputVector = self.neural_network.forwardProp(inputVector)

        for i in range(4):
            move = np.argmax(outputVector.copy() )
            # Check that the move is legal
            if ( self.snake.isLegal( move, x, y, self.length_grid, self.width_grid ) == False ):
                # print("Move rejected. Replanning")
                # outputVector[0][move] = -1
                self.isOver = True
            else:
                break
        
        if ( np.sum(outputVector[0] ) == -4):
            print("NO MOVE FOUND")
            print("(x, y) is ")
            print( str(x) + str(", ") + str(y) )
            self.isOver = True
            #while(True):
            #    pass

        if ( move == 0 ):
            move = "left"

        elif ( move == 1 ):
            move = "right"

        elif ( move == 2):
            move = "down"

        elif ( move == 3 ):
            move = "up"

        # print(move)
        return move
        


