#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <math.h>

using namespace std;

int getInt();

int main()
{
    srand(time(NULL));

    int boardSize;
    boardSize = 101; //initialize board size variable to default size (including square "zero")
    cout << "How many spaces would you like the board to have? (standard size is 101, including ''zero space'') \n";
    boardSize = getInt();
    boardSize = abs(boardSize); //no negatives allowed

    int board[boardSize];
    int i = 0;

    for(i=0;i<boardSize;i++) //board is initially filled with zeros; squares that lead to snakes and ladders will be marked with ending position
        board[i] = 0; //later, a nonzero value in a square will indicate needing to shift the position due to a snake/ladder


    int ans; //variable that will store yes/no answers in the following questions, indicates if path to take
    ans = -1;
    while(ans!=0 && ans!=1)
    {
        cout << "\nWould you like to simulate the usual snake and ladder positions?\n0: Yes \n1: No\n";
        ans = getInt();
        if(ans!=0 && ans!=1)
            {
                cout << "\nInvalid entry.\n";
                ans = -1;
            }
    }

    if(ans == 0 && boardSize >= 101)
    {
        //snake and ladder positions based on original Milton Bradley board
        //ladders
        board[1] = 38;
        board[4] = 14;
        board[9] = 31;
        board[21] = 42;
        board[28] = 84;
        board[36] = 44;
        board[51] = 67;
        board[71] = 91;
        board[80] = 100;

        //snakes
        board[98] = 78;
        board[95] = 75;
        board[93] = 73;
        board[87] = 24;
        board[64] = 60;
        board[62] = 19;
        board[56] = 53;
        board[49] = 11;
        board[48] = 26;
        board[16] = 6;
    }

    if(ans == 0 && boardSize < 101)
    {
        cout << "\nUsual positions not possible due to chosen board size being too small. Please enter snake and ladder spaces manually.\n";
        ans = 1;
    }

    int numSnakes; //number of total snakes and ladders to be placed (I just like snakes)
    numSnakes = 19; //initialized to 19, the standard number of snakes/ladders on a standard board
    int k; //counter for this process
    k = 0;
    int startSnake;
    int endSnake;
    startSnake = 0;
    endSnake = 0;
    int validEntry;
    validEntry = -1;
    int cont;
    cont = 0;
    int checkSpace;
    checkSpace = -1;
    if(ans == 1)
    {
        while(cont != 1)
        {
            cout << "\nHow many snakes and ladders would you like to place in total?\n";
            numSnakes = getInt();
            numSnakes = abs(numSnakes); //no negatives allowed

            if(numSnakes >= boardSize)
            {
                cout << "\nToo many snakes, there are only " << boardSize - 1 << " valid spaces.\n";
                validEntry = -1;
            }
            else
                validEntry = 1;

            if(validEntry == 1) //snakes/ladders cannot be places until a valid number is selected
            {
                k = 0;
                while(k<numSnakes)
                {
                    cout << "\nWhere does snake/ladder #" << k+1 << " begin?\n";
                    startSnake = getInt();
                    cout << "\nWhere does snake/ladder #" << k+1 << " end?\n";
                    endSnake = getInt();
                    if(board[startSnake] != 0 || board[endSnake] != 0 || startSnake < 1 || startSnake >= boardSize || endSnake < 1 || endSnake >= boardSize) //doesn't allow a single square to be the start of multiple snakes/ladders; doesn't allow snakes/ladders to be placed off the board
                    {
                        cout << "\nOne of these spaces is occupied by another ladder or snake, or is outside of the valid range.\n";
                    }
                    else
                    {
                        board[startSnake] = endSnake; //places snake/ladder if the option is valid
                        k++;
                    }
                }
                cont = 1; //once all snakes and ladders have been appropriately placed, the program continues
            }
        }
    }


    //number of visits per space
    float visits[boardSize];
    for(k=0;k<boardSize;k++)
            visits[k] = 0;

    //player position on board
    int pos;
    pos = 0;

    //avg time to absorption
    double tta;
    tta = 0;

    //will take a value 1-diceSize for dice rolls
    int dice;
    dice = 0;
    int diceSize;
    diceSize = -1;
    cout << "\nHow many sides should the die have?\n";
    diceSize = getInt();
    diceSize = abs(diceSize); //no negatives allowed


    //will be used to check if the position occupied is the start of a snake or a ladder
    int snakecheck;
    snakecheck = -1;

    //counter for simulation iterations
    int j;
    j=0;

    //number of games played
    int N;
    N = 1000000;
    cout << "\nHow many games should be simulated? (Please be nice to your CPU)\n";
    N = getInt();
    N = abs(N); //no negatives allowed

    for(j=0;j<N;j++)
    {
        while(pos != (boardSize - 1)) //game ends once player has reached square 100
        {
            /*if(tta > 100000000) //failsafe
                {
                    cout << "\nLoop broken, possible inescapable cycle found\n";
                    break;
                }*/
            tta += 1; //every dice roll counts as a turn (step in time to absorption)
            dice = (rand() % diceSize) + 1; //dice roll
            if(pos + dice < boardSize) //position only moves if there are enough spaces (e.g. can't move 5 spaces from square 96 on a standard board)
            {
                pos = pos + dice;
            }

            snakecheck = board[pos]; //checks if the position has a snake or ladder and shifts accordingly if so
            if(snakecheck != 0)
                pos = snakecheck;
            visits[pos] += 1; //counter for the number of times player visits a certain space
        }
        pos = 0; //resets position for next iteration
    }

    cout << "\nSimulation parameters:\n";
    cout << "\nNumber of spaces, including ''zero'' space: " << boardSize;
    cout << "\nNumber of sides on the die: " << diceSize;
    cout << "\nNumber of total snakes and ladders: " << numSnakes;
    cout << "\n\nPositions of each:\n";
    for(i=0;i<boardSize;i++)
    {
        if(board[i]!=0)
            cout << "\nSnake/ladder from position " << i << " to position " << board[i];
    }

    cout << "\n\n\nResults of simulation:\n";
    cout << "\nAverage visits per space: \n\n";
    for(i=0;i<boardSize;i++)
        cout << "position " << i << ": " << visits[i]/N << "\n";
    cout << "\n\nAverage time to absorption: " << tta/N << endl;

    return 0;
}

int getInt()
{
    int val;
    while(true)
    {
        cin >> val;
        if(cin.fail())
        {
            cin.clear();
            cin.ignore(32767,'\n');
            cout << "\nInvalid input, please enter a positive integer.\n";
        }
        else
        {
            cin.ignore(32767,'\n');
            return val;
        }
    }
}
