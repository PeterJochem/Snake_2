# This file implements the neural network

import numpy as np



class Neural_Network:


    def __init__(self):
    
        # Pass in the size of the input
        self.w1 = self.init_Weights(4)
        self.bias_1 = np.ones(4) * 0.1

        # Pass in the size of the intermediate vector
        self.w2 = self.init_Weights(4)
        self.bias_2 = np.ones(4) * 0.1

        
    # This randomnly a single layer's of the NN's weights
    # Input: The length of the desired vector 
    # Output: The randomnly initalized weight vector
    def init_Weights(self, length):
        
        returnVector = np.zeros( length )
        returnVector = np.ones( length )

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

           returnVector[i] = (np.e ** inVector[i]  ) / integral   
    
        
        print( returnVector )
        return returnVector


    # This method takes an input vector
    # Input: an input vector to forward propogate 
    # Output: The maximum index of the output vector
    def forwardProp(self, inputVector):
    
        # print("")
        # print( np.matmul( inputVector, self.w1.T) + self.bias_1   )
        # print("")
        layer_1 = self.relu( np.matmul( inputVector, self.w1.T) + self.bias_1 )   
        

        # Use the softmax function at the output layer
        outputVector = self.softmax( np.matmul( layer_1, self.w2) + self.bias_2 )
        
        # Return the max index of the output vector
        return np.argmax( outputVector )



    # This method takes itself and a mate's weights
    # and mutate them to return a child 
    # Input:
    # Output: child neural net
    def mutate(self, mate):
         
        # Return a new, child neural network
        pass 


####### Main for testing ###########

myNN = Neural_Network()

inputVector = np.array([0.0, 0.0, 0.0, 0.0])

print( myNN.forwardProp( inputVector  ) )




