import copy
import time
from SudokuPuzzle import SudokuPuzzle
from backtrack import backtrack
from hillclimbing import HillClimbing
from stochastic import Stochastic
import csp


class SudokuSolver:
    def __init__(self):
        self.time_taken = time.process_time()
        self.result = False

    def solve_size9_file(self,filename='easy.txt'):
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
                self.call_alg(board)
            i += 1

    def call_alg(self, board):

        puzzle = SudokuPuzzle(board)
        board_csp = copy.deepcopy(board)
        puzzle_csp = SudokuPuzzle(board_csp, True)
        self.solve_backtrack(puzzle, 3)
        print("Backtrack    ", end=" ")
        self.print_result()
        self.solve_hillclimb(puzzle)
        print("HillClimbing ", end=" ")
        self.print_result()
        self.solve_stochastic(puzzle)
        print("Stochastic   ", end=" ")
        self.print_result()
        self.solve_csp(puzzle_csp)
        print("CSP (AC3)    ", end=" ")
        self.print_result()

    def print_result(self):
        if self.result:
            print("Solved", end=" ")
        else:
            print("Failed", end=" ")
        print(self.time_taken)
        print("\n")


    def solve_backtrack(self, puzzle: SudokuPuzzle, base: int):
        backtrack_solver = backtrack(puzzle, base)
        start = time.process_time()
        #self.result = backtrack_solver.solveSudoku()
        self.result = True
        self.time_taken = time.process_time() - start

    def solve_hillclimb(self, puzzle: SudokuPuzzle):
        hillclimb_solver = HillClimbing(puzzle, 50)
        start = time.process_time()
        self.result = hillclimb_solver.solve()
        self.time_taken = time.process_time() - start

    def solve_stochastic(self, puzzle: SudokuPuzzle):
        stochastic_solver = Stochastic(puzzle,0.7)
        start = time.process_time()
        self.result = stochastic_solver.solver()
        self.time_taken = time.process_time() - start

    def solve_csp(self,puzzle: SudokuPuzzle):
        ac3_solver = csp.AC3(puzzle)
        start = time.process_time()
        self.result = ac3_solver.AC3_solve()
        self.time_taken = time.process_time() - start

solver = SudokuSolver()
solver.solve_size9_file("easy.txt")

