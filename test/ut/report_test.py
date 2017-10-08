#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import unittest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir + '/../..')

from poker_stats.entity import *
from poker_stats.report import get_profit_for_player
from poker_stats.handparser import parse_files

class report_tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(report_tests, self).__init__(*args, **kwargs)
        self.player_name = 'TEST_PLAYER'

    def prepare_hand(self, collected, preflop, flop = [], turn = [], river = []):
        hand = Hand()
        player = Player()
        player.collected = collected
        player.preflop = preflop
        player.flop = flop
        player.turn = turn
        player.river = river
        hand.players[self.player_name] = player
        return hand

    def test_ShouldCalculateProfitForOpenRaiseNoAction(self):
        hand = self.prepare_hand(0.25, preflop = [
                Action(Action.Raise, 0.30),
                Action(Action.Uncalled, 0.20)
            ])
        self.assertAlmostEqual(0.15, get_profit_for_player(hand, self.player_name), 2)

    def test_ShouldCalculateProfitForOpenRaise3BetFromBB4Bet(self):
        hand = self.prepare_hand(2.25, preflop = [
                Action(Action.Raise, 0.30),
                Action(Action.Raise, 2.70),
                Action(Action.Uncalled, 1.60)
            ])
        self.assertAlmostEqual(1.15, get_profit_for_player(hand, self.player_name), 2)

    def test_ShouldCalculateProfitForOpenRaiseCallFromBBBetFlopUncalled(self):
        hand = self.prepare_hand(0.65, preflop = [
                Action(Action.Raise, 0.30)
            ], flop = [
                Action(Action.Bet, 0.35),
                Action(Action.Uncalled, 0.35)
            ])
        self.assertAlmostEqual(0.35, get_profit_for_player(hand, self.player_name), 2)

    def test_ShouldCalculateProfitForParsedHandOpenRaiseBetBetBetUncalled(self):
        hands = parse_files([test_dir + '/data/openraise_bet_bet_bet_uncalled.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_BTN'), 2)
        self.assertAlmostEqual(-1.60, get_profit_for_player(hand, 'PLAYER_SB'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'PLAYER_BB'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_UTG'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_MP'), 2)
        self.assertAlmostEqual(1.70 - hand.rake, get_profit_for_player(hand, 'PLAYER_CO'), 2)

    def test_ShouldCalculateProfitForParsedHandFoldPre(self):
        hands = parse_files([test_dir + '/data/fold_pre.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_BTN'), 2)
        self.assertAlmostEqual(-0.05, get_profit_for_player(hand, 'PLAYER_SB'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'PLAYER_BB'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_UTG'), 2)
        self.assertAlmostEqual(0.15 - hand.rake, get_profit_for_player(hand, 'PLAYER_MP'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_CO'), 2)

    def test_ShouldCalculateProfitForParsedHandBlinidVsBlindTimeout(self):
        hands = parse_files([test_dir + '/data/openraise_timeout_uncalled.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_BTN'), 2)
        self.assertAlmostEqual(-0.20, get_profit_for_player(hand, 'PLAYER_SB'), 2)
        self.assertAlmostEqual(0.20 - hand.rake, get_profit_for_player(hand, 'PLAYER_BB'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_UTG'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_MP'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'PLAYER_CO'), 2)

    def test_ShouldCalculateProfitsForBiggestSampleHandsOnTheButton(self):
        hands = parse_files([test_dir + '/data/sorted_btn.hand'])

        hand = hands[0]
        self.assertAlmostEqual(11.74 - hand.rake, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.05, get_profit_for_player(hand, 'longbreath'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'dima kk club'), 2)
        self.assertAlmostEqual(-0.35, get_profit_for_player(hand, 'Forstning'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'Skeleton1007'), 2)
        self.assertAlmostEqual(-11.24, get_profit_for_player(hand, 'Retro66'), 2)

        hand = hands[1]
        self.assertAlmostEqual(-9.75, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.05, get_profit_for_player(hand, 'cotyara1986'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'Snegul'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'KnME'), 2)
        self.assertAlmostEqual(-0.20, get_profit_for_player(hand, 'kasztanek136'), 2)
        self.assertAlmostEqual(10.10 - hand.rake, get_profit_for_player(hand, 'littlekhans'), 2)

        hand = hands[2]
        self.assertAlmostEqual(7.54 - hand.rake, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.05, get_profit_for_player(hand, 'MrDaxooo'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'Adrian197879'), 2)
        self.assertAlmostEqual(-0.30, get_profit_for_player(hand, 'takezo0229'), 2)
        self.assertAlmostEqual(-7.09, get_profit_for_player(hand, 'Takich7'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'ckostt'), 2)

        hand = hands[3]
        self.assertAlmostEqual(6.79 - hand.rake, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.05, get_profit_for_player(hand, 'kosta455'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'aruranka'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'pody606'), 2)
        self.assertAlmostEqual(-6.64, get_profit_for_player(hand, 'afrika14'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'bratykow'), 2)

        hand = hands[4]
        self.assertAlmostEqual(6.26 - hand.rake, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.05, get_profit_for_player(hand, 'MOSUTANA'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, '0Darkman0'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, '_-BATRIM-_'), 2)
        self.assertAlmostEqual(-6.11, get_profit_for_player(hand, 'piirakka87'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'straicar'), 2)

    def test_ShouldCalculateProfitsForBiggestSampleHandsOnTheSmallBlind(self):
        hands = parse_files([test_dir + '/data/sorted_sb.hand'])

        hand = hands[0]
        self.assertAlmostEqual(10.62 - hand.rake, get_profit_for_player(hand, 'pobedito'), 2)
        self.assertAlmostEqual(-10.52, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, '8_PILOT_8'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'MaikStasiv'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'VDK_Ukr'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'GerDaTobe'), 2)

        hand = hands[1]
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'Driver1966ss'), 2)
        self.assertAlmostEqual(5.28 - hand.rake, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'cupko0'), 2)
        self.assertAlmostEqual(-4.98, get_profit_for_player(hand, 'davejb68'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'huang hans01'), 2)
        self.assertAlmostEqual(-0.20, get_profit_for_player(hand, 'pool_king111'), 2)

        hand = hands[2]
        self.assertAlmostEqual(3.60 - hand.rake, get_profit_for_player(hand, 'vlad oleynik'), 2)
        self.assertAlmostEqual(-3.50, get_profit_for_player(hand, 'HubertusB'), 2)
        self.assertAlmostEqual(-0.10, get_profit_for_player(hand, 'starkmage'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'KnME'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, '-Z3RO_DAY-'), 2)
        self.assertAlmostEqual(0, get_profit_for_player(hand, 'Gostina'), 2)

if __name__ == "__main__":
    unittest.main()
