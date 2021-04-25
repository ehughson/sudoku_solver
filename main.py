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

stoch_cnt = 0
hill_cnt = 0
ac3_cnt = 0
stoch_time = 0
hill_time = 0
ac3_time = 0
back_time = 0


def reset_counts():
    global stoch_cnt, hill_cnt, ac3_cnt, stoch_time, hill_time, ac3_time, back_time
    stoch_cnt = 0
    hill_cnt = 0
    ac3_cnt = 0
    stoch_time = 0
    hill_time = 0
    ac3_time = 0
    back_time = 0

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
                solve_for_board(board)
                print("---------------------------------------------")
            i += 1

def solve_for_board(board):
    global stoch_cnt, hill_cnt, ac3_cnt, stoch_time, hill_time, ac3_time, back_time
    #print(board)
    print("Stochastic       ",end='')
    t = time.time()
    puzzle = SudokuPuzzle(board)
    stochastic_solver = Stochastic(puzzle, 0.7)
    start = time.time()
    result = stochastic_solver.solver()
    time_taken = time.time() - start
    if result:
        stoch_cnt += 1
        print("Solved   ",end='')
    else:
        print("Failed   ",end='')
    print(str(time_taken))
    stoch_time += float(time_taken)
    # puzzle.print_sudoku()

    print("HillClimbing     ", end='')
    #print(board)
    puzzle = SudokuPuzzle(board)
    hillclimb_solver = HillClimbing(puzzle, 2000)
    start = time.time()
    result = hillclimb_solver.solve()
    time_taken = time.time() - start
    if result:
        hill_cnt += 1
        print("Solved   ", end='')
    else:
        print("Failed   ", end='')
    print(str(time_taken))
    hill_time += float(time_taken)
    #puzzle.print_sudoku(result)


    # board = board_random(base)
    # board = solve_size9_file()
    t = time.time()
    test_csp = SudokuPuzzle(board, True)
    sudoku = AC3(test_csp, base)
    result = sudoku.AC3_solve()
    time_taken = time.time() - t

    flag = False
    new_grid = list(test_csp.values.values())

    if any(len(val) > 1 for val in new_grid):
        flag = True

    if flag == True:
        new_board = np.array(new_grid).reshape(len(test_csp.board), len(test_csp.board))
        # new_board_s = SudokuPuzzle(new_board)
        t = time.time()
        back_track_brd = backtrack(new_board, base)
        back_track_brd_out = back_track_brd.solveBacktrack(0, 0)
        time_taken2 = time.time() - t

        print("AC3 + Backtrack  ",end='')
        print("Solved   ",end='')
        print(str(time_taken2))
        ac3_time += float(time_taken2)

    else:
        ac3_cnt += 1
        print("AC3              ",end='')
        print("Solved   ",end='')
        print(str(time_taken))
        ac3_time += float(time_taken)


    t = time.time()
    test_bt = SudokuPuzzle(board, True)
    back_track = backtrack(test_bt.board, base)
    back_track_brd_out = back_track.solveBacktrack(0, 0)
    time_taken = time.time() - t
    print("Backtrack        ",end='')
    print("Solved   ",end='')
    print(str(time_taken))
    back_time += float(time_taken)

def solved_stat(total):
    print("***************************************")
    print("Number of puzzles solved out of ",total)
    print("***************************************")
    print("Stochastic   : ", stoch_cnt)
    print("HillClimbing : ", hill_cnt)
    print("AC3          : ", ac3_cnt)
    print("***************************************")
    print("       Average Run Time                ")
    print("***************************************")
    print("Stochastic   : ", stoch_time/total)
    print("HillClimbing : ", hill_time/total)
    print("AC3          : ", ac3_time/total)
    print("Backtracking : ", back_time/total)
    print('#########################################')
if __name__ == '__main__':
        base = 3
        print("Random Puzzles with 57 empty cells")
        print("**************************")
        for i in range(5):
            board = board_random(base, 56)
            solve_for_board(board)
            print("---------------------------------------------")

        solved_stat(5)
        reset_counts()
        print("Random Puzzles with 46 empty cells")
        print("**************************")
        for i in range(5):
            board = board_random(base, 46)
            solve_for_board(board)
            print("---------------------------------------------")
        solved_stat(5)
        reset_counts()

        print("Random Puzzles with 27 empty cells")
        print("**************************")
        for i in range(5):
            board = board_random(base, 27)
            solve_for_board(board)
            print("---------------------------------------------")
        solved_stat(5)
        reset_counts()

        print("Easy puzzles")
        solve_size9_file('easy.txt')
        solved_stat(50)
        reset_counts()

        print("Hard puzzles")
        solve_size9_file('hard.txt')
        solved_stat(95)
        reset_counts()

        print("End")

        
        

        
        