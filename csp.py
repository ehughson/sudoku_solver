import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue

digits =  cols = "123456789"
rows = "ABCDEFGHI"


#FINDING THE CROSS PRODUCT OF TWO SETS 
def cross(A, B):
	return [a + b for a in A for b in B]

squares = cross(rows, cols)
print(squares)

class csp:
    #INITIALIZING THE CSP
    def __init__ (self, grid, domain = digits):
        digits =  cols = "123456789"
        rows = "ABCDEFGHI"


        #FINDING THE CROSS PRODUCT OF TWO SETS 
        def cross(A, B):
            return [a + b for a in A for b in B]

        self.squares = cross(rows, cols)
        #print(squares)
        #print(self.variables)
        self.domain = self.getDict(grid)
        self.values = self.getDict(grid)		
        #print(self.values)

        self.unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

        
        #print(self.unitlist)
        #print(self.squares)
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.squares)
        self.constraints = {(variable, peer) for variable in self.squares for peer in self.peers[variable]}

	#GETTING THE STRING AS INPUT AND RETURNING THE CORRESPONDING DICTIONARY
    def getDict(self, grid):
        i = 0
        j = 0
        values = dict()
        #print(self.squares)

        for cell in self.squares:
            #print(grid)
            if j < 9:
                if grid[j][i]!=0:
                    #print("the grid is:", grid[j][i])
                    #print("what is j?",j)
                    values[cell] = grid[j][i]
                else:
                    values[cell] = digits
                i = i +1
                if i == 9:
                    i = 0
                    j = j + 1 
        #print(values)
        return values

    def AC3(self):
        q = queue.Queue()

        for arc in self.constraints:
            q.put(arc)

        #print(self.values)
        i = 0
        while not q.empty():
            (Xi, Xj) = q.get()
            print(Xi)
            print(Xj)

            i = i + 1 

            if self.Revise(Xi, Xj):
                if len(self.values[Xi]) == 0:
                    return False

                for Xk in (self.peers[Xi] - set(Xj)):
                    q.put((Xk, Xi))

        return True 



    #WORKING OF THE REVISE ALGORITHM
    def Revise(self, Xi, Xj):
        #print(Xi)
        revised = False
        #print(self.values[Xi])
        values = set(str(self.values[Xi]))
        print(values)

        for x in values:
            if not self.isconsistent(x, Xi, Xj):
                self.values[Xi] = self.values[Xi].replace(x, '')
                revised = True 

        return revised 

    def isconsistent(self, x, Xi, Xj):
        print("what is the value?", self.values[Xj])
        #print(list(self.values[Xj]))
        yvalues = set(str(self.values[Xj]))
        for y in yvalues:
            if Xj in self.peers[Xi] and y!=x:
                return True

        return False


if __name__ == '__main__':
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

        board = [[ nums[pattern(r, c )] for c in cols] for r in rows]
        
        squares = side*side 
        empties = squares *3//4 

        for p in sample(range(squares), empties):
                board[p//side][p%side] = 0
        
        print(board)

        sudoku = csp(board)

        ac3_results = sudoku.AC3()
        print(ac3_results)
        #for grid in board:
        #        #prev = time.time()
        #        print(grid)
        #        sudoku = csp(grid=grid)
        
        #print(sudoku.constraints)