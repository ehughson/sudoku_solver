import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue

#constraint propogation with AC3

class AC3():
    def __init__(self, CSP):
                 self.grid = CSP

    def AC3_solve(self):
        q = queue.Queue()
        
        for arc in self.grid.constraints: #add all the arcs to a queue
            q.put(arc)
        while not q.empty():
            (x, y) = q.get() #get the first arc (x,y) off the queue
            values = set(self.grid.values[x])
            for p in values:
                if not self.isconsistent(p, x, y):
                    print("we are removing this value:", p)
                    print("before removing value:", self.grid.values[x])
                    self.grid.values[x] = "".join(c for c in self.grid.values[x] if c not in set(p))
                    print("after removing values:", self.grid.values[x])
                    if len(self.grid.values[x]) == 0:
                        print("here")
                        return False

                    for k in (self.grid.units[x]):
                        for v in k:
                            if v != x:
                                q.put((v, x)) #if the x domain has changed add all arcs of the form (k, x) to the queue
        
        #print(self.grid.values)
        sudoku_grid = []
        r = 0
        for key in self.grid.values:
            if r == 0:
                interarray = []
            r = r +1
            if len(self.grid.values[key]) > 1:
                print("WE HAVE AN ERROR -- VALUE CONTAINS MORE THAN ONE VALUE")
                exit(-1)
            interarray.append(self.grid.values[key])
            if r == 9:
                r = 0
                sudoku_grid.append(interarray)
            #print(val)
        print(sudoku_grid)
        #self.grid.print_sudoku(self.grid.values)
        return sudoku_grid


    def isconsistent(self, x, Xi, Xj):
        for y in self.grid.values[Xj]:
            for peer in self.grid.units[Xi]:
                if Xj in peer and y!= x:
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
        #print(3//4)
        empties = (side*side) * 3//6
        #empties = 37

        #print(empties)

        for p in sample(range(side*side), empties):
                board[p//side][p%side] = 0
        
        #print(board)
        print(board)
        test_bt = SudokuPuzzle(board)
        #print("the results of sudokupuzzle:",  test_bt.board)
        #print("the symbols are:", test_bt.symbols)
        sudoku = AC3(test_bt)
        final_sudoku = sudoku.AC3_solve()
        print(final_sudoku)
        test_bt.print_sudoku(final_sudoku)