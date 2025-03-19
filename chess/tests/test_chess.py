#!/usr/bin/python3
from django.test                import TestCase
from chess.ChessLogic.ChessBase import ChessGame
#from ..ChessLogic import ChessBase.ChessGame

#-------------------------#-
#    RUY LOPEZ            #-
#-------------------------#-
###########################-
####  0 1 2 3 4 5 6 7  ####-
##-----------------------##-
## 8  r - b q k b n r  7 ##-
## 7  - p p p - p p p  6 ##-
## 6  p - n - - - - -  5 ##-
## 5  - B - - p - - -  4 ##-
## 4  - - - - P - - -  3 ##-
## 3  - - - - - N - -  2 ##-
## 2  P P P P - P P P  1 ##-
## 1  R N B Q K - - R  0 ##-
##-----------------------##-
####  A B C D E F G H  ####-
###########################-


class ChessLogicTestCase(TestCase):
    def setUp(self):
        self.g = ChessGame()
        self.code_dict = {'T': self.assertTrue, 'F': self.assertFalse}
        self.cases = [
            ('Te2e4', 'Te7e5', 'Tg1f3', 'Tb8c6', 'Tf1b5', 'Fb7b5',
             'Td7d5', 'Te4d5', 'Fc6b4', 'Fc7c5', 'Tc8d7', 'Ff7f5',
             'Td2d4', 'Fe5d3', 'Tc6b4', 'Fb2b4', 'Te1e2', 'Tc7c5',
             'Fd5c5', 'Td5c6'),
        ]

    def test_ruy_lopez(self):
        ruy_lopez_str = "r1bqkbnr/-ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"
        roy_g = str(ChessGame(ruy_lopez_str))
        self.g.reset()
        moves1 = [ 'e2e4',
                   'e7e5',
                   'g1f3',
                   'b8c6',
                   'f1b5',
                   'a7a6',
                  ]
        for i in moves1:
            self.g.move(i)

        self.assertEqual(roy_g, str(self.g))

    def test_case_batch(self):
        for _case in self.cases:
            self.g.reset()
            for j in _case:
                self.code_dict[j[0]](self.g.move(j[1:]))
        print(self.g)

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

    def test_ultra(self):
        self.g.reset()
        a = [((1, 4), (3, 4)),
             ((6, 4), (5, 4)),
             ((1, 5), (3, 5)),
             ((7, 3), (6, 4))]
        print("----------")
        print(self.g.translate(a[0][0]))
        print(self.g.translate(a[0][1]))
        print(self.g.translate('e2'))
        print(self.g.translate('e4'))
        for i in a:
            self.assertNotEqual(False, self.g.move(i[0], np=i[1]))
        print(self.g.str_board())

    def test_queen(self):
        pass
        
    def tearDown(self):
        pass

