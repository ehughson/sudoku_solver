import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue
from backtrack import backtrack

#constraint propogation with AC3

class AC3():
    """
    A class to represent a Sudoku solver using Constraint Satisfaction Problem
    Reference : https://sandipanweb.wordpress.com/2017/03/17/solving-sudoku-as-a-constraint-satisfaction-problem-using-constraint-propagation-with-arc-consistency-checking-and-then-backtracking-with-minimum-remaning-value-heuristic-and-forward-checking/
    https://medium.com/my-udacity-ai-nanodegree-notes/solving-sudoku-think-constraint-satisfaction-problem-75763f0742c9
    https://medium.com/swlh/how-to-solve-constraint-satisfaction-problems-csps-with-ac-3-algorithm-in-python-f7a9be538cfe
    About the algorithm
    <TO BE ADDED>
    Attributes
    ----------
    csp : object of the SudokuPuzzle class
    base: size of sudoku = n x n, where n is base
    Methods
    -------
    AC3_solve
        solver for the sudoku
    successor_function
        generates the successor of the current state
    heuristic function
        calculates the heuristic of the current state
    """

    def __init__(self, csp, base):
        """
        input is the Sudoku puzzle
        """
        self.grid = csp
        #print(self.grid.board)
        self.base = base

    def AC3_solve(self):
        """
        Solver for AC3 CSP
        """
        
        q = queue.Queue()
        #print("the size of the constraints are:", len(self.grid.constraints))
        for arc in self.grid.constraints:  # add all the arcs to a queue
            q.put(arc)
        while not q.empty():
            (x, y) = q.get()  # get the first arc (x,y) off the queue
            values = set(self.grid.values[x])
            for p in values:
                if not self.isconsistent(p, x, y):
                    self.grid.values[x] = "".join(c for c in self.grid.values[x] if c not in set(p))
                    #print(self.grid.values[x])
                    if len(self.grid.values[x]) == 0:
                        return False
                    for k in (self.grid.units[x]):
                        for v in k:
                            if v != x:
                                q.put((v, x))  # if the x domain has changed add all arcs of the form (k, x) to the queue

        #print(len(self.grid.board))
        return True
       
          

    def isconsistent(self, x, Xi, Xj):
        """
        Check inconsistency
        """
        for y in self.grid.values[Xj]:
            for peer in self.grid.units[Xi]:
                if Xj in peer and y != x:
                    return True
        return False
    

