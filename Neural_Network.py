# This file implements the neural network

import numpy as np
import random


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
    

    def createVector(self, start, stop, numCol, numRow):

        returnVector = np.zeros( (numCol, numRow) )
        
        for i in range(len( returnVector ) ):
            for j in range(len( returnVector[0] ) ):
                returnVector[i][j] = random.uniform(start, stop)
        
        return returnVector

    # This randomnly a single layer's of the NN's weights
    # Input: The length of the desired vector 
    # Output: The randomnly initalized weight vector
    def init_Weights(self, numColumns, numRows):
        
        # Must make the weights smaller or else softmax returns infinite
        # returnVector = np.ones( length ) * 0.001

        returnVector = self.createVector(-0.15, 0.15, numColumns, numRows)
        
        #print("")
        #print(np.random.randn(numColumns, numRows) )
        #print("")
        
        # returnVector = np.asarray(np.random.randn(numColumns, numRows), dtype=np.float32)
        
        # ( np.ones( (numColumns, numRows) ) ) + np.random.rand( numColumns, numRows ) 
        #print("")
        #print("The return vector is ")
        #print(returnVector)
        #print("")

        # np.ones( (numColumns, numRows) ) * 0.05 
        # np.random.rand( numColumns, numRows ) # * 0.1 

        return returnVector
        
         
    # This function implements the rectified linear unit
    def relu( self, myInput ):
        
        for i in range( len(myInput) ):
            myInput[i] = max(0.0, myInput[i] )
    
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
             
        print( returnVector )
        return returnVector


    # This method takes an input vector
    # Input: an input vector to forward propogate 
    # Output: The maximum index of the output vector
    def forwardProp(self, inputVector):
        
        layer_1 = self.relu( np.matmul( inputVector.copy(), self.w1.copy() ) )  # + self.bias_1 )   
        
        # Use the softmax function at the output layer
        outputVector = np.array( [ self.softmax( np.matmul( layer_1.copy(), self.w2.copy() ) ) ] ) # + self.bias_2 )
            
        
        # Return the max index of the output vector
        #print("")
        #print(outputVector)
        #print("")
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




