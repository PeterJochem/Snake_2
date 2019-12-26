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
        
        self.moveNumber = 0

        self.message = None

        self.length_grid = length_grid
        self.width_grid = width_grid
        self.board = np.zeros( (length_grid, width_grid) )
    
        self.length_window = length_window
        self.width_window = width_window
        
        if ( display == None ):
            self.window = GraphWin("Snake", self.length_window, self.width_window)
        else:
            self.window = display  
        
        # else:
        #    self.window = None
            
        self.snake = Snake("Peter", "Blue")

        # FIX ME!!                              # 5, 20
        self.neural_network = Neural_Network( 8, 5, 4  )
    
        # This also sets the methods board object
        self.drawBoard()
        
        self.id = 0

        # A tuple of the current food's location
        self.current_food = [0, 0]
        self.current_food = self.placeFood()
        

    # Return the normalized distance
    def distance_wall(self, x, y, priorX, priorY):

        maxLength = maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )

        # Check if we are on the diagonal
        deltaX = int(x - priorX)
        deltaY = int(y - priorY)
        distance = 0.0
        if ( (deltaX == 1) and (deltaY == 1) ):
            # Distance to the bottom right corner   
            distance = np.sqrt( ( (self.width_grid - x)**2) + ( (self.length_grid - y)**2) )  
            return distance / maxLength

        if ( (deltaX == -1) and (deltaY == 1) ):
            # Distance to the bottom left corner
            distance = np.sqrt( ( x**2) + ( (self.length_grid - y)**2) )
            return distance / maxLength

        if ( (deltaX == 1) and (deltaY == -1) ):
            # Distance to the right top corner
            distance = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )
            return distance / maxLength

        if ( (deltaX == -1) and (deltaY == -1) ):
            # Distance to the left top corner
            distance = np.sqrt( ( x**2) + ( y**2) )
            return distance / maxLength

        # Check the single dimension movements
        if ( (x - priorX == 1) ):
            maxLength = float(self.width_grid) 
        elif( y - priorY == 1  ):
             maxLength = float(1 * self.length_grid)

        # Check that the (x, y) pair is legal
        if ( (x < 0) or (y < 0) ):
             return 0.0   
        elif ( (x >= self.width_grid) or (y >= self.length_grid) ):
            # EXPLAIN THIS
            return 0.0
       
        
        # Normal 4-neighbor cases 
        if ( ( int(x - priorX) != 0) ):
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
            return [0.0, 0.0]
            # return [maxLength, maxLength]
       
        # Traverse in this direction to see how far we are to any body part
        # Set this to the high value to avoid discontinuity in the statistic!
        # -1 is good, 0 is the worst, larger from there is better
        linear_to_body_x_forward = maxLength
        linear_to_body_y_forward = maxLength
        linear_to_body_x_backwards = maxLength
        linear_to_body_y_backwards = maxLength


        # Traverse the x-dimension forwards
        for i in range( self.length_grid - x ):
            
            if ( self.snake.isBody(x + i, y) == True  ):
                linear_to_body_x_forward = float(i) / maxLength
                break  
        
        # Traverse the x-dimension backwards
        for i in range( x ):

            if ( self.snake.isBody(x - i, y) == True ):
                linear_to_body_x_backwards = float(i) / maxLength
                break
        
        # Traverse the y-dimension forwards
        for i in range( self.width_grid - y ):

            if ( self.snake.isBody(x, y + i) == True ):
                linear_to_body_y_forward = float(i) / maxLength                    
                break

        # Traverse the y-dimension backwards
        for i in range( y ):

            if ( self.snake.isBody(x, y - i) == True ):
                linear_to_body_y_backwards = float(i) / maxLength
                break
        
        # Return the tuple
        if ( forward == True):
            return [1.0, 1.0]
            # return [linear_to_body_x_forward, linear_to_body_y_forward] 
        else:
            return [1.0, 1.0]
            # return  [linear_to_body_x_backwards, linear_to_body_y_backwards]


    def distance_food(self, x, y, priorX, priorY):
        
        # This computes the actual distance
        #maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) )  
        # Check that the (x,y) pair is legal
        #if ( (x < 0) or (y < 0) or (x >= self.width_grid) or (y >= self.length_grid) ):
        #    return -1
        #return np.sqrt( ( (x - self.current_food[0])**2) + ( (y - self.current_food[1])**2) ) / maxLength
        

        # Check the 8 neighbor diagonal cases first
        deltaX = int(x - priorX)
        deltaY = int(y - priorY)
        distance = 0.0
        
        # distance = 1 if the food is in that direction
        # distance = 0 if the food is not in that direction

        if ( (deltaX == 1) and (deltaY == 1) ):
            
            if ( ( abs(x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return 1.0
            else:
                return 0.0

        elif ( (deltaX == 1) and (deltaY == -1) ):
            if ( ( abs(x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return  1.0
            else:
                return 0.0

        elif ( (deltaX == -1) and (deltaY == 1) ):
            if ( ( abs(x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return 1.0
            else:
                return 0.0

        elif ( (deltaX == -1) and (deltaY == -1) ):
            if ( abs( (x - self.current_food[0] ) == abs( y - self.current_food[1]  )  ) ):
                return 1.0
            else:
                return 0.0

    

        # maxLength = np.sqrt( ( (self.width_grid)**2) + ( (self.length_grid)**2) ) 
        maxLength = self.width_grid
        # Check that the (x,y) pair is legal
        if ( (x < 0) or (y < 0) or (x >= self.length_grid) or (y >= self.width_grid) ):
            return 0.0
        
        if ( (deltaX != 0) and ( abs(x - self.current_food[0]) < abs(priorX - self.current_food[0])  )  ):
            return 1.0  #abs(x - self.current_food[0])
        
        elif ( (deltaY != 0) and (  abs(y - self.current_food[1]) < abs(priorY - self.current_food[1])  )  ):
            return 1.0  # abs(y - self.current_food[1])
        else:
            return 0.0
        

    
    def generate_8_Neighbors(self, x, y):

        return [ [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1], [x + 1, y + 1], [x - 1, y - 1], [x - 1, y + 1], [x + 1, y - 1] ]

    def generate_4_Neighbors(self, x, y):

        return [ [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1] ]


        

    
    # This method takes the game state and computes the in vector
    # that will go to the neural network
    # Input: 
    # Output: N x ? np.array
    def compute_In_Vector(self, x, y):
        
        # FIX ME!!
        # Let's start with just the 4 neighbor
        numNeighbors = 8
        numStats = 1
        length = numNeighbors * numStats
        returnVector = np.zeros( (length, 1) )

        # Statistics
        # One-dimensional Distance to wall in that direction
        # Distance to food if we move to that location
        # Distance to the body? 
            # 0 if no such body part in that direction
        
        # Create a list of tuples of each of the x and y locations
        # The statistic methods will check if the locations are legal or not 
        
        neighbors_list = self.generate_8_Neighbors(x, y) 
        # neighbors_list = self.generate_4_Neighbors(x, y)

        vectorIndex = 0
        forward = [True, False, True, False]
        for i in range( len(neighbors_list) ):
            
            prior_x = self.snake.body_x[-1] 
            prior_y =  self.snake.body_y[-1]
            x = neighbors_list[i][0] 
            y = neighbors_list[i][1]
            
            # Compute distance to it's tail? 
            # Compute the statisitcs for the given neighbor
            returnVector[vectorIndex] = 100 * self.distance_food( x, y, prior_x, prior_y ) 
            # returnVector[vectorIndex + 1] = 100 * np.random.rand()    # self.distance_wall( x, y, prior_x, prior_y )
            # returnVector[vectorIndex + 1] = 100 * (self.distance_body( x, y, forward[i] ) )[0]
            # returnVector[vectorIndex + 2] = 100 *  (self.distance_body( x, y, forward[i] ) )[1]

            vectorIndex = vectorIndex + numStats
        
        #print("")
        #print("The inVector is " )
        #print(returnVector)
        #print("")
        return returnVector
        

    def placeFood(self):
        
        priorX = self.current_food[0]
        priorY = self.current_food[1]

        # Place the food randomnly
        # Check that the spot is not occupied by the current snake
        
        while (True):
            new_x = int( random() * len(self.board[0] ) ) 
            new_y = int( random() * len(self.board ) )
        
            # Check that 
            for i in range(len( self.snake.body_x ) ):
                
                if ( (new_x == self.snake.body_x[i] ) and (new_y == self.snake.body_y[i] )  ):
                    continue
                if ( (priorX == new_x) or ( priorY == new_y) ):
                    continue


            if( self.id == 0):
                 new_x = 4 # 4
                 new_y = 9 # 9
                 self.id = 1
                 return [new_x, new_y]
            #elif(self.id == 1):
            #    new_x = 5
            #    new_y = 9    
            #    self.id = 2
            #    return [new_x, new_y]
            #elif ( self.id == 2 ):
            #    new_x = 5
            #    new_y = 7
            #    self.id = 3
            #    return [new_x, new_y]
            #else:
            return [new_x, new_y]

    
    def drawInputLayer(self, yCord):
        nn_width = (0.25) * (self.length_window)
        center = ( float( 0.75 * self.length_window) ) + (nn_width / 2.0)

        # Draw the neural network's neuron's
        if ( self.window != None ):

            # Draw the input neurons
            increment = float( nn_width ) /  float( (self.neural_network.numInputs) )

            isEven = False
            iterations = int( (self.neural_network.numInputs) / 2) - 1
            if ( ( (self.neural_network.numInputs) % 2) == 0 ):
                isEven = True

            priorLeft = 0
            priorRight = 0
            # Draw the center neuron(s)
            if ( isEven == False):
                nextNeuron = Point( center, yCord)
                ratio = 0.01

                # Draw the next neuron
                cir = Circle(nextNeuron, ratio * self.length_window )
                self.neural_network.inputLayerCords.append( cir )

                priorLeft = center
                priorRight = center
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
            else:
                centerLeft = Point( center - (increment / 2.0), yCord)
                centerRight = Point( center + (increment / 2.0), yCord)
                
                priorLeft =  center - (increment / 2.0)
                priorRight =  center + (increment / 2.0)
                ratio = 0.01
                # Draw the next neuron
                cir = Circle(centerLeft, ratio * self.length_window )
                self.neural_network.inputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
                
                cir = Circle(centerRight, ratio * self.length_window )
                self.neural_network.inputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')


            for i in range(0, iterations):
                nextNeuronRight = Point( priorRight + increment, yCord)
                nextNeuronLeft = Point( priorLeft - increment, yCord)

                priorRight = priorRight + increment
                priorLeft = priorLeft - increment
                ratio = 0.01
                # Draw the next right neuron
                cir = Circle(nextNeuronRight, ratio * self.length_window )
                self.neural_network.inputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
                # Draw the next left neuron
                cir = Circle(nextNeuronLeft, ratio * self.length_window )
                self.neural_network.inputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')

     
    def drawHiddenLayer(self, yCord):

        nn_width = (0.25) * (self.length_window)
        center = ( float( 0.75 * self.length_window) ) + (nn_width / 2.0)

        # Draw the neural network's neuron's
        if ( self.window != None ):

            # Draw the input neurons
            increment = float( nn_width ) /  float( (self.neural_network.numInputs) )

            isEven = True
            iterations = int( (self.neural_network.numHidden) / 2) - 1
            if ( ( (self.neural_network.numHidden) % 2) != 0 ):
                isEven = False
                iterations = int( (self.neural_network.numHidden) / 2)         

            priorLeft = 0
            priorRight = 0
            # Draw the center neuron(s)
            if ( isEven == False):
                nextNeuron = Point( center, yCord)
                
                ratio = 0.01
                # Draw the next neuron
                cir = Circle(nextNeuron, ratio * self.length_window )
                self.neural_network.hiddenLayerCords.append( cir )
                priorLeft = center
                priorRight = center
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
            else:
                centerLeft = Point( center - (increment / 2.0), yCord)
                centerRight = Point( center + (increment / 2.0), yCord)
                
                priorLeft =  center - (increment / 2.0)
                priorRight =  center + (increment / 2.0)
                ratio = 0.01
                # Draw the next neuron
                cir = Circle(centerLeft, ratio * self.length_window )
                self.neural_network.hiddenLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
                cir = Circle(centerRight, ratio * self.length_window )
                self.neural_network.hiddenLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
            
            for i in range(0, iterations):
                nextNeuronRight = Point( priorRight + increment, yCord)
                nextNeuronLeft = Point( priorLeft - increment, yCord)

                priorRight = priorRight + increment
                priorLeft = priorLeft - increment
                ratio = 0.01
                # Draw the next right neuron
                cir = Circle(nextNeuronRight, ratio * self.length_window )
                self.neural_network.hiddenLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
                # Draw the next left neuron
                cir = Circle(nextNeuronLeft, ratio * self.length_window )
                self.neural_network.hiddenLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
    
    def drawOutputLayer(self, yCord):
            
        nn_width = (0.25) * (self.length_window)
        center = ( float( 0.75 * self.length_window) ) + (nn_width / 2.0)

        # Draw the neural network's neuron's
        if ( self.window != None ):

            # Draw the input neurons
            increment = float( nn_width ) /  float( (4.0) )

            isEven = True
            iterations = int( (4) / 2) - 1
            if ( ( 4 % 2) != 0 ):
                isEven = False
                iterations = int( 4 / 2)

            priorLeft = 0
            priorRight = 0
            # Draw the center neuron(s)
            if ( isEven == False):
                nextNeuron = Point( center, yCord)
                
                ratio = 0.01
                # Draw the next neuron
                cir = Circle(nextNeuron, ratio * self.length_window )
                self.neural_network.outputLayerCords.append( cir )
               
                priorLeft = center
                priorRight = center
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
            else:
                centerLeft = Point( center - (increment / 2.0), yCord)
                centerRight = Point( center + (increment / 2.0), yCord)
                
                priorLeft =  center - (increment / 2.0)
                priorRight =  center + (increment / 2.0)
                ratio = 0.01
                # Draw the next neuron
                cir = Circle(centerLeft, ratio * self.length_window )
                self.neural_network.outputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
                cir = Circle(centerRight, ratio * self.length_window )
                self.neural_network.outputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')

            for i in range(0, iterations):
                nextNeuronRight = Point( priorRight + increment, yCord)
                nextNeuronLeft = Point( priorLeft - increment, yCord)
                
                priorRight = priorRight + increment
                priorLeft = priorLeft - increment
                ratio = 0.01
                # Draw the next right neuron
                cir = Circle(nextNeuronRight, ratio * self.length_window)
                self.neural_network.outputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
                # Draw the next left neuron
                cir = Circle(nextNeuronLeft, ratio * self.length_window )
                self.neural_network.outputLayerCords.append( cir )
                cir.draw(self.window)
                cir.setOutline('black')
                cir.setFill('blue')
    
    def drawWeights(self):
        
        # records the lines
        self.neural_network.L1 = []
        self.neural_network.L2 = []

        # Draw the weights from the input layer to the hidden layer
        for i in range( self.neural_network.numInputs):
            for j in range( self.neural_network.numHidden ):
                
                column = int( i / (len(self.neural_network.w1)) )
                row =  int( i % (len(self.neural_network.w1)) )

                line = Line( self.neural_network.inputLayerCords[i].getCenter(),  self.neural_network.hiddenLayerCords[j].getCenter()  )
                self.neural_network.L1.append(line)
                line.setFill( color_rgb( int( 150 - abs(self.neural_network.w1[row][column] * 120 ) ), 0, 0)  )
                
                line.draw(self.window)
                
        # Draw the weights from the hidden layer to the output layer
        for i in range( self.neural_network.numHidden):
            for j in range( self.neural_network.numOutput ):
                column = int( i / (len(self.neural_network.w2)) )
                row =  int( i % (len(self.neural_network.w2)) )

                line = Line( self.neural_network.hiddenLayerCords[i].getCenter(),  self.neural_network.outputLayerCords[j].getCenter()  )
                self.neural_network.L2.append(line)
                 
                line.setFill( color_rgb( int( 150 - abs(self.neural_network.w2[row][column] * 120 ) ), 0, 0) )
                line.draw(self.window)
        

    # Draw the board to the screen
    def drawBoard(self):
        
        if (self.window != None ):
            self.window.setBackground("black") 
        
        # Store the lists of lists of graphics objects that is the grid 
        self.rectangles = []
        
        # Store the list of points needed to draw the board
        points = [] 
        
        for i in range( self.length_grid ):
            
            current_row_rectangles = []
                
            Point_1 = Point( 0 , 0 ) 
            for j in range( self.width_grid ):
                 
                current_row = float( 0.75 * self.length_window) / float( self.length_grid)
                current_column = float( 1.0 * self.width_window) / float( self.width_grid ) 
                
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
        
        if ( self.window != None ):
            # pass
            self.drawInputLayer(20)
        if ( self.window != None ):
            # pass
            self.drawHiddenLayer(100)
        if ( self.window != None ):
            #pass
            self.drawOutputLayer(180)
        # Draw lines over the original grid?
        if ( self.window != None ):
            # pass
            self.drawWeights()


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
         
        self.moveNumber = self.moveNumber + 1
        if ( self.moveNumber > 1000):
            self.isOver = True

        # Re-draw the food
        if ( self.window != None ):
            self.rectangles[ self.current_food[1] ][ self.current_food[0]  ].setFill("purple")
        
        # Update the internal data structures 
        newState_x = self.snake.body_x.copy() 
        newState_y = self.snake.body_y.copy()

        if ( command == "left" ):
            newState_x = np.append( newState_x,  newState_x[ -1] - 1)
            newState_y = np.append( newState_y,  newState_y[ -1]    )
        
        elif ( command == "right" ):
            newState_x = np.append( newState_x,  newState_x[ -1] + 1)
            newState_y = np.append( newState_y,  newState_y[ -1]    )    
        
        elif ( command == "up" ):
            newState_x = np.append( newState_x,  newState_x[ -1]    )
            newState_y = np.append( newState_y,  newState_y[ -1] + 1)

        elif ( command == "down" ):
            newState_x = np.append( newState_x,  newState_x[-1]    )
            newState_y = np.append( newState_y,  newState_y[-1] - 1)
        

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
            
            
            # Change the color of the fired neurons
            for i in range(len(self.neural_network.inputLayerFired) ):
                if ( self.neural_network.inputLayerFired[i] == True ):

                    #pass
                    self.neural_network.inputLayerCords[i].setOutline("red")
                else:

                    # pass
                    self.neural_network.inputLayerCords[i].setOutline("blue")
                    # self.neural_network.L2[i].setFill('blue')

            for i in range(len(self.neural_network.hiddenLayerFired) ):
                if ( self.neural_network.hiddenLayerFired[i] == True ):
                    
                    # pass 
                    self.neural_network.hiddenLayerCords[i].setOutline("red")
                else:
                    
                    # pass
                    self.neural_network.hiddenLayerCords[i].setOutline("blue") 
                    # self.neural_network.L2[i].setFill('blue')

            for i in range(len(self.neural_network.outputLayerFired) ):
                if ( self.neural_network.outputLayerFired[i] == True ):

                    # pass
                    self.neural_network.outputLayerCords[i].setOutline("red")
                else:
                    
                    # pass
                    self.neural_network.outputLayerCords[i].setOutline("blue")
                    # self.neural_network.L2[i].setFill('blue')
            

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
            self.neural_network.left = True
            move = "left"

        elif ( move == 1 ):
            self.neural_network.right = True
            move = "right"

        elif ( move == 2):
            self.neural_network.down = True
            move = "down"

        elif ( move == 3 ):
            self.neural_network.up = True
            move = "up"

        # print(move)
        return move
        


