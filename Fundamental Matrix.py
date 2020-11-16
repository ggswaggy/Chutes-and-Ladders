#!/usr/bin/env python
# coding: utf-8

# In[28]:


import numpy as np
from numpy import array


# In[33]:


#function will be called to check if space is the start of a snake/ladder
def checkSnake(vec, length, find):
    for i in range (length):
        if vec[i] == find:
            return 1
    return 0

#function for input verification
def getInt():
    while True:
        try:
            return int(input("Please enter a number: "))
        except ValueError:
            print("Invalid input. Please try again!")


# In[94]:


print("How many spaces would you like the board to have? (standard size is 101, including 'zero' space)")
boardSize = getInt()
boardSize = abs(boardSize)

board = [0]*boardSize

print("How many sides on the die?")
diceSize = getInt()
diceSize = abs(diceSize)

ans = -1
while ans!=0 and ans!=1:
    print("Would you like to simulate the usual snake and ladder positions?\n0: Yes\n1: No")
    ans = getInt()
    if ans!=0 and ans!=1:
        print("Invalid entry.")
        ans = -1
        
snakes = [-1]*boardSize

if ans == 0 and boardSize >= 101:
    #snake and ladder positions based on original Milton Bradley board
    #ladders
    board[1] = 38
    board[4] = 14
    board[9] = 31
    board[21] = 42
    board[28] = 84
    board[36] = 44
    board[51] = 67
    board[71] = 91
    board[80] = 100

    #snakes
    board[98] = 78
    board[95] = 75
    board[93] = 73
    board[87] = 24
    board[64] = 60
    board[62] = 19
    board[56] = 53
    board[49] = 11
    board[47] = 26
    board[16] = 6
    
    snakes[0] = 1
    snakes[1] = 4
    snakes[2] = 9
    snakes[3] = 16
    snakes[4] = 21
    snakes[5] = 28
    snakes[6] = 36
    snakes[7] = 47
    snakes[8] = 49
    snakes[9] = 51
    snakes[10] = 56
    snakes[11] = 62
    snakes[12] = 64
    snakes[13] = 71
    snakes[14] = 80
    snakes[15] = 87
    snakes[16] = 93
    snakes[17] = 95
    snakes[18] = 98
    
if ans == 0 and boardSize < 101: #does not allow usual snake/ladder placements on a board too small for them, defaults to manual placements
    print("Usual positions not possible due to chosen board size being too small. Please enter snake and ladder positions manually.")
    ans = 1

cont = 0
validEntry = -1
checkSpace = -1
numSnakes = 19
startSnake = 0
endSnake = 0
k=0

if ans == 1:
    while(cont!=1): #loops until a valid number of snakes/ladders have been placed
        print("How many snakes/ladders would you like to have in total?")
        numSnakes = getInt()
        numSnakes = abs(numSnakes)
        
        if numSnakes >= boardSize:
            print("Too many snakes, there are only %d valid spaces." %(boardSize - 1))
            validEntry = -1
        else:
            validEntry = 1 #once valid number has been selected, entry into the placement loop is granted


        if validEntry == 1: #placement loop, will loop until positions for all snakes and ladders have been selected validly
            i=0
            while i < numSnakes:
                print("Where does snake/ladder # %d begin?" %(i+1))
                startSnake = getInt()
                print("Where does snake/ladder # %d end?" %(i+1))
                endSnake = getInt()
                startSnake = abs(startSnake)
                endSnake = abs(endSnake)
    
                #snakes/ladders cannot be placed outside of the board or where another snake/ladder is placed
                if(board[startSnake] != 0 or board[endSnake] != 0 or startSnake < 1 or startSnake >= boardSize or endSnake < 1 or endSnake >= boardSize):
                    print("One of these spaces is occupied by another ladder or snake, or is outside of the valid range.")
                else:
                    board[startSnake] = endSnake
                    snakes[i] = startSnake
                    i = i + 1
            cont = 1

        
    


# In[95]:


smallBoardSize = boardSize - numSnakes #transition matrix will be reduced for calculation speed
smallBoard = [0]*smallBoardSize #spaces where snakes/ladders begin do not exist as far as the chain is concerned

bigMat = np.zeros((boardSize,boardSize),dtype = float) #full transition matrix
mat = np.zeros((smallBoardSize,smallBoardSize),dtype = float) #reduced transition matrix
transitionMat = np.zeros((smallBoardSize-1,smallBoardSize-1),dtype = float) #transition matrix without absorbing state
idty = np.zeros((smallBoardSize - 1,smallBoardSize - 1),dtype = float) #identity matrix of appropriate size

prob = 1/diceSize #probability of dice roll
exs = 0 #excess roll, used to calculate the probability of staying in the same state once near the final square
alrtSnake = 0 #will be used to see if the new position is the beginning of a snake/ladder
i = 0

#filling full transition matrix
for i in range(boardSize):
    alrtSnake = 0
    alrtSnake = checkSnake(snakes,numSnakes,i)
    if alrtSnake == 1:
        continue
    for j in range(1,diceSize+1):
        if i+j >= boardSize:
            exs = exs + 1
        else:
            if board[i+j] == 0:
                bigMat[i][i+j] += prob
            else:
                bigMat[i][board[i+j]] += prob
        bigMat[i][i] += (exs * prob)
        exs = 0


i2 = 0
j2 = 0
i = 0

#filling reduced transition matrix
for i in range(boardSize):
    alrtSnake = 0
    alrtSnake = checkSnake(snakes,numSnakes,i)
    if alrtSnake == 1:
        continue
    for j in range(boardSize):
        alrtSnake = checkSnake(snakes,numSnakes,j)
        if alrtSnake == 1:
            continue
        mat[i2][j2] = bigMat[i][j]
        j2 += 1
    j2 = 0
    i2 += 1

    
#filling identity matrix
i = 0
j = 0
for i in range(smallBoardSize-1):
    for j in range(smallBoardSize-1):
        if i == j:
            idty[i][j] = 1
        else:
            idty[i][j] = 0

#filling the transient matrix
i=0
j=0
for i in range(smallBoardSize-1):
    for j in range(smallBoardSize-1):
        transitionMat[i][j] = mat[i][j]
        
#calculating the fundamental matrix, recall that inv(I - Q) = N
ImQ = idty - transitionMat
N = np.linalg.inv(ImQ)       




# In[96]:


c = np.ones((smallBoardSize-1,1),dtype = float)
t = np.dot(N,c) #calculates the average times to absorption starting at each square, t[0] is the avg time starting from the beginning

print("Fundamental matrix: ")
print(N)
print("Average time to absorption: ")
print(t[0])


# In[ ]:




