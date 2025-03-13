#!/usr/bin/python3
from django.test import TestCase
from ..ChessLogic.ChessBase import ChessGame

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
        self.g = ChessGame()
        self.code_dict = {'T': self.assertTrue, 'F': self.assertFalse}
        self.cases = [
            ('Te2e4', 'Te7e5', 'Tg1f3', 'Tb8c6', 'Tf1b5', 'Fb7b5', 'Td7d5', 'Te4d5', 'Tc6b4', 'Tc7c5'),
        ]

    def test_ruy_lopez(self):
        ruy_lopez_str = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"
        roy_g = str(ChessGame(ruy_lopez_str))
        self.g.reset()
        moves1 = [ 'e2e4',
                   'e7e5',
                   'g1f3',
                   'b8c6',
                   'f1b5', ]
        for i in moves1:
            self.g.move(i)

        self.assertEqual(roy_g, str(self.g))

    def test_case_batch(self):
        for _case in self.cases:
            self.g.reset()
            for j in _case:
                self.code_dict[j[0]](self.g.move(j[1:]))

    def test_pawn(self):
        self.g.reset()
        self.assertTrue(self.g.move('e2e4'))
        self.assertTrue(self.g.move('e7e5'))

    def test_alpha_translate(self):
        self.g.reset()
        tr1 = 'abcdefgh'
        tr2 = '12345678'
        for i in range(0, 8):
            for j in range(0, 8):
                tuple = (i, j)
                alpha = tr1[j] + tr2[i]
                self.assertEqual(tuple, self.g.translate(alpha))
                self.assertEqual(alpha, self.g.translate(tuple))

    def test_intersect(self):
        self.g.reset()
        self.assertFalse(self.g.direct_attack(  (0, 0), (0, 5)  ))
        self.assertTrue( self.g.direct_attack(  (0, 1), (2, 2)  ))
        self.assertFalse(self.g.direct_attack(  (0, 0), (0, 1)  ))
        self.assertFalse(self.g.direct_attack(  (0, 0), (1, 0)  ))
        self.assertFalse(self.g.direct_attack(  (0, 2), (3, 4)  ))
        self.assertTrue( self.g.direct_attack(  (6, 4), (4, 4)  ))
        self.assertTrue( self.g.direct_attack(  (6, 4), (5, 4)  ))
        self.assertFalse(self.g.direct_attack(  (6, 4), (6, 4)  ))

    def test_queen(self):
        pass
        
    def tearDown(self):
        pass

