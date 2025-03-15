#!/usr/bin/python3

def visp(pos, moves):
    board = [['_' for x in range(0, 8)] for y in range(0, 8)]
    board[pos[0]][pos[1]] = 'x'
    for i in moves:
        board[i[0]][i[1]] = '+'
    return board

def pair_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def sign(n):
    if   n < 0: return -1
    elif n > 0: return  1
    else:       return  0

def points_on_line(op, np, mint=1):
    a  = (np[0] - op[0], np[1] - op[1])
    x1 = sign(a[0]); x2 = sign(a[1])
    points = []
    for i in range(1, max(abs(a[0]), abs(a[1])) + mint):
        points.append(pair_add(op, (i*x1, i*x2)))
    return points

def average(*args):
    return sum(args) // len(args)

def midpoint(op, np):
    return (average(op[0], np[0]), average(op[1], np[1]))

