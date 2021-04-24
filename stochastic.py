import copy
import math
import random
from math import sqrt
from SudokuPuzzle import SudokuPuzzle


class Stochastic:
    """
    A class to represent a Sudoku solver using Simulated Annealing

    Steps implemented

    Starting with an initial candidate solution, an exploration of the search space is conducted by
    iteratively applying the above neighbourhood operator. Given a candidate solution s, a neighbour s' is
    then accepted if (a) s' is better than s (with respect to the cost function), or (b) with a probability:
    exp(-d/t)
    where d is the proposed change in the cost function and t is a control parameter, known as the
    temperature. Moves that meet neither of the above two conditions are reset.

    Attributes
    ----------
    puzzle : object of the SudokuPuzzle class
    start_state : starting state of the puzzle
    current_state : current state of the puzzle
    symbol_set : set of all symbols used
    non_fixed_values : positions of non fixed values in each row
    alpha : alpha value for controlling temperature t linearly

    Methods
    -------
    create_start_state
        generates the start state
    successor_function
        generates the successor of the current state
    heuristic function
        calculates the heuristic of the current state
    solver
        solves the puzzle using Simulated Annealing
    """

    def __init__(self, puzzle, alpha_val):
        self.initial_state = puzzle
        self.current_state = copy.deepcopy(self.initial_state)
        self.non_fixed_values = list()
        emp_list = []
        for row in self.current_state.board:
            self.non_fixed_values.append(emp_list)
        self.symbol_set = set(self.current_state.symbols)
        self.choices = []
        self.create_start_state()
        self.alpha = alpha_val

    def create_start_state(self):
        """creates the start state by filling each row of the puzzle with values 1 to n"""
        row_num = 0
        start_state = copy.deepcopy(self.initial_state)
        for row in start_state.board:
            row_symbol_set = set(row)
            avail_symbol_set = self.symbol_set.difference(row_symbol_set)
            sel_row = []
            col = 0
            for i in row:
                if i == "":
                    choice_list = list(avail_symbol_set)
                    filled = random.choices(choice_list)
                    avail_symbol_set.remove(filled[0])
                    row[col] = filled[0]
                    sel_row.append(col)
                col+=1
            self.non_fixed_values[row_num] = sel_row
            start_state.board[row_num] = row
            row_num += 1
        for i in range(len(self.non_fixed_values)):
            row = self.non_fixed_values[i]
            if len(row) > 1:
                self.choices.append(i)
        self.current_state = start_state


    def successor_function(self, curr_state: SudokuPuzzle):
        """
        creates a successor state by swapping any two non fixed values in the same row selected randomly
        """
        state = copy.deepcopy(curr_state)
        if state.size == 1:
            sel_row = 0
        else:
           rand_num = random.randint(0, len(self.choices)-1)
           sel_row = self.choices[rand_num]
        row = self.non_fixed_values[sel_row]
        len_fixed = len(row)
        if len_fixed > 1:
           fix1 = random.randint(0, len_fixed-1)
           fix2 = random.randint(0, len_fixed-1)
        else:
            fix1 = 0
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
            #Finding duplicates
            dup_col = dict()
            # Iterate over each element in list
            for elem in col:
                # If element exists in dict then increment its value else add it in dict
                if elem in dup_col:
                    dup_col[elem] += 1
                else:
                    dup_col[elem] = 1
            dup_col = {key: value for key, value in dup_col.items() if value > 1}
            for key, value in dup_col.items():
                if value > 1:
                   conflicts += (value -1)
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
                # Finding duplicates
                dup_sub= dict()
                # Iterate over each element in list
                for elem in subgrid:
                    # If element exists in dict then increment its value else add it in dict
                    if elem in dup_sub:
                        dup_sub[elem] += 1
                    else:
                        dup_sub[elem] = 1
                dup_sub = {key: value for key, value in dup_sub.items() if value > 1}
                for key, value in dup_sub.items():
                    if value > 1:
                        conflicts += (value-1)
            row_start += s

        return conflicts

    def jump(self, probability: float):
        return random.random() < probability

    def solver(self):
        """solver using Simulated Annealing"""
        # continue until solution has been found
        t = 1
        for i in range(10000):
            t = self.alpha * t
            if t == 0:
                return self.current_state
            if self.current_state.solved():
                return self.current_state
            next_state = self.successor_function(self.current_state)
            delta = self.heuristic_function(self.current_state) - self.heuristic_function(next_state)
            if delta > 0:
                self.current_state = copy.deepcopy(next_state)
            else:
                probability = math.exp(delta / t)
                if self.jump(probability):
                    self.current_state = copy.deepcopy(next_state)

        if self.current_state.solved():
            return True
        else:
            return False

#board = [["1",""],["","1"]]
#board = [["2","1","",""],["4","","1","2"],["1","","",""],["3","4","","1"]]


# board = [
#          ["","","","2","6","","7","","1"],
#          ["6","8","","","7","","","9",""],
#          ["1","9","","","","4","5","",""],
#          ["8","2","","1","","","","4",""],
#          ["","","4","6","","2","9","",""],
#          ["","5","","","","3","","2","8"],
#          ["","","9","3","","","","7","4"],
#          ["","4","","","5","","","3","6"],
#          ["7","","3","","1","8","","",""],
#         ]
#



