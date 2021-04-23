import copy
import random
from math import sqrt
import sys
from SudokuPuzzle import SudokuPuzzle


class HillClimbing:
    """
    A class to represent a Sudoku solver using HillClimbing Algorithm using Random Restart
    Reference : https://www.cs.rochester.edu/u/brown/242/assts/termprojs/Sudoku09.pdf

    About the algorithm
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
    initial_state : starting state of the puzzle
    current_state : current state of the puzzle
    symbol_set : set of all symbols used
    non_fixed_values : positions of non fixed values in each row
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

    def __init__(self, puzzle, iterations):

        sys.setrecursionlimit(3000)
        self.initial_state = puzzle
        self.current_state = copy.deepcopy(self.initial_state)
        self.non_fixed_values = list()
        emp_list = []
        for row in self.current_state.board:
            self.non_fixed_values.append(emp_list)
        self.symbol_set = set(self.current_state.symbols)
        self.choices = []
        self.create_start_state()
        self.iterations = iterations


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
        #print("******************************************************************")
        #print("Start state : ")
        #self.current_state.print_sudoku()
        #print("------------------------------------------------------------------")
        #print('heuristic of start state', self.heuristic_function(self.current_state))


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

    def climb(self, state: SudokuPuzzle,iteration: int):
        """finding local maxima using heuristic function"""

        next_state = self.successor_function(state)
        #print("------------------------------------------------------------------")
        #print("Next state : ")
        #state.print_sudoku()
        #print("------------------------------------------------------------------")
        #print('Heuristic of CURRENT state = ', self.heuristic_function(state))
        #print('Heuristic of NEXT state = ', self.heuristic_function(next_state))
        #print("******************************************************************")

        next_state.print_sudoku()
        if self.heuristic_function(next_state) == 0:
            #print('Solved ! : Heuristics has reached 0')
            return next_state
        else:
            # maximum iterations reached - need to restart
            if iteration == self.iterations:
                return self.initial_state
            iteration += 1
            # No improvement in heuristics -> do not go to next state but climb
            if self.heuristic_function(next_state) >= self.heuristic_function(state):
                #print('Climbing : using current state')
                return self.climb(state, iteration)
            # Else, go to next state and climb
            else:
                #print('Climbing : using next state')
                return self.climb(next_state, iteration)
        return state

    def solver(self):
        """solver using HillClimbing"""

        # continue until solution has been found
        i = 0
        while True:
            i+=1
            if self.current_state.solved():
                #print('Solved !')
                return self.current_state
            self.current_state = self.climb(self.current_state, 1)
            #in case of restart, create a new random start state
            if self.current_state.board == self.initial_state.board:
                self.create_start_state()
        #print('Total number of iterations = ', i)
        return None


