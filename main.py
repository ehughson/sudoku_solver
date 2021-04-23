import numpy as np 
from random import sample
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle
import queue
from csp import AC3
from backtrack import backtrack
from stochastic import Stochastic
from hillclimbing import HillClimbing
from randomized_board import board_random
import time

if __name__ == '__main__':
        base = 3
        board = board_random(base)

        print("\n################## NOW DOING AC3 ##################\n")
        t = time.time()
        test_csp = SudokuPuzzle(board)
        sudoku = AC3(test_csp)
        final_sudoku = sudoku.AC3_solve()

        print("the time it took to complete AC3:", str(time.time() - t))
        test_csp.print_sudoku(final_sudoku)


        print("\n################## NOW DOING BACKTRACK ##################\n")
        t = time.time() 
        test_bt = SudokuPuzzle(board)
        back_track = backtrack(board, base)
        backtrack_output = back_track.solveSudoku()

        print("the time it took to complete Backtrack:", str(time.time() - t))
        test_bt.print_sudoku()



        print("\n################## NOW DOING HILLCLIMBING ##################\n")
        t = time.time()
        puzzle = SudokuPuzzle(board)
        iterations = 600
        solution = HillClimbing(puzzle,iterations)

        print("the time it took to complete HillClimbing:", str(time.time() - t))
        puzzle.print_sudoku()

        print("\n################## NOW DOING STOCHASTIC ##################\n")
        t = time.time()
        puzzle1 = SudokuPuzzle(board)
        alpha1 = 0.99
        solution = Stochastic(puzzle1, alpha1)

        print("the time it took to complete Stochastic:", str(time.time() - t))
        puzzle1.print_sudoku()