#This python script converts the format of the puzzle lists of the form list of lists of string.
#This is a one time run
def create_boards(filename, outfile):
    input = []
    with open(filename, 'rt') as myfile:
       for myline in myfile:
          input.append(myline.rstrip('\n'))
    nf = open(outfile, 'a+')
    i=0
    board = []
    for line in input:
        # print("line = ", line)
        if line[0:1] == 'P':
            i = 0
            board = []
        if 0 < i <= 9:
            row = ['', '', '', '', '', '', '', '', '']
            line_lst = list(line)
            j = 0
            for k in range(17):
                if k % 2 == 0:
                    if line_lst[k] != '0':
                        row[j] = line_lst[k]
                    j += 1
            board.append(row)
        if i == 9:
            nf.write(str(board))
            nf.write("\n")
        i += 1
    nf.close()


create_boards('easy.txt', 'easy_sudoku.txt')
create_boards('hard.txt', 'hard_sudoku.txt')