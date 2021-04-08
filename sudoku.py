import itertools
import sys

characters = 'ABCDEFGHI'
numbers = '123456789'


class Sudoku:

    def __init__(self, board):
        self.variables, self.domains, self.constraints, self.neighbors, self.pruned = list(), dict(), list(), dict(), dict()
        self.prepare(board)

    def prepare(self, board):

        game = list(board)
        print("here is the game board:", game)

        #a = characters
        #b = numbers
        self.variables =  [a + b for a in characters for b in numbers]
        #print(self.variables)
    
        #if its 0 then it gets all possible values if its already assigned a number then it gets stuck with that number
        self.domains = {v: list(range(1, 10)) if game[i] == 0 else [int(game[i])] for i, v in enumerate(self.variables)}

        #print(self.domains)

        #if assigned a value of 0, then it gets pruned and is given an empty list
        self.pruned = {v: list() if game[i] == 0 else [int(game[i])] for i, v in enumerate(self.variables)}
        

        #print(self.pruned)

        self.build_constraints() #builds all possible constraints???

        self.build_neighbors() #get the neighbourhood of each cell

    def build_constraints(self):

        blocks = (
            [[a + b for a in characters for b in number]for number in numbers] +
            [[a + b for a in character for b in numbers] for character in characters] +
            [[a + b for a in character for b in number] for character in ('ABC', 'DEF', 'GHI') for number in ('123', '456', '789')]
        )

        print(blocks)
        for block in blocks:
            combinations = self.permutate(block)
            for combination in combinations:
                if [combination[0], combination[1]] not in self.constraints:
                    self.constraints.append([combination[0], combination[1]])
        #print(self.constraints)

    def build_neighbors(self):

        for x in self.variables:
            self.neighbors[x] = list()
            for c in self.constraints:
                if x == c[0]:
                    self.neighbors[x].append(c[1])
        #print(self.neighbors)

    def solved(self):

        for v in self.variables:
            if len(self.domains[v]) > 1:
                return False

        return True

    def complete(self, assignment):

        for x in self.variables:
            if len(self.domains[x]) > 1 and x not in assignment:
                return False

        return True

    def consistent(self, assignment, var, value):

        consistent = True

        for key, val in assignment.iteritems():
            if val == value and key in self.neighbors[var]:
                consistent = False

        return consistent

    def assign(self, var, value, assignment):

        assignment[var] = value

        self.forward_check(var, value, assignment)

    def unassign(self, var, assignment):

        if var in assignment:

            for (D, v) in self.pruned[var]:
                self.domains[D].append(v)

            self.pruned[var] = []

            del assignment[var]

    def forward_check(self, var, value, assignment):

        for neighbor in self.neighbors[var]:
            if neighbor not in assignment:
                if value in self.domains[neighbor]:
                    self.domains[neighbor].remove(value)
                    self.pruned[var].append((neighbor, value))

    @staticmethod
    def constraint(xi, xj): 
        print(xi != xj)
        return xi != xj

    @staticmethod
    def permutate(iterable):
        result = list()

        for L in range(0, len(iterable) + 1):
            if L == 2:
                for subset in itertools.permutations(iterable, L):
                    result.append(subset)

        return result

    @staticmethod
    def conflicts(sudoku, var, val):

        count = 0

        for n in sudoku.neighbors[var]:
            if len(sudoku.domains[n]) > 1 and val in sudoku.domains[n]:
                count += 1

        return count

    def out(self, mode):

        if mode == 'console':

            for var in self.variables:
                sys.stdout.write(str(self.domains[var][0]))

        elif mode == 'file':
            return
