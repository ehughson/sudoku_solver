import random
from math import sqrt
from time import time
from SudokuPuzzle import SudokuPuzzle


class HillClimbing:
    """
    A class to represent a Sudoku solver using HillClimbing Algorithm using Random Restart
    Reference : https://www.cs.rochester.edu/u/brown/242/assts/termprojs/Sudoku09.pdf

    Steps implemented
    Let the start state be defined as the initially puzzle with all of the empty spaces filled in such that each
    row contains the numbers one to n^2. Using this as a start state, the successor function can be
    defined as swapping any two non fixed values in the same row.  The heuristic can simply be the sum
    of the number of conflicts that appear within each column and each box.  Since each row has exactly
    the numbers one to n^2 there are no conflicts within the rows.

    The general hill climbing algorithm described above is incomplete.  This is because it can
    get stuck in a local minimum.   One simple way to fix this is to randomly restart the algorithm
    whenever it goes a while without improving the heuristic value.  This is known as random restart
    hill climbing.

    Attributes
    ----------
    puzzle : object of the SudokuPuzzle class
    start_state : starting state of the puzzle
    current_state : current state of the puzzle
    symbol_set : set of all symbols used
    non_fixed_values : positions of non fixed values in each row
    max_runtime : maximum run time in seconds
    iterations : number of iterations in each climb
    
    Methods
    -------
    create_start_state
        generates the start state 
    successor_function
        generates the successor of the current state
    heuristic function
        calculates the heuristic of the current state
    """

    def __init__(self, puzzle, max_runtime, iterations):
        self.start_state = puzzle
        self.non_fixed_values = list()
        emp_list = []
        for row in self.start_state.board:
            self.non_fixed_values.append(emp_list)
        self.symbol_set = set(self.start_state.symbols)
        self.create_start_state()
        self.current_state = self.start_state
        self.max_runtime = max_runtime
        self.iterations = iterations

    def create_start_state(self):
        """creates the start state by filling each row of the puzzle with values 1 to n"""
        row_num = 0
        for row in self.start_state.board:
            row_symbol_set = set(row)
            avail_symbol_set = self.symbol_set.difference(row_symbol_set)
            sel_row = []
            col = 0
            for i in row:
                if i == "":
                    i = avail_symbol_set.pop()
                    row[col] = i
                    sel_row.append(col)
                col+=1
            self.non_fixed_values[row_num] = sel_row
            self.start_state.board[row_num] = row
            row_num += 1


    def sel_row(self, state: SudokuPuzzle):
        if state.size == 1:
            return 0

        choices = []

        for i in range(len(self.non_fixed_values)):
            row = self.non_fixed_values[i]
            if len(row) > 0:
                choices.append(i)

        return random.choice(choices)

    def successor_function(self, state: SudokuPuzzle):
        """
        creates a successor state by swapping any two non fixed values in the same row selected randomly
        """

        sel_row = self.sel_row(state)
        row = self.non_fixed_values[sel_row]
        len_fixed = len(row)
        if len_fixed > 1:
           fix1 = random.randint(0, len_fixed-1)
           fix2 = random.randint(0, len_fixed-1)
        else:
            fix1 = 0
            fix2 = 0
            fix2 = 0
        pos1 = row[fix1]
        pos2 = row[fix2]
        temp_row = state.board[sel_row]
        temp = temp_row[pos1]
        temp_row[pos1] = temp_row[pos2]
        temp_row[pos2] = temp
        state.board[sel_row] = temp_row
        return state

    def heuristic_function(self, state: SudokuPuzzle):
        """heuristic = number of conflicts that appear within each column and each box"""

        # adding conflicts in each column
        conflicts = 0
        for i in range(state.size):
            col = []
            for row in state.board:
                col.append(row[i])
            col_duplicates = any(col.count(element) > 1 for element in col)
            if col_duplicates:
                conflicts += 1

        # adding conflicts in each subgrid
        s = int(sqrt(state.size))
        row_start = 0
        for i in range(s):
            col = 0
            for c in range(s):
                subgrid = []
                for j in range(s):
                    r = row_start
                    for k in range(s):
                        row = state.board[r]
                        subgrid.append(row[col])
                        r += 1
                    col += 1
                subg_duplicates = any(subgrid.count(element) > 1 for element in subgrid)
                if subg_duplicates:
                    conflicts += 1
            row_start += s

        return conflicts

    def climb(self, state: SudokuPuzzle):
        """finding local maxima using heuristic function"""
        for i in range(self.iterations):
            next_state = self.successor_function(state)
            # random restart
            if i == self.iterations:
                return state
            # no conflicts in column/sub grid -> solved
            if self.heuristic_function(next_state) == 0:
                return next_state
            else:
                # improvement in heuristic function
                if self.heuristic_function(next_state) >= self.heuristic_function(state):
                    return self.climb(state)

    def solver(self):
        """solver using HillClimbing"""
        start_time = time()
        # continue until solution has been found or until max_runtime has not been reached
        while True:#or (time() - start_time < self.max_runtime):
            if self.current_state.solved():
                return self.current_state
            self.current_state = self.climb(self.current_state)
        return None

#board = [["1",""],["","1"]]
board = [["2","1","",""],["4","","1","2"],["1","","",""],["3","4","","1"]]
print("board",board)
puzzle = SudokuPuzzle(board)
max_runtime = time()
iterations = 5
solution = HillClimbing(puzzle, max_runtime,iterations)
solution.solver()
print("solution is ", solution.current_state.board)
