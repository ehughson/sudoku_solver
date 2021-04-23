from math import sqrt

class SudokuPuzzle:
    """
    A class to represent a single sudoku puzzle.

    Attributes
    ----------
    board : list[list]
        contains the sudoku puzzle as a list of rows of characters. Blank is represented as ""
    size  : int
        size of the puzzle.(for n*n puzzle, size = n)
    symbols : list[int]
        list of symbols used in the puzzle
    
    Methods
    -------
    check_validity
        Checks if the puzzle is valid
    invalid_state
        Checks if the state of the puzzle is invalid
    """
    def __init__(self,board):
        """
        Example:
        For the below puzzle
        |1| | | |
        |3|2| |1|
        | | |2|4|
        | | |1| |

        self.board = [["1","","",""],["3","2","","1"],["","","2","4"],["","","1",""]]
        self.variables = [1,2,3,4]
        """
        self.board = board
        self.size = len(board)
        self.symbols = []
        for i in range(self.size):
            self.symbols.append(str(i+1))
        self.symbols.sort()
        self.cols = "1"
        self.rows = "A"
        self.unitlist = ""
        self.init_csp_values()

        self.squares = self.cross(self.rows, self.cols)
        self.domain = self.getDict(self.board)
        self.values = self.getDict(self.board)

        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
        self.constraints = {(variable, i) for variable in self.squares for peer in self.units[variable] for i in peer if i != variable}

    def init_csp_values(self):
        digit = "1"
        alph = "A"
        for i in range(self.size-1):
            digit = chr(ord(digit) + 1)
            self.cols = self.cols + digit
            alph = chr(ord(alph) + 1)
            self.rows = self.rows + alph
        cross1 = []
        cross2 = []
        cross3 = []
        for c in self.cols:
            cross1.append(self.cross(self.rows, c))
        for r in self.rows:
            cross2.append(self.cross(r, self.cols))
        s = int(sqrt(self.size))
        rs_list = []
        cs_list = []
        for r in range(s):
            st = int(s*r)
            en = int(st + s)
            rs_list.append(self.rows[st: en])
            cs_list.append(self.cols[st: en])
        for rs in rs_list:
            for cs in cs_list:
               cross3.append(self.cross(rs, cs))
        self.unitlist = cross1 + cross2 + cross3

    def cross(self, A, B):
        return [a + b for a in A for b in B]

    def getDict(self, grid =""):
        "Creates the dict for CSP"
        i = 0
        j = 0
        values = dict()

        "Converting grid elements into integers. Space is converted into 0"
        r = 0
        for row in grid:
            for c in range(len(row)):
                if row[c] == '':
                    row[c] = '0'
                else:
                    row[c] = int(row[c])
            grid[r] = row
            r+=1

        for cell in self.squares:
            if j <= self.size:
                if grid[j][i]!=0:
                    values[cell] = str(grid[j][i])
                else:
                    values[cell] = self.cols
                i = i +1
                if i == self.size:
                    i = 0
                    j = j + 1
        return values

    def check_validity(self):
        """
        Checks the validity of the input puzzle.
        The puzzle should be of size n * n. 
        
        Returns
        -------
        True : if the puzzle is valid
        False: if the puzzle is invalid
        """
        for row in self.board:
            if len(self.board) != len(row):
                return False
        return True

    def invalid_state(self):
        """
        Check if the current state of the puzzle is invalid.
        No row/column/subgrid should contain a duplicate element.

        Returns
        -------
        True : if the state is invalid
        False: if the state is valid
        """

        "checking for duplicates in each row"
        for row in self.board:
            row_duplicates = any(row.count(element) > 1 for element in row)
            if row_duplicates:
                break

        "checking for duplicates in each column"
        for i in range(self.size):
            col = []
            for row in self.board:
                col.append(row[i])
            col_duplicates = any(col.count(element) > 1 for element in col)
            if col_duplicates:
                break

        "checking for duplicates in each subgrid"
        s = int(sqrt(self.size))
        row_start = 0
        for i in range(s):
            col = 0
            for c in range(s):
                subgrid = []
                for j in range(s):
                    r = row_start
                    for k in range(s):
                        row = self.board[r]
                        subgrid.append(row[col])
                        r += 1
                    col += 1
                subg_duplicates = any(subgrid.count(element) > 1 for element in subgrid)
                if subg_duplicates:
                    break
            row_start += s
        if row_duplicates | col_duplicates | subg_duplicates:
            return True

        return False

    def solved(self):
        """
        Checks if the puzzle is solved

        Returns
        -------
        True : if solved
        False: Otherwise
        """

        "Not solved if the state is invalid"
        if self.invalid_state():
            return False

        "If any row does not match the list of symbols used in the puzzle, it is not solved"
        for row in self.board:
            row = sorted(row)
            if row != self.symbols:
                return False

        return True

    def print_sudoku(self,values=None):
        """
        Prints the sudoku puzzle
        """
        if values:
            print_board = values
        else:
            print_board = self.board
        s = int(sqrt(self.size))
        r = 1
        for row in print_board:
            c = 1
            print('\n')
            print("||", end=" ")
            for i in range(self.size):
                if c % s == 0:
                    print(row[i], "||", end=" ")
                else:
                    print(row[i], "|", end=" ")
                c+=1
            r+=1












