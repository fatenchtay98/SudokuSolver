#Soduko Solver Using Three Algorithms: Brute Force - Backtracking with GUI - Depth First Search
import turtle  # turtle graphics are vector graphics that use relative cursor upon in a cartesian plane
import time
from time import sleep
import copy

t = turtle.Turtle()
t.speed(0)
easy_board= [
        [5, 3, 8, 0, 1, 6, 0, 7, 9],
        [0, 0, 0, 3, 8, 0, 5, 4, 1],
        [2, 4, 1, 5, 0, 0, 0, 0, 0],
        [0, 6, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 5, 0, 0, 0],
        [0, 9, 0, 0, 0, 4, 0, 0, 2],
        [6, 0, 0, 2, 0, 0, 9, 3, 0],
        [1, 2, 9, 0, 4, 0, 0, 5, 0],
        [0, 5, 4, 6, 9, 0, 0, 0, 8]]

medium_board = [
        [3, 1, 6, 5, 0, 8, 4, 0, 2],
        [5, 2, 9, 0, 0, 4, 7, 0, 8],
        [4, 8, 7, 0, 2, 9, 0, 3, 1],
        [0, 6, 3, 4, 1, 0, 9, 8, 7],
        [9, 7, 0, 8, 6, 3, 1, 2, 5],
        [0, 5, 1, 0, 9, 0, 6, 4, 0],
        [1, 3, 0, 9, 0, 7, 2, 5, 6],
        [6, 0, 2, 3, 0, 1, 0, 7, 4],
        [7, 0, 5, 2, 0, 6, 3, 1, 9]]

hard_board = [
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 8, 5],
        [0, 0, 7, 0, 4, 8, 0, 5, 0],
        [0, 0, 1, 3, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 7, 0, 0, 0, 0],
        [8, 6, 0, 0, 0, 0, 9, 0, 3],
        [7, 0, 0, 0, 0, 5, 0, 6, 2],
        [0, 0, 3, 7, 0, 0, 0, 0, 0]]

class Problem(object):
    def __init__(self, init):
        self.init = init
#function to check that there is no empty cell
    def goal(self, s):
       for i in range(0,9):
        for j in range(0,9):
            if s[i][j] == 0:
                return False
       return True

# function that will check if a number is not found among the used values, if it doesnt found it then it will return all the available numbers that can be placed
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

# function taht will return the coordinates(i,j) for the first empty box
    def position(self, board, s):
        for i in range(board):
            for j in range(board):
                if s[i][j] == 0:
                    return i, j

# function that will return the values that are not used in the row
    def row_values(self, s, row):
        values = range(1, 10)
        x = [number for number in s[row] if (number != 0)]
        y = self.filter_values(values, x)
        return y

#function that will return the values that are not used in the row
    def col_values(self, y, s, column):
        x = [] # to store the possible values
        for index in range(9):
            if s[index][column] != 0:
                x.append(s[index][column])
                #print(x)
        y = self.filter_values(y, x)
        #print(y)
        return y

#function that will return the values that are not used in the 3x3 square
    def box_values(self, options, s, row, column):
        x = []
        r = int(row/3)*3
        c = int(column/3)*3
        for i in range(0, 3):
            for j in range(0,3):
                x.append(s[r + i][c + j])
        y = self.filter_values(options, x)
        return y

    def actions(self, s):
        row,column = self.position(9, s) #call function to get the first 0/empty cell
  #Call the (rows, col, box) functions to remove the undesired numbers from that row,column location
        numbers = self.row_values(s, row)
        numbers = self.col_values(numbers, s, column)
        numbers = self.box_values(numbers, s, row, column)
  #Since we have many options, we will use yield instead of return (it allows the code to produce a series of values over time for each state)
        for number in numbers:
            new = copy.deepcopy(s) #we dont want to change the original grid so we use the deepcopy function
            new[row][column] = number
            yield new

class Node:
    def __init__(self, s):
        self.s = s
#return a list of all the possible grids
    def expand(self, problem):
        return [Node(s) for s in problem.actions(self.s)]

