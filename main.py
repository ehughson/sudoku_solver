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

def solve_size9_file(filename='easy.txt'):
        input = []
        with open(filename, 'rt') as myfile:
            for myline in myfile:
                input.append(myline.rstrip('\n'))
        i = 0
        board = []
        for line in input:
            if line[0:1] == 'P':
                i = 0
                board = []
            if 0 < i <= 9:
                row = ['', '', '', '', '', '', '', '', '']
                line_lst = list(line)
                j = 0
                for k in range(17):
                    if k % 2 == 0:
                        if line_lst[k] != '0':
                            row[j] = str(line_lst[k])
                        else:
                            row[j] = ''
                        j += 1
                board.append(row)
            if i == 9:
                return board
            i += 1


if __name__ == '__main__':
        base = 3
        #board = board_random(base)
        board = solve_size9_file()

        print(board)
        print("\n################## NOW DOING STOCHASTIC ##################\n")
        t = time.time()
        puzzle = SudokuPuzzle(board)
        stochastic_solver = Stochastic(puzzle, 0.7)
        start = time.process_time()
        result = stochastic_solver.solver()

        print("the time it took to complete Stochastic:", str(time.time() - t))
        puzzle.print_sudoku()
        
        print("\n################## NOW DOING HILLCLIMBING ##################\n")
        board = solve_size9_file()
        t = time.time()

        print(board)
        puzzle = SudokuPuzzle(board)
        hillclimb_solver = HillClimbing(puzzle, 50)
        start = time.process_time()
        result = hillclimb_solver.solve()
        print(result)

        print("the time it took to complete HillClimbing:", str(time.time() - t))
        puzzle.print_sudoku(result)
        

        print("\n################## NOW DOING AC3 ##################\n")
        board = solve_size9_file()
        t = time.time()
        test_csp = SudokuPuzzle(board, True)
        sudoku = AC3(test_csp, base)
        result = sudoku.AC3_solve()
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
        board = solve_size9_file()
        t = time.time() 
        test_bt = SudokuPuzzle(board, True)
        print(test_bt.board)
        back_track = backtrack(test_bt.board, base)
        backtrack_output = back_track.solveSudoku()

        print("the time it took to complete Backtrack:", str(time.time() - t))
        test_bt.print_sudoku(backtrack_output)


        
        

        
        