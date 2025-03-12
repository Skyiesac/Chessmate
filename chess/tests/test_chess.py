#!/usr/bin/python3
from django.test import TestCase
from ..ChessLogic.ChessBase import *

#########################
###  0 1 2 3 4 5 6 7  ###
#-----------------------#
# 8  R - B K Q B N R  7 #
# 7  P P P P - P P P  6 #
# 6  - - N - - - - -  5 #
# 5  - b - - P - - -  4 #
# 4  - - - - p - - -  3 #
# 3  - - - - - n - -  2 #
# 2  p p p p - p p p  1 #
# 1  r n b k q - - r  0 #
#-----------------------#
###  A B C D E F G H  ###
#########################

class ChessLogicTestCase(TestCase):
    def setUp(self):
        self.g = Game()

    def test_alpha_tuple_translate(self):
        self.g.reset()
        tr1 = 'abcdefgh'
        tr2 = '12345678'
        for i in range(0, 8):
            for j in range(0, 8):
                tuple = (i, j)
                alpha = tr1[j] + tr2[i]
                self.assertEqual(tuple, self.g.alpha_translate(alpha))
                self.assertEqual(alpha, self.g.tuple_translate(tuple))

    def test_intersect(self):
        self.g.reset()
        self.assertEqual(False , self.g.check_intersect(  (0, 0), (0, 5)  ))
        self.assertEqual(True  , self.g.check_intersect(  (0, 1), (2, 2)  ))
        self.assertEqual(False , self.g.check_intersect(  (0, 0), (0, 1)  ))
        self.assertEqual(False , self.g.check_intersect(  (0, 0), (1, 0)  ))
        self.assertEqual(False , self.g.check_intersect(  (0, 2), (3, 4)  ))
        self.assertEqual(True  , self.g.check_intersect(  (6, 4), (4, 4)  ))
        self.assertEqual(True  , self.g.check_intersect(  (6, 4), (5, 4)  ))
        self.assertEqual(False , self.g.check_intersect(  (6, 4), (6, 4)  ))

    def test_pawn(self):
        self.g.reset()
        self.assertEqual(True , self.g.move_piece('e2', 'e4', alpha=True))

    def test_queen(self):
        pass
        
    def tearDown(self):
        pass

    def test_game(self):
        pass

