import numpy as np
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue

class AC3():
    """
    A class to represent a Sudoku solver using Constraint Satisfaction Problem
    Reference : <TO BE ADDED>

    About the algorithm
    <TO BE ADDED>

    Attributes
    ----------
    csp : object of the SudokuPuzzle class

    Methods
    -------
    AC3_solve
        solver for the sudoku
    successor_function
        generates the successor of the current state
    heuristic function
        calculates the heuristic of the current state
    """

    def __init__(self, csp: SudokuPuzzle):
        """
        input is the Sudoku puzzle
        """
        self.grid = csp

    def AC3_solve(self):
        """
        Solver for AC3 CSP
        """
        q = queue.Queue()
        for arc in self.grid.constraints:  # add all the arcs to a queue
            q.put(arc)
        while not q.empty():
            (x, y) = q.get()  # get the first arc (x,y) off the queue
            values = set(self.grid.values[x])
            for p in values:
                if not self.isconsistent(p, x, y):
                    self.grid.values[x] = "".join(c for c in self.grid.values[x] if c not in set(p))
                    if len(self.grid.values[x]) == 0:
                        return False
                    for k in (self.grid.units[x]):
                        for v in k:
                            if v != x:
                                q.put(
                                    (v, x))  # if the x domain has changed add all arcs of the form (k, x) to the queue

        sudoku_grid = []
        r = 0
        for key in self.grid.values:
            if r == 0:
                interarray = []
            r = r + 1
            if len(self.grid.values[key]) > 1:
                print("WE HAVE AN ERROR -- VALUE CONTAINS MORE THAN ONE VALUE")
                exit(-1)
            interarray.append(self.grid.values[key])
            if r == self.grid.size:
                r = 0
                sudoku_grid.append(interarray)
        return sudoku_grid

    def isconsistent(self, x, Xi, Xj):
        for y in self.grid.values[Xj]:
            for peer in self.grid.units[Xi]:
                if Xj in peer and y != x:
                    return True
        return False

if __name__ == '__main__':

    board = [["1",""],["","1"]]
    # board = [["2","1","",""],["4","","1","2"],["1","","",""],["3","4","","1"]]
    #board = [["2","","",""],["","","2",""],["","4","",""],["","","","3"]]
    # board = [
    #     ["", "", "", "2", "6", "", "7", "", "1"],
    #     ["6", "8", "", "", "7", "", "", "9", ""],
    #     ["1", "9", "", "", "", "4", "5", "", ""],
    #     ["8", "2", "", "1", "", "", "", "4", ""],
    #     ["", "", "4", "6", "", "2", "9", "", ""],
    #     ["", "5", "", "", "", "3", "", "2", "8"],
    #     ["", "", "9", "3", "", "", "", "7", "4"],
    #     ["", "4", "", "", "5", "", "", "3", "6"],
    #     ["7", "", "3", "", "1", "8", "", "", ""],
    # ]

    test_bt = SudokuPuzzle(board)
    sudoku = AC3(test_bt)
    final_sudoku = sudoku.AC3_solve()
    test_bt.print_sudoku(final_sudoku)
