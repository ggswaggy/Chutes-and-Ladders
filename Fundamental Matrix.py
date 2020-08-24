#!/usr/bin/env python
# coding: utf-8

# In[35]:


import numpy as np
from numpy import array


# In[36]:


def checkSnake(vec, length, find):
    for i in range (length):
        if vec[i] == find:
            return 1
    return 0


# In[37]:


boardSize = int(input("How many spaces would you like the board to have? (standard size is 101, including 'zero' space): "))
boardSize = abs(boardSize)

board = [0]*boardSize

diceSize = int(input("How many sides on the die?: "))
diceSize = abs(diceSize)

numSnakes = int(input("How many snakes/ladders would you like to have in total?: "))
numSnakes = abs(numSnakes)

snakes = [None]*numSnakes
startSnake = -1
endSnake = -1
i=0
while i < numSnakes:
    startSnake = int(input("Where does snake/ladder # %d begin?: " %(i+1)))
    endSnake = int(input("Where does snake/ladder # %d end?: " %(i+1)))
    startSnake = abs(startSnake)
    endSnake = abs(endSnake)
    
    if(board[startSnake] != 0 or board[endSnake] != 0 or startSnake < 1 or startSnake >= boardSize or endSnake < 1 or endSnake >= boardSize):
        print("One of these spaces is occupied by another ladder or snake, or is outside of the valid range.")
    else:
        board[startSnake] = endSnake
        snakes[i] = startSnake
        i = i + 1


    


# In[56]:


smallBoardSize = boardSize - numSnakes
smallBoard = [0]*smallBoardSize

bigMat = np.zeros((boardSize,boardSize),dtype = float)
mat = np.zeros((smallBoardSize,smallBoardSize),dtype = float)
transitionMat = np.zeros((smallBoardSize-1,smallBoardSize-1),dtype = float)
idty = np.zeros((smallBoardSize - 1,smallBoardSize - 1),dtype = float)

prob = 1/diceSize
exs = 0
alrtSnake = 0
i = 0

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

    
i = 0
j = 0
for i in range(smallBoardSize-1):
    for j in range(smallBoardSize-1):
        if i == j:
            idty[i][j] = 1
        else:
            idty[i][j] = 0

i=0
j=0
for i in range(smallBoardSize-1):
    for j in range(smallBoardSize-1):
        transitionMat[i][j] = mat[i][j]
        
ImQ = idty - transitionMat
N = np.linalg.inv(ImQ)       




# In[61]:


c = np.ones((smallBoardSize-1,1),dtype = float)
t = np.dot(N,c)

print("Fundamental matrix: ")
print(N)
print("Average time to absorption: ")
print(t[0])

