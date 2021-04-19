import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue



class AC3():
    def __init__(self, CSP):
                 self.grid = CSP

    def AC3_solve(self):
        q = queue.Queue()
        
        for arc in self.grid.constraints: #add all the arcs to a queue
            q.put(arc)

        #print("what is the queue size?", q.qsize())
        #print(self.values)
        i = 0
        #print("entering queue")
        while not q.empty():
            (x, y) = q.get() #get the first arc (x,y) off the queue
            #values = set(self.values[x])
            i = i + 1 
            #if self.Revise(x, y):
            values = set(self.grid.values[x])
            for p in values:
                if not self.isconsistent(p, x, y):
                    self.grid.values[x] = self.grid.values[x].replace(p, '')
                    #print(self.values[x])
                    if len(self.grid.values[x]) == 0:
                        #print(self.values[x])
                        return False

                    for k in (self.grid.peers[x] - set(y)): #remove values from x domain for which there is no possible corresponding y domain
                        q.put((k, x)) #if the x domain has changed add all arcs of the form (k, x) to the queue

                        #print("what is the queue size?", q.qsize())
        
        #print(i)
        self.display(self.grid.values)
        return True 



    def isconsistent(self, x, Xi, Xj):
        for y in self.grid.values[Xj]:
            if Xj in self.grid.peers[Xi] and y!=x:
                return True

        return False

    def display(self, values):
        for r in self.grid.rows:
            if r in 'DG':
                print ("------------------------------------------------------------------------------")
            for c in self.grid.cols:
                if c in '47':
                    print (' | ', values[r+c], ' ',end=' ')
                else:
                    print (values[r+c], ' ',end=' ')
            print (end='\n')
    
    def isComplete(self):
        for variable in self.grid.squares:
            if len(self.grid.values[variable])>1:
                return False
        return True

    def write(self, values):
        output = ""
        for variable in self.grid.squares:
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
        
        #squares = side*side 
        print(3//4)
        empties = (side*side) * 3//6
        #empties = 37

        print(empties)

        for p in sample(range(side*side), empties):
                board[p//side][p%side] = 0
        
        #print(board)
        print(board)
        test_bt = SudokuPuzzle(board)
        print("the results of sudokupuzzle:",  test_bt.board)
        print("the symbols are:", test_bt.symbols)
        #"000260701680070090190004500820100040004602900050003028009300074040050036703018000"
        #board = [[0,0,0,2,6,0,7,0,1],[6,8,0,0,7,0,0,9,0],[1,9,0,0,0,4,5,0,0],[8,2,0,1,0,0,0,4,0],[0,0,4,6,0,2,9,0,0],[0,5,0,0,0,3,0,2,8],[0,0,9,3,0,0,0,7,4],[0,4,0,0,5,0,0,3,6],[7,0,3,0,1,8,0,0,0]]

        sudoku = AC3(test_bt)
        final_sudoku = sudoku.AC3_solve()
        #ac3_results = sudoku.AC3()