Neural Network meets genetic algorithm to learn how to play snake

How to run my code: Simply fork my repo and run ```python Snake_Game.py```. No other software needs to be installed (other than the standard Python-3 interpreter) 

I have found the best results occur when I used 1 hidden layer with a width of 5. So, the neural network has 8 input neurons, a layer of 5 hidden neurons and 4 output neurons. Each output neuron represents a direction that the snake could move. 

Future idea: graph performance as a function of graph structure  

Rather than using backpropogation to compute the gradient and then use stochastic gradient descent, I used a genetic algorithm to learn a good weight set. After every iteration, the most fit neural network's weight sets are averaged element-wise and then have a small bit of noise added to them. 

Describe the pickling: I implemented weight saving features so that I could minimize traning times for debugging. Describe more...


Personally, I am very surprised that the genetic algorithm is robust enough to learn a good enough weight set!! 
