# This file implements the neural network




class Neural_Network:


    def __init__(self):
    
        self.inputWeights = np.Matrix( [ ] ).T
        bias_1 = 0.1

        self.hiddenWeights = np.Matrix( [] ).T
        bias_2 = 0.1

        self.outputUnits = np.Matrix( [] ).T
        bias_3 = 0.1


    # This randomnly initializes the NN's 
    # given weights 
    def initialize_Weights(self):
        
        pass 
        
    
    # This function implements the rectified linear unit
    def relu( myInput ):

        return max(0.0, myInput) 
    
    # This function implements the softmax function
    def softmax(self, myInput):
        
        


    # This method takes an input vector
    # Input: 
    # Output: 
    def forwardProp(inputVector):
    
        # input vector needs to be a matrix to use the "*"
        # If not, use np.matmul(x, y)
        layer_1 = self.relu( inputVector * self.inputWeights ) + bias_1 )   
        
        layer_2 = self.softmax( layer_1 * self.hiddenWeights + bias_2 )

        # Use the softmax function at the output layer 
         



    # This method takes itself and a mate's weights
    # and mutate them to return a child 
    # Input:
    # Output: child neural net
    def mutate(self, mate):
         
        # Return a new, child neural network
        pass 

