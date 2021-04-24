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
        #print(test_csp.board)
        sudoku = AC3(test_csp, base)
        #print(sudoku.grid.values)
        sudoku.AC3_solve()
        time_taken = time.time()-t
        
        flag = False
        new_grid = list(test_csp.values.values())

        if any(len(val) > 1 for val in new_grid):
                flag = True
        
        if flag == True:

                new_board = np.array(new_grid).reshape(len(test_csp.board), len(test_csp.board))
                #new_board_s = SudokuPuzzle(new_board)
                t = time.time()
                back_track_brd = backtrack(new_board, base)
                back_track_brd_out = back_track_brd.solveSudoku()
                time_taken2 = time.time() - t
                
                print("the time it took to complete AC3 using backtrack:", str(time_taken + time_taken2))
                test_csp.print_sudoku(back_track_brd_out)
                
                
        else:

                print("the time it took to complete AC3:", str(time_taken))
                new_board = np.array(new_grid).reshape(len(test_csp.board), len(test_csp.board))
                new_board = ( [list( map(int,i) ) for i in new_board] )
                test_csp.print_sudoku(new_board)
       

        
        print("\n################## NOW DOING BACKTRACK ##################\n")
        t = time.time() 
        test_bt = SudokuPuzzle(board)
        print(test_bt.board)
        back_track = backtrack(test_bt.board, base)
        backtrack_output = back_track.solveSudoku()

        print("the time it took to complete Backtrack:", str(time.time() - t))
        test_bt.print_sudoku(backtrack_output)


        
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

        