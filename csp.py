import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue


class csp:
    #INITIALIZING THE CSP
    def __init__ (self,grid = ""):
        self.digits =  self.cols = "123456789"
        self.rows = "ABCDEFGHI"
        #FINDING THE CROSS PRODUCT OF TWO SETS 

        def cross(A, B):
            return [a + b for a in A for b in B]

        self.squares = cross(self.rows, self.cols)
        #print(self.squares)
        self.domain = self.getDict(grid)
        self.values = self.getDict(grid)		
        #print("here are the domains: ", len(self.domain))
        #print("here are the values:", len(self.values))

        print("here are the cols:", self.cols)
        self.unitlist = ([cross(self.rows, c) for c in self.cols] + [cross(r, self.cols) for r in self.rows] + [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
        
        #print(self.unitlist)
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
        
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.squares)
        #print(self.peers)
        self.constraints = {(variable, peer) for variable in self.squares for peer in self.peers[variable]} #all the arcs A<B = A<B and B<A
        #print(self.constraints)
        #print("here are the constraints:", len(self.constraints))

    def getDict(self, grid =""):
        i = 0
        j = 0
        values = dict()
        
        print(grid)
        for cell in self.squares:
            #print(grid)
            if j < 9:
                if grid[j][i]!=0:
                    values[cell] = str(grid[j][i])
                else:
                    values[cell] = self.digits
                i = i +1
                if i == 9:
                    i = 0
                    j = j + 1 
        print(values)
        return values

    def AC3(self):
        q = queue.Queue()
        
        for arc in self.constraints: #add all the arcs to a queue
            q.put(arc)

        #print("what is the queue size?", q.qsize())
        #print(self.values)
        i = 0
        print("entering queue")
        while not q.empty():
            (x, y) = q.get() #get the first arc (x,y) off the queue
            #values = set(self.values[x])
            i = i + 1 
            #if self.Revise(x, y):
            values = set(self.values[x])
            for p in values:
                if not self.isconsistent(p, x, y):
                    self.values[x] = self.values[x].replace(p, '')
                    #print(self.values[x])
                    if len(self.values[x]) == 0:
                        #print(self.values[x])
                        return False

                    for k in (self.peers[x] - set(y)): #remove values from x domain for which there is no possible corresponding y domain
                        q.put((k, x)) #if the x domain has changed add all arcs of the form (k, x) to the queue

                        #print("what is the queue size?", q.qsize())
        
        print(i)
        self.display(self.values)
        return True 



    def isconsistent(self, x, Xi, Xj):
        for y in self.values[Xj]:
            if Xj in self.peers[Xi] and y!=x:
                return True

        return False

    def display(self, values):
        for r in self.rows:
            if r in 'DG':
                print ("------------------------------------------------------------------------------")
            for c in self.cols:
                if c in '47':
                    print (' | ', values[r+c], ' ',end=' ')
                else:
                    print (values[r+c], ' ',end=' ')
            print (end='\n')
    
    def isComplete(self, csp):
        for variable in squares:
            if len(csp.values[variable])>1:
                return False
        return True

    def write(self, values):
        output = ""
        for variable in self.squares:
            output = output + str(values[variable])
        return output


if __name__ == '__main__':
        base = 3

        side = base * base

        def pattern(r, c):
                return (base * (r%base)+r//base+c)%side

        def shuffle(s):
                return sample(s, len(s))

        rBase = range(base)
        rows1 = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        colum = [g*base +c for g in shuffle(rBase) for c in shuffle(rBase)]

        nums = shuffle(range(1, base*base+1))

        board = [[ nums[pattern(r, c )] for c in colum] for r in rows1]
        
        squares = side*side 
        empties = squares *3//4 

        for p in sample(range(squares), empties):
                board[p//side][p%side] = 0
        
        print(board)
        board = [[0,0,3,0,2,0,6,0,0],[9,0,0,3,0,5,0,0,1],[0,0,1,8,0,6,4,0,0],[0,0,8,1,0,2,9,0,0],[7,0,0,0,0,0,0,0,8],[0,0,6,7,0,8,2,0,0],[0,0,2,6,0,9,5,0,0],[8,0,0,2,0,3,0,0,9],[0,0,5,0,1,0,3,0,0]]



        test_bt = SudokuPuzzle(board)
        print(test_bt)
        print("the results of sudokupuzzle:",  test_bt.board)
        sudoku = csp(grid=board)

        ac3_results = sudoku.AC3()
        #print(sudoku.values)
        #print(sudoku.write(sudoku.values))
        #print(sudoku.display(sudoku.values))
        #print(ac3_results)
        #for grid in board:
        #        #prev = time.time()
        #        print(grid)
        #        sudoku = csp(grid=grid)
        
        #print(sudoku.constraints)