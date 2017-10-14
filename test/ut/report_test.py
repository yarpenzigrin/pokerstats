#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import unittest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir + '/../..')

from poker_stats.entity import *
from poker_stats.handparser import parse_files

class report_tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(report_tests, self).__init__(*args, **kwargs)
        self.player_name = 'TEST_PLAYER'

    def prepare_hand(self, collected, preflop, flop = [], turn = [], river = []):
        hand = Hand()
        player = Player()
        player.name = self.player_name
        player.collected = collected
        for h in preflop:
            h.player = player
        hand.preflop = preflop
        for h in flop:
            h.player = player
        hand.flop = flop
        hand.turn = turn
        hand.river = river
        hand.players[self.player_name] = player
        return hand

    def test_ShouldCalculateProfitForOpenRaiseNoAction(self):
        hand = self.prepare_hand(0.25, preflop = [
                Action(Action.Raise, 0.30),
                Action(Action.Uncalled, 0.20)
            ])
        self.assertAlmostEqual(0.15, hand.profit_for_player(self.player_name), 2)

    def test_ShouldCalculateProfitForOpenRaise3BetFromBB4Bet(self):
        hand = self.prepare_hand(2.25, preflop = [
                Action(Action.Raise, 0.30),
                Action(Action.Raise, 2.70),
                Action(Action.Uncalled, 1.60)
            ])
        self.assertAlmostEqual(1.15, hand.profit_for_player(self.player_name), 2)

    def test_ShouldCalculateProfitForOpenRaiseCallFromBBBetFlopUncalled(self):
        hand = self.prepare_hand(0.65, preflop = [
                Action(Action.Raise, 0.30)
            ], flop = [
                Action(Action.Bet, 0.35),
                Action(Action.Uncalled, 0.35)
            ])
        self.assertAlmostEqual(0.35, hand.profit_for_player(self.player_name), 2)

    def test_ShouldCalculateProfitForParsedHandOpenRaiseBetBetBetUncalled(self):
        hands = parse_files([test_dir + '/data/openraise_bet_bet_bet_uncalled.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_BTN'), 2)
        self.assertAlmostEqual(-1.60, hand.profit_for_player('PLAYER_SB'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('PLAYER_BB'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_UTG'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_MP'), 2)
        self.assertAlmostEqual(1.70 - hand.rake, hand.profit_for_player('PLAYER_CO'), 2)

    def test_ShouldCalculateProfitForParsedHandFoldPre(self):
        hands = parse_files([test_dir + '/data/fold_pre.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_BTN'), 2)
        self.assertAlmostEqual(-0.05, hand.profit_for_player('PLAYER_SB'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('PLAYER_BB'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_UTG'), 2)
        self.assertAlmostEqual(0.15 - hand.rake, hand.profit_for_player('PLAYER_MP'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_CO'), 2)

    def test_ShouldCalculateProfitForParsedHandBlinidVsBlindTimeout(self):
        hands = parse_files([test_dir + '/data/openraise_timeout_uncalled.hand'])
        self.assertEqual(1, len(hands))
        hand = hands[0]

        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_BTN'), 2)
        self.assertAlmostEqual(-0.20, hand.profit_for_player('PLAYER_SB'), 2)
        self.assertAlmostEqual(0.20 - hand.rake, hand.profit_for_player('PLAYER_BB'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_UTG'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_MP'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('PLAYER_CO'), 2)

    def test_ShouldCalculateProfitsForBiggestSampleHandsOnTheButton(self):
        hands = parse_files([test_dir + '/data/sorted_btn.hand'])

        hand = hands[0]
        self.assertAlmostEqual(11.74 - hand.rake, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.05, hand.profit_for_player('longbreath'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('dima kk club'), 2)
        self.assertAlmostEqual(-0.35, hand.profit_for_player('Forstning'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('Skeleton1007'), 2)
        self.assertAlmostEqual(-11.24, hand.profit_for_player('Retro66'), 2)

        hand = hands[1]
        self.assertAlmostEqual(-9.75, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.05, hand.profit_for_player('cotyara1986'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('Snegul'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('KnME'), 2)
        self.assertAlmostEqual(-0.20, hand.profit_for_player('kasztanek136'), 2)
        self.assertAlmostEqual(10.10 - hand.rake, hand.profit_for_player('littlekhans'), 2)

        hand = hands[2]
        self.assertAlmostEqual(7.54 - hand.rake, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.05, hand.profit_for_player('MrDaxooo'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('Adrian197879'), 2)
        self.assertAlmostEqual(-0.30, hand.profit_for_player('takezo0229'), 2)
        self.assertAlmostEqual(-7.09, hand.profit_for_player('Takich7'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('ckostt'), 2)

        hand = hands[3]
        self.assertAlmostEqual(6.79 - hand.rake, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.05, hand.profit_for_player('kosta455'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('aruranka'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('pody606'), 2)
        self.assertAlmostEqual(-6.64, hand.profit_for_player('afrika14'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('bratykow'), 2)

        hand = hands[4]
        self.assertAlmostEqual(6.26 - hand.rake, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.05, hand.profit_for_player('MOSUTANA'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('0Darkman0'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('_-BATRIM-_'), 2)
        self.assertAlmostEqual(-6.11, hand.profit_for_player('piirakka87'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('straicar'), 2)

    def test_ShouldCalculateProfitsForBiggestSampleHandsOnTheSmallBlind(self):
        hands = parse_files([test_dir + '/data/sorted_sb.hand'])

        hand = hands[0]
        self.assertAlmostEqual(10.62 - hand.rake, hand.profit_for_player('pobedito'), 2)
        self.assertAlmostEqual(-10.52, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('8_PILOT_8'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('MaikStasiv'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('VDK_Ukr'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('GerDaTobe'), 2)

        hand = hands[1]
        self.assertAlmostEqual(0, hand.profit_for_player('Driver1966ss'), 2)
        self.assertAlmostEqual(5.28 - hand.rake, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('cupko0'), 2)
        self.assertAlmostEqual(-4.98, hand.profit_for_player('davejb68'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('huang hans01'), 2)
        self.assertAlmostEqual(-0.20, hand.profit_for_player('pool_king111'), 2)

        hand = hands[2]
        self.assertAlmostEqual(3.60 - hand.rake, hand.profit_for_player('vlad oleynik'), 2)
        self.assertAlmostEqual(-3.50, hand.profit_for_player('HubertusB'), 2)
        self.assertAlmostEqual(-0.10, hand.profit_for_player('starkmage'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('KnME'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('-Z3RO_DAY-'), 2)
        self.assertAlmostEqual(0, hand.profit_for_player('Gostina'), 2)

if __name__ == "__main__":
    unittest.main()
