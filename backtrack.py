import numpy as np 
from random import sample
from math import sqrt
import time
from SudokuPuzzle import SudokuPuzzle

#reference: https://www.geeksforgeeks.org/backtracking-introduction/
#https://www.geeksforgeeks.org/sudoku-backtracking-7/
#https://afteracademy.com/blog/sudoku-solver

class backtrack():

        def __init__(self, puzzle, base):
                self.puzzle =( [list( map(int,i) ) for i in puzzle] )
                self.box_size = base

        def foundSolution(self, i, j):

                for x in range(i,len(self.puzzle)):
                        for y in range(j,len(self.puzzle)):
                                if (self.puzzle[x][y] == 0) or (self.puzzle[x][y] > len(self.puzzle)):
                                        #print(self.grid[x][y])
                                        return x,y
                for x in range(len(self.puzzle)):
                        for y in range(len(self.puzzle)):
                                if (self.puzzle[x][y] == 0)or (self.puzzle[x][y] > len(self.puzzle)):
                                        return x,y
                return None, None

        def isSafe(self, i, j, num):
                for x in range(len(self.puzzle)):
                        if self.puzzle[i][x] == num:
                                return False 
                
                for x in range(len(self.puzzle)):
                        if self.puzzle[x][j]  == num:
                                return False

                rowVal = self.box_size *(i//self.box_size)
                colVal =  self.box_size *(j//self.box_size)
                for x in range(rowVal, rowVal+self.box_size):
                        for y in range(colVal, colVal+self.box_size):
                                if self.puzzle[x][y] == num:
                                        return False
                return True

        #i = 0
        def applyValue(self, i, j, val):
                self.puzzle[i][j] = val
                return 
        
        def removeValue(self, i, j):
                self.puzzle[i][j] = 0
                return


        def solveBacktrack(self, i=0, j=0 ):
                i, j = self.foundSolution(i, j) #find next cell that is worth completing
                if i == None or j == None:
                        return True #puzzle is solved
                
                for val in range(1,len(self.puzzle) +1):
                        if self.isSafe(i,j,val):
                                self.applyValue(i, j, val)
                                #print(grid)
                                self.solveBacktrack(i, j)
                                self.removeValue(i, j)
                                #print(i+1)
                return False




