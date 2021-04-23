from random import sample

def board_random( base,empty_frac = 0):
   

    side = base * base

    def pattern(r, c):
            return (base * (r%base)+r//base+c)%side

    def shuffle(s):
            return sample(s, len(s))

    rBase = range(base)
    rows1 = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    colum = [g*base +c for g in shuffle(rBase) for c in shuffle(rBase)]

    nums = shuffle(range(1, base*base+1))

    board = [[ str(nums[pattern(r, c )]) for c in colum] for r in rows1]

    #squares = side*side 
    #print(3//4)
    if empty_frac != 0:
        empties = (side*side) * empty_frac
    else:
        empties = (side*side) * 3//6
    #empties = 37

    #print(empties)

    for p in sample(range(side*side), empties):
            board[p//side][p%side] = str(0)

    #print(board)
    return board