def DFS(problem):
    start = Node(problem.init)
    if problem.goal(start.s):
        return start.s
    stack = []
    stack.append(start) #to place init node onto the stack

    while stack:
        node = stack.pop()
        if problem.goal(node.s): # if we reach goal
            return node.s
        stack.extend(node.expand(problem)) #else we add another to the stack
    return None

def solve_dfs(board):
    problem = Problem(board)
    solution = DFS(problem)
    if solution:
        print ("The solution using DFS is:\n")
        for row in solution:
            print(row)
    else:
        print ("No solution found")

def isComplete():
    for row in board:
        for col in row:
            if (col == "0"):
                return False
    return True

def solve():
    global board
    if isComplete():
        return True

    i, j = 0, 0
    for rowIdx, row in enumerate(board):
        for colIdx, col in enumerate(row):
            if col == "0":
                i, j = rowIdx, colIdx

    possibilities = values_possible(i, j) #all the possible numbers in that square
    for value in possibilities:
        snapshot = copy.deepcopy(board)

        board[i][j] = value
        result = solve()
        if result == True:
            return True
        else:
            board = copy.deepcopy(snapshot)

    return False

def values_possible(i, j):
    global board
    if board[i][j] != "0": #Not empty
        return False
    #we need to find possible numbers {'1','2'..} as a set (we can edit it)
    values = {str(n) for n in range(1, 10)}

    # to remove existing numbers in rows
    for value in board[i]:
        values -= set(value)

    # to remove existing numbers in columns
    for col in range(0, 9):
        values = values - set(board[col][j])

    # to remove existing numbers in 3x3 box
    xbox = (i // 3) * 3 #to get integer division
    ybox = (j // 3) * 3

    square = board[ xbox: xbox + 3]
    for i, row in enumerate(square):
        square[i] = row[ybox : ybox + 3]

    for row in square:
        for col in row:
            values -= set(col)
    #all available values
    return list(values)

def printBoard():
    global board
    for i in range(0, 9):
        if i % 3 == 0 and i != 0:  # for i=3,6 and 9
            print("- - - - - - - - - - - - - ")
        for j in range(0, 9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
def BF():
    global board
    # to convert list of strings into list of lists
    for i, nb in enumerate(board):
        board[i] = list(nb)
    solve()
    printBoard()

# function that will return true if there is no empty cell left
def findempty(x):
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i][j] == 0:
                return False
    return True


# A procedure to draw the grid on screen using Python Turtle
def printgrid(z):
    x = -100
    y = 100

    for row in range(0, 10):
        if (row % 3) == 0:
            t.pensize(3)  # to draw lines in bold
        else:
            t.pensize(1)  # to draw normal lines
        t.penup()  # to pick up the turtle’s Pen
        t.goto(x, y - row * 25)  # to move the turtle to position x,y
        t.pendown()  # to put down the turtle’s Pen
        t.goto(x + 225, y - row * 25)

    for col in range(0, 10):
        if (col % 3) == 0:
            t.pensize(3)
        else:
            t.pensize(1)
        t.penup()
        t.goto(x + col * 25, y)
        t.pendown()
        t.goto(x + col * 25, y - 225)

    for row in range(0, 9):
        for col in range(0, 9):
            if z[row][col] != 0:
                t.penup()
                t.goto(col * 25 - 90, 80 - row * 25)
                t.write(z[row][col])


# Backtracking function to find a solution
def backtrack(x):
    group = []

    for i in range(0, 81):
        row = i // 9  # floor division
        col = i % 9
        if x[row][col] == 0:  # empty cell
            for nb in range(1, 10):  # to get nb from 1 till 9
                if (nb in x[row]) == False:  # to check if that nb is not already in the row
                    if not nb in (
                    x[0][col], x[1][col], x[2][col], x[3][col], x[4][col], x[5][col], x[6][col], x[7][col],
                    x[8][col]):  # to check if it is in the column
                        # Identify which of the 9 squares we are working on
                        if row == 0 or row == 1 or row == 2:
                            if col < 3:  # first box
                                group.append(x[0][0:3])
                                group.append(x[1][0:3])
                                group.append(x[2][0:3])
                            elif col < 6:  # second box
                                group.append(x[0][3:6])
                                group.append(x[1][3:6])
                                group.append(x[2][3:6])
                            else:  # third box
                                group.append(x[0][6:9])
                                group.append(x[1][6:9])
                                group.append(x[2][6:9])
                        elif row == 3 or row == 4 or row == 5:
                            if col < 3:  # forth box
                                group.append(x[3][0:3])
                                group.append(x[4][0:3])
                                group.append(x[5][0:3])
                            elif col < 6:  # fifth box
                                group.append(x[3][3:6])
                                group.append(x[4][3:6])
                                group.append(x[5][3:6])
                            else:  # sixth box
                                group.append(x[3][6:9])
                                group.append(x[4][6:9])
                                group.append(x[5][6:9])
                        else:
                            if col < 3:  # seventh box
                                group.append(x[6][0:3])
                                group.append(x[7][0:3])
                                group.append(x[8][0:3])
                            elif col < 6:  # eighth box
                                group.append(x[6][3:6])
                                group.append(x[7][3:6])
                                group.append(x[8][3:6])
                            else:  # ninth box
                                group.append(x[6][6:9])
                                group.append(x[7][6:9])
                                group.append(x[8][6:9])

                        total = group[0] + group[1] + group[2]

                        if not nb in total:  # to see if this number exist in the 3x3 group
                            x[row][col] = nb
                            t.clear()
                            printgrid(x)
                            t.getscreen().update()

                            if findempty(x) == True:
                                return True
                            else:
                                if backtrack(x) == True:
                                    return True
            break  # to break the loop if condition satisfies

    x[row][col] = 0  # if not we need to backtrack


print('Enter a number to choose the Algorithm You want: 1 = Brute Force - 2 = DFS - 3 = Backtracking With GUI')
alg = input()
if(alg == '1'):
    print('Enter a number to choose the difficulty of Sudoku Game:1 = Easy - 2 = Medium - 3 = Hard')
    level = input()
    start_time = time.time()
    if(level == '1'):
        board = [
        "538016079",
        "000380541",
        "241500000",
        "060900000",
        "000035000",
        "090004002",
        "600200930",
        "129040050",
        "054690008"]
        BF()
    elif(level == '2'):
        board = [
        "316508402",
        "529004708",
         "487029031",
        "063410987",
        "970863125",
        "051090640",
        "130907256",
        "602301074",
        "705206319"]
        BF()
    elif(level == '3'):
        board = [
        "400000000",
        "000009000",
        "000000785",
        "007048050",
        "001300000",
        "006070000",
        "860000903",
        "700005062",
        "003700000"]
        BF()
    else:
        print("Enter a valid number 1,2 or 3")
    print("%s seconds" % (time.time() - start_time))
elif(alg =='2'):
    print('Enter a number to choose the difficulty of Sudoku Game:1 = Easy - 2 = Medium - 3 = Hard')
    level = input()
    start_time = time.time()
    if (level == '1'):
        solve_dfs(easy_board)
    elif (level == '2'):
        solve_dfs(medium_board)
    elif (level == '3'):
        solve_dfs(hard_board)
    else:
        print("Enter a valid number 1,2 or 3")
    print("%s seconds" % (time.time() - start_time))

elif(alg == '3'):
    print('Enter a number to choose the difficulty of Sudoku Game:1 = Easy - 2 = Medium - 3 = Hard')
    level = input()
    if (level == '1'):
        x = easy_board
    elif(level == '2'):
        x = medium_board
    elif (level == '3'):
        x = hard_board
    else:
        print("Enter a valid number 1,2 or 3")
    printgrid(x)
    start_time = time.time()
    t.getscreen().update()
    sleep(1)  # to wait for 1 second
    if backtrack(x) == True:
        print("Solution is found after:")
    else:
        print("Can't find solution")
    print("%s seconds" % (time.time() - start_time))
else:
    print("Enter a valid number 1,2 or 3")