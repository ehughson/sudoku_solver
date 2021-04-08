import numpy as np 
from random import sample


#class Sudoku():
#        def __init__(self, grid):




base = 3

side = base * base

def pattern(r, c):
    return (base * (r%base)+r//base+c)%side

def shuffle(s):
    return sample(s, len(s))

rBase = range(base)
rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
cols = [g*base +c for g in shuffle(rBase) for c in shuffle(rBase)]

nums = shuffle(range(1, base*base+1))

board = [ [ nums[pattern(r, c )] for c in cols] for r in rows]
print(board)


print("############### the following is the solution of the puzzle #################")
for line in board:
    print(line)


squares = side*side 
empties = squares *3//4 

for p in sample(range(squares), empties):
    board[p//side][p%side] = 0

print("############### the following is the puzzle with values removed #################")
numSize = len(str(side))

print(board)
for line in board:
    print("["+"  ".join(f"{n or '.':{numSize}}" for n in line)+"]")


def findNextCellToFill(grid, i, j):
        for x in range(i,9):
                for y in range(j,9):
                        if grid[x][y] == 0:
                                return x,y
        for x in range(0,9):
                for y in range(0,9):
                        if grid[x][y] == 0:
                                return x,y
        return -1,-1

def isValid(grid, i, j, e):
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
                columnOk = all([e != grid[x][j] for x in range(9)])
                if columnOk:
                        # finding the top left x,y co-ordinates of the section containing the i,j cell
                        secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
                        for x in range(secTopX, secTopX+3):
                                for y in range(secTopY, secTopY+3):
                                        if grid[x][y] == e:
                                                return False
                        return True
        return False

i = 0
def solveSudoku(grid, i=0, j=0):
        i,j = findNextCellToFill(grid, i, j)
        if i == -1:
                return True
        for e in range(1,10):
                if isValid(grid,i,j,e):
                        grid[i][j] = e
                        #print(grid)
                        if solveSudoku(grid, i, j):
                                return grid
                        # Undo the current cell for backtracking
                        grid[i][j] = 0
                        print(i+1)
        return False

backtrack_output = solveSudoku(board)
print(backtrack_output)
print("############### SOLVING SUDOKU #################")

for line in backtrack_output:
    print("["+"  ".join(f"{n or '.':{numSize}}" for n in line)+"]")




def expandLine(line):
    return line[0] + line[5:9].join([line[1:5]*(base-1)] *base) + line[9:13]

line0  = expandLine("╔═══╤═══╦═══╗")
line1  = expandLine("║ . │ . ║ . ║")
line2  = expandLine("╟───┼───╫───╢")
line3  = expandLine("╠═══╪═══╬═══╣")
line4  = expandLine("╚═══╧═══╩═══╝")

symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
nums   = [ [""]+[symbol[n] for n in row] for row in backtrack_output ]
print(line0)
for r in range(1,side+1):
    print( "".join(n+s for n,s in zip(nums[r-1],line1.split("."))) )
    print([line2,line3,line4][(r%side==0)+(r%base==0)])
