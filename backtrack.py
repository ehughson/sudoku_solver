import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle

#reference: https://www.geeksforgeeks.org/backtracking-introduction/

class backtrack():
        def __init__(self, puzzle, base):
                self.grid =( [list( map(int,i) ) for i in puzzle] )
                self.box_size = base

        def foundSolution(self, i, j):

                for x in range(i,len(self.grid)):
                        for y in range(j,len(self.grid)):
                                if (self.grid[x][y] == 0) or self.grid[x][y] > len(self.grid):
                                        #print(self.grid[x][y])
                                        return x,y
                for x in range(0,len(self.grid)):
                        for y in range(0, len(self.grid)):
                                if (self.grid[x][y] == 0)or (self.grid[x][y] > len(self.grid)):
                                        return x,y
                return None, None

        def isValid(self, i, j, num):
                for x in range(len(self.grid)):
                        if self.grid[i][x] == num:
                                return False 
                
                for x in range(len(self.grid)):
                        if self.grid[x][j]  == num:
                                return False

                rowVal, colVal = self.box_size *(i//self.box_size), self.box_size *(j//self.box_size)
                for x in range(rowVal, rowVal+self.box_size):
                        for y in range(colVal, colVal+self.box_size):
                                if self.grid[x][y] == num:
                                        return False
                return True

        #i = 0
        def applyValue(self, i, j, val):
                self.grid[i][j] = val
                return 
        
        def removeValue(self, i, j):
                self.grid[i][j] = 0
                return


        def solveSudoku(self, i=0, j=0):
                i,j = self.foundSolution(i, j) #find next cell that is worth completing
                if i == None or j == None:
                        return True #puzzle is solved
                
                #print(len(self.grid)+1)
                for e in range(1,len(self.grid) +1):
                        if self.isValid(i,j,e):
                                self.applyValue(i, j, e)
                                #print(grid)
                                if self.solveSudoku( i, j):
                                        return self.grid
                                # Undo the current cell for backtracking
                                self.removeValue(i, j)
                                #print(i+1)
                return False




'''
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

'''
