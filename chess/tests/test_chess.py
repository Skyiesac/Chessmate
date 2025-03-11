#!/usr/bin/python3
from django.test import TestCase
from ..ChessLogic.ChessBase import *

#########################
###  0 1 2 3 4 5 6 7  ###
#-----------------------#
# 0  r n b k q b n r  0 #
# 1  p p p p p p p p  1 #
# 2  - - - - - - - -  2 #
# 3  - - - - - - - -  3 #
# 4  - - - - - - - -  4 #
# 5  - - - - - - - -  5 #
# 6  P P P P P P P P  6 #
# 7  R N B K Q B N R  7 #
#-----------------------#
###  0 1 2 3 4 5 6 7  ###
#########################

class ChessLogicTestCase(TestCase):
    def setUp(self):
        self.g = Game()

    def test_alpha_tuple_translate(self):
        tr1 = 'abcdefgh'
        tr2 = '12345678'
        for i in range(0, 8):
            for j in range(0, 8):
                tuple = (i, j)
                alpha = tr1[j] + tr2[i]
                self.assertEqual(tuple, self.g.alpha_translate(alpha))
                self.assertEqual(alpha, self.g.tuple_translate(tuple))

    def test_intersect(self):
        self.assertEqual(True , self.g.illegal_intersect(  (0, 0), (0, 5)  ))
        self.assertEqual(False, self.g.illegal_intersect(  (0, 1), (2, 2)  ))
        self.assertEqual(False, self.g.illegal_intersect(  (0, 0), (0, 1)  ))
        self.assertEqual(False, self.g.illegal_intersect(  (0, 0), (1, 0)  ))
        self.assertEqual(True , self.g.illegal_intersect(  (0, 2), (3, 4)  ))

    def test_game(self):
        pass

    def test_pawn(self):
        pass

    def test_queen(self):
        pass
        
    def tearDown(self):
        pass
