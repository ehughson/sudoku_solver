import numpy as np 
from random import sample
base = 3

side = base * base

def pattern(r, c):
    return (base * (r%base)+r//base+c)%side

def shuffle(s):
    return sample(s, len(s))

rBase = range(base)
rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
cols = [g*base +c for g in shuffle(rBase) for c in shuffle(rBase)]

nums = shuffle(range(1, base*base+1))

board = [ [ nums[pattern(r, c )] for c in cols] for r in rows]
print("############### the following is the solution of the puzzle #################")
for line in board:
    print(line)


squares = side*side 
empties = squares *3//4 

for p in sample(range(squares), empties):
    board[p//side][p%side] = 0

print("############### the following is the puzzle with values removed #################")
numSize = len(str(side))
for line in board:
    print("["+"  ".join(f"{n or '.':{numSize}}" for n in line)+"]")


def expandLine(line):
    return line[0] + line[5:9].join([line[1:5]*(base-1)] *base) + line[9:13]

line0  = expandLine("╔═══╤═══╦═══╗")
line1  = expandLine("║ . │ . ║ . ║")
line2  = expandLine("╟───┼───╫───╢")
line3  = expandLine("╠═══╪═══╬═══╣")
line4  = expandLine("╚═══╧═══╩═══╝")

symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
nums   = [ [""]+[symbol[n] for n in row] for row in board ]
print(line0)
for r in range(1,side+1):
    print( "".join(n+s for n,s in zip(nums[r-1],line1.split("."))) )
    print([line2,line3,line4][(r%side==0)+(r%base==0)])