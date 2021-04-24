import time
import SudokuPuzzle, backtrack, hillclimbing, stochastic, csp

class SudokuSolver:

   def solve_backtrack(puzzle: SudokuPuzzle,base:int):
    backtrack_solver = backtrack(puzzle,base)
    start = time.clock()
    backtrack_solver.found
    time_taken = time.clock() - start


