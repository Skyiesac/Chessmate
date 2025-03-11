#!/usr/bin/python3
from django.test import TestCase
from ..ChessLogic.ChessBase import *

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

    def test_game(self):
        pass

    def test_pawn(self):
        pass

    def test_queen(self):
        pass
        
    def tearDown(self):
        pass
