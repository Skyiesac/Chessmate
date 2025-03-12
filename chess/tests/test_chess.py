#!/usr/bin/python3
from django.test import TestCase
from ..ChessLogic.ChessBase import *

#-------------------------#-
#    RUY LOPEZ            #-
#-------------------------#-

###########################-
####  0 1 2 3 4 5 6 7  ####-
##-----------------------##-
## 8  r - b k q b n r  7 ##-
## 7  p p p p - p p p  6 ##-
## 6  - - n - - - - -  5 ##-
## 5  - B - - p - - -  4 ##-
## 4  - - - - P - - -  3 ##-
## 3  - - - - - N - -  2 ##-
## 2  P P P P - P P P  1 ##-
## 1  R N B K Q - - R  0 ##-
##-----------------------##-
####  A B C D E F G H  ####-
###########################-

class ChessLogicTestCase(TestCase):
    def setUp(self):
        self.g = Game()

    def test_ruy_lopez(self):
        ruy_lopez_str = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"
        roy_g = str(Game(ruy_lopez_str))
        self.g.reset()
        moves1 = [ ('e2', 'e4'),
                   ('e7', 'e5'),
                   ('g1', 'f3'),
                   ('b8', 'c6'),
                   ('f1', 'b5'), ]
        for i in moves1:
            self.g.move_piece(*i, alpha=True)

        self.assertEqual(roy_g, str(self.g))

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

