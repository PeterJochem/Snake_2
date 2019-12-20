# This file implements the neural network

import numpy as np
import random
import copy

class Neural_Network:


    def __init__(self, numInputs, numHidden, numOutput):
        
        self.numInputs = numInputs
        self.numHidden = numHidden
        self.numOutput = numOutput

        # Pass in the size of the input
        self.w1 = self.init_Weights(numInputs, numHidden)
        self.bias_1 = np.ones(numHidden) * 0.1

        # Pass in the size of the intermediate vector
        self.w2 = self.init_Weights(numHidden, numOutput)
        self.bias_2 = np.ones(numOutput) * 0.1
     
        # For testing
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        ###########
    
    def checkMoves(self):
        count = 0
        if (self.up):
            count = count + 1

        if ( self.down ):
            # Occurs
            count = count + 1

        if(self.left):
            count = count + 1

        if(self.right):
            # Occurs
            count = count + 1

        #if ( count == 3):
        #    print("TRIPLE")
       
        #if ( self.up and self.right ):
        #    print("up and right")
        
        #if ( self.down and self.right  ):
        #    print("down and right ")
        
        # Observed
        #if( self.up and self.left ):
        #    print("up and left")
        
        # Observed
        #if ( self.down and self.left ):
        #    print("down and left")
        
        #if ( self.down and self.up ):
        #    print("up and down")
        
        # Observed
        #if ( self.right and self.left  ):
        #    print("left and right")
    

       #if (count == 2):
        #    print("Double")
        #if (count == 1):
        #    print("SINGLE")
        return count
        

    def checkDirections(self):

        if (self.up and self.down and self.left and self.right):
            return True
        return False
    
    def createVector(self, start, stop, numCol, numRow):

        returnVector = np.zeros( (numCol, numRow) )

        for i in range(len( returnVector ) ):
            for j in range(len( returnVector[0] ) ):
                returnVector[i][j] =random.uniform(start, stop)
        
        return returnVector
    
    # This method takes the current neural net and crosses it over
    # to make the offspring
    # Input:
    # Output:
    def crossOver(self, partner, numChildren):

        offSpring = []
        
        # Re-set the state's fields
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.id = 0

        # Try averaging all the entries +/ random noise

        for i in range(numChildren):

            nextChild_solo =  copy.deepcopy(self)
            nextChild_couple = copy.deepcopy(self)

            nextChild_solo.w1 = ( ((self.w1 + partner.w1) ) / 2.0) #+ ( self.createVector( -100.0, 100.0, len(self.w1), len(self.w1[0])  )  )
            nextChild_solo.w2 = ( ((self.w2 + partner.w2) ) / 2.0) #+ ( self.createVector( -100.0, 100.0, len(self.w2), len(self.w2[0] ) )  )

            nextChild_couple.w1 = ( ((self.w1) ) ) + ( self.createVector( -1.0, 1.0, len(self.w1), len(self.w1[0])  )  )
            nextChild_couple.w2 = ( ((self.w2) ) ) + ( self.createVector( -1.0, 1.0, len(self.w2), len(self.w2[0])  )  )

            offSpring.append(nextChild_solo)
            offSpring.append(nextChild_couple)

        return offSpring



    # This randomnly a single layer's of the NN's weights
    # Input: The length of the desired vector 
    # Output: The randomnly initalized weight vector
    def init_Weights(self, numColumns, numRows):
        
        # Must make the weights smaller or else softmax returns infinite
        returnVector = self.createVector(-1.0, 1.0, numColumns, numRows)

        return returnVector
        
         
    # This function implements the rectified linear unit
    def relu( self, myInput ):
        
        for i in range( len(myInput) ):
            myInput[i] = max(0.0, myInput[0][i] )
    
        return myInput
    
    # This function implements the softmax function
    # Input is a 1 x N vector where N is the number of categorical output variables 
    # Return is a 1 x N vector of the softmax for each of the N entries 
    def softmax(self, inVector):
        
        returnVector = np.zeros(len(inVector) )
        
        # Traverse the array once to compute the integral term
        integral = float( np.sum( np.exp( inVector ) ) )
        
        for i in range(len(inVector) ):

           returnVector[i] = (np.e ** inVector[i] ) / integral   
        
        # print( returnVector )
        return returnVector


    # This method takes an input vector
    # Input: an input vector to forward propogate 
    # Output: The maximum index of the output vector
    def forwardProp(self, inputVector):
        
        #print("")   
        #print( np.matmul( inputVector.copy().T, self.w1.copy() ) )
        # print("")   
        
        # WHY DOES RELU PREVENT TRIPLES??????
        #layer_1 = self.relu( np.matmul( inputVector.copy().T, self.w1.copy() ) )  # + self.bias_1 )   
        layer_1 =  np.matmul( inputVector.copy().T, self.w1.copy() )

        # Use the softmax function at the output layer
        #outputVector = # np.array( [ self.softmax( (np.matmul( layer_1.copy(), self.w2.copy() ) )[0] ) ] ) # + self.bias_2 )
        
        # outputVector = np.array( [ np.matmul( layer_1.copy(), self.w2.copy() )[0]  ] ) 
        outputVector = np.matmul( layer_1.copy(), self.w2.copy() )
    

        #print("") 
        #print(outputVector)
        #print("")
        
        #while(True):
        #    pass
        
        
        return outputVector


    # This method takes itself and a mate's weights
    # and mutate them to return a child 
    # Input:
    # Output: child neural net
    def mutate(self, mate):
         
        # Return a new, child neural network
        pass 


####### Main for testing ###########

#myNN = Neural_Network(16, 5, 4)
#inputVector = np.zeros(16)
#print( myNN.forwardProp( inputVector  ) )




