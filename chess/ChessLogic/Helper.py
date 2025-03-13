#!/usr/bin/python3

def ind(l, t):
    return l[t[0]][t[1]]

def seti(l, t, g):
    l[t[0]][t[1]] = g

def str_b(l):
    return "\n".join(["".join(x) for x in l])

def visp(pos, moves):
    board = [['_' for x in range(0, 8)] for y in range(0, 8)]
    seti(board, pos, 'x')
    #board[pos[0]][pos[1]] = 'x'
    for i in moves:
        seti(board, i, '+')
    return board

def pair_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def remove_out_of_range(l):
    return list(filter(lambda p: p[0] >= 0 and p[1] >= 0 and p[0] <= 7 and p[1] <= 7, l))

def lmake(pos, l):
    return [pair_add(pos, x) for x in l]

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
