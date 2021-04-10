from math import sqrt
class SudokuPuzzle:
    """
    A class to represent a single sudoku puzzle.

    Attributes
    ----------
    board : list[list]
        contains the sudoku puzzle as a list of rows
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
        ***This should be preceded by an invalid state check***

        Returns
        -------
        True : if solved
        False: Otherwise
        """

        "If any row does not match the list of symbols used in the puzzle, it is not solved"
        for row in self.board:
            row.sort()
            if row != self.symbols:
                return False

        return True

    def print_sudoku(self):
        """
        Prints the sudoku puzzle
        """
        for row in self.board:
            print("|", end=" ")
            for i in range(self.size):
                print(row[i], "|", end=" ")
            print("\n")







