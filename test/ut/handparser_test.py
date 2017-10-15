#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import unittest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir + '/../..')

from poker_stats.entity import *
from poker_stats.hand_parser import parse_files

class hand_parser_tests(unittest.TestCase):

    def assertLine(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in xrange(len(expected)):
            self.assertEqual(expected[i].type, actual[i].type)
            self.assertEqual(expected[i].value, actual[i].value)

    def assertPlayer(self, hand, name, position, starting_stack, preflop, flop, turn, river):
        self.assertEqual(position, hand.players[name].position)
        self.assertEqual(starting_stack, hand.players[name].starting_stack)
        self.assertLine(preflop, hand.preflop_actions(name))
        self.assertLine(flop, hand.flop_actions(name))
        self.assertLine(turn, hand.turn_actions(name))
        self.assertLine(river, hand.river_actions(name))

    def test_ShouldParseCorrectlyOpenRaiseBetBetBetUncalledHand(self):
        hands = parse_files([test_dir + '/data/openraise_bet_bet_bet_uncalled.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]
        self.assertEqual('PokerStars', hand.game.site)
        self.assertEqual('Hold\'em No Limit', hand.game.type)
        self.assertEqual((0.05, 0.10), hand.game.stakes)
        self.assertEqual('Aludra', hand.game.table_name)
        self.assertEqual('6-max', hand.game.table_type)
        self.assertEqual('1', hand.id)
        self.assertEqual('2017/08/07 11:12:54 ET', hand.timestamp)
        self.assertEqual(6, len(hand.players))
        self.assertEqual('4c Kc Ts', hand.board.flop)
        self.assertEqual('3s', hand.board.turn)
        self.assertEqual('As', hand.board.river)
        self.assertEqual(3.30, hand.pot)
        self.assertEqual(0.15, hand.rake)

        preflop = [Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_BTN', 'BTN', 21.05, preflop, [], [], [])

        preflop = [Action(ActionType.Post, 0.05), Action(ActionType.Call, 0.25)]
        flop = [Action(ActionType.Check, 0), Action(ActionType.Call, 0.40)]
        turn = [Action(ActionType.Check, 0), Action(ActionType.Call, 0.90)]
        river = [Action(ActionType.Check, 0), Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_SB', 'SB', 10.39, preflop, flop, turn, river)

        preflop = [Action(ActionType.Post, 0.10), Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_BB', 'BB', 10, preflop, [], [], [])

        preflop = [Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_UTG', 'UTG', 10.90, preflop, [], [], [])
        self.assertPlayer(hand, 'PLAYER_MP', 'MP', 10, preflop, [], [], [])

        preflop = [Action(ActionType.Raise, 0.30)]
        flop = [Action(ActionType.Bet, 0.40)]
        turn = [Action(ActionType.Bet, 0.90)]
        river = [Action(ActionType.Bet, 2.00), Action(ActionType.Uncalled, 2.00)]
        self.assertEqual('Ah Ac', hand.players['PLAYER_CO'].holding)
        self.assertEqual(3.15, hand.players['PLAYER_CO'].collected)
        self.assertPlayer(hand, 'PLAYER_CO', 'CO', 10, preflop, flop, turn, river)

    def test_ShouldParseCorrectlyOpenRaiseAndAllFoldsPre(self):
        hands = parse_files([test_dir + '/data/fold_pre.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        preflopFolds = [Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_UTG', 'UTG', 8.12, preflopFolds, [], [], [])
        self.assertPlayer(hand, 'PLAYER_CO', 'CO', 26.65, preflopFolds, [], [], [])
        self.assertPlayer(hand, 'PLAYER_BTN', 'BTN', 15.75, preflopFolds, [], [], [])

        sbActions = [Action(ActionType.Post, 0.05), Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_SB', 'SB', 15.83, sbActions, [], [], [])

        bbActions = [Action(ActionType.Post, 0.10), Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_BB', 'BB', 9.85, bbActions, [], [], [])

        mpActions = [Action(ActionType.Raise, 0.30), Action(ActionType.Uncalled, 0.20)]
        self.assertPlayer(hand, 'PLAYER_MP', 'MP', 9.83, mpActions, [], [], [])

    def test_ShouldParseCorrectlyOpenRaiseTimeoutAndAllFoldsPre(self):
        hands = parse_files([test_dir + '/data/openraise_timeout_uncalled.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        preflopFolds = [Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_UTG', 'UTG', 9.57, preflopFolds, [], [], [])
        self.assertPlayer(hand, 'PLAYER_CO', 'CO', 10.79, preflopFolds, [], [], [])
        self.assertPlayer(hand, 'PLAYER_BTN', 'BTN', 10.00, preflopFolds, [], [], [])
        self.assertPlayer(hand, 'PLAYER_MP', 'MP', 9.12, preflopFolds, [], [], [])

        sbActions = [Action(ActionType.Post, 0.05), Action(ActionType.Raise, 0.20), Action(ActionType.Fold, 0)]
        self.assertPlayer(hand, 'PLAYER_SB', 'SB', 13.74, sbActions, [], [], [])

        bbActions = [Action(ActionType.Post, 0.10), Action(ActionType.Raise, 0.65), Action(ActionType.Uncalled, 0.45)]
        self.assertPlayer(hand, 'PLAYER_BB', 'BB', 14.22, bbActions, [], [], [])

if __name__ == "__main__":
    unittest.main()
