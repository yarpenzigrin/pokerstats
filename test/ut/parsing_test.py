import os
import sys
import unittest
sys.path.append(os.path.abspath('../..'))

from poker_stats import parseHandsFromFile
from entity import *

class ParserTests(unittest.TestCase):

    def assertLine(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in xrange(len(expected)):
            self.assertEqual(expected[i].type, actual[i].type)
            self.assertEqual(expected[i].value, actual[i].value)

    def test_ShouldParseCorrectlyOpenRaiseBetBetBetUncalledHand(self):
        hands = parseHandsFromFile('data/openraise_bet_bet_bet_uncalled.hand', 'PLAYER_CO')
        self.assertEqual(1, len(hands))
        hand = hands[0]
        self.assertEqual('CO', hand.position)
        self.assertEqual(3.30, hand.pot)
        self.assertEqual(3.15, hand.collected)
        self.assertLine([Action(Action.Raise, 0.30)], hand.preflop)
        self.assertLine([Action(Action.Bet, 0.40)], hand.flop)
        self.assertLine([Action(Action.Bet, 0.90)], hand.turn)
        self.assertLine([Action(Action.Bet, 2.00), Action(Action.Uncalled, -2.00)], hand.river)

if __name__ == "__main__":
    unittest.main()
