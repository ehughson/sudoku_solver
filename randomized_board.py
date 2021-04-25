from random import sample

def main():
    print("SUDOKU SOLVER PROJECT")
    """
    Empirical questions:
    1. Does there exist a class of instances of the puzzle on which one algorithm always 
    outperforms another algorithm? Is this true for all instances, or 
    is the other algorithm still sometimes a better choice?
    2. How does the performance of the algorithms vary according to the 
    input size and hardness of the puzzle ? 
    
    Puzzles of size 2*2, 3*3 are considered and the performance is evaluated. 
    3. Can the algorithms be classified as optimal or suboptimal ? 
    """

def board_random( base,empty_frac = 0):
    side = base * base
    Base = range(base)
    row = [i*base + r for i in shuffle(Base) for r in shuffle(Base)]
    col= [i*base + c for i in shuffle(Base) for c in shuffle(Base)]
    nums = shuffle(range(1, side+1))
    board = [[ str(nums[pattern(base,side, r, c )]) for c in col] for r in row]
    if empty_frac != 0:
        empties = empty_frac
    else:
        empties = (side*side) * 4//7
    #print(empties)
    for p in sample(range(side*side), empties):
            board[p//side][p%side] = ''

    return board
def pattern(base, side, r, c):
            return (base * (r%base)+r//base+c)%side
def shuffle(s):
            return sample(s, len(s))