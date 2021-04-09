class SudokuPuzzle:
    """
    A class to represent a single sudoku puzzle.

    Attributes
    ----------
    board : list[list]
        contains the sudoku puzzle as a list of rows
    size  : int
        size of the puzzle.(for n*n puzzle, size = n)
    variables : list[int]
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
        self.variables = ["1","2","3","4"]
        """
        self.board = board
        self.variables = [range(1,len(board)+1)] #need to convert each number to string
        self.size = len(board)

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
        "checking for duplicates in each column"
        #To be added
        col_duplicates = True
        "checking for duplicates in each subgrid"
        #To be added
        sub_duplicates = True

        if row_duplicates | col_duplicates | sub_duplicates:
            return True
        return False





