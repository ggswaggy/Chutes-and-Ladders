# Chutes-and-Ladders
TL;DR: Programs used to simulate a customizable game of Chutes and Ladders and to calculate such a game's fundamental matrix to find similar data. 

Both of these programs are fundamental pieces of a research project exploring the mathematical properties of this board game, Chutes and Ladders, and a more complicated one, No Te Enojes. 
As far as these programs go, the purpose is to provide two different perspectives on the nature of the game, one by empircal monte carlo simulation and the other by a theoretical, 
probabilistic approach with the implentation of Markov Chain theory. The C++ program perfoms the former and the Python code the latter. 

Both codes allow for full customization of the gameboard (placement of chutes and ladders) as well as die size. Failsafes are put in place to make sure placements are valid.
In the C++ simulation code, one failsafe counts the number of terms and breaks the simulation loop once this number climbs too high, as this would suggest that an inescapable
loop has been formed by user placement of board elements. It might be a good idea to test this failsafe with a small number of simulated games first and then deactivate it, 
as a particularly large board with a particularly large number of simulations could set this failsafe off without there actually being a loop. 

The C++ code has full input-verification failsafes implemented--the Python code does not. Please be kind to it. 

In either code, the user is presented with the option to simulate the original Milton Bradley standard board configuration. Although the original board has 100 spaces, players
must begin off of the board, and thus we consider 101 spaces in this code. The 0-th space is occupied before rolling for the first time. In general, to simulate a board
with N playable spaces, the user must enter N+1 into the space number prompt, as the 0-th space will always be counted. 
