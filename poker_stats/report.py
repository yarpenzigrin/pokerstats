#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from poker_stats.entity import is_call_preflop, is_raise_preflop, is_3bet_preflop, profit_for_player
from poker_stats.handfilter import apply_filter, create_position_filter, create_voluntary_filter

class BlindReport(object):
    def __init__(self):
        self.sb_hand_count = 0
        self.sb_expected_profit = 0
        self.sb_vpip = 0
        self.sb_vpip_profit = 0
        self.sb_pfr = 0
        self.sb_pfr_profit = 0
        self.sb_flat = 0
        self.sb_flat_profit = 0
        self.sb_3bet = 0
        self.sb_3bet_profit = 0

        self.bb_hand_count = 0
        self.bb_expected_profit = 0
        self.bb_vpip = 0
        self.bb_vpip_profit = 0
        self.bb_pfr = 0
        self.bb_pfr_profit = 0
        self.bb_flat = 0
        self.bb_flat_profit = 0
        self.bb_3bet = 0
        self.bb_3bet_profit = 0

def create_blind_report(hands, player_name):
    report = BlindReport()

    sb_hands = apply_filter(hands, create_position_filter(player_name, ['SB']))
    sb_voluntary_hands = apply_filter(sb_hands, create_voluntary_filter(player_name, 'only'))
    sb_pfr_hands = apply_filter(sb_voluntary_hands, lambda h: is_raise_preflop(h, player_name))
    sb_flat_hands = apply_filter(sb_voluntary_hands, lambda h: is_call_preflop(h, player_name))
    sb_3bet_hands = apply_filter(sb_voluntary_hands, lambda h: is_3bet_preflop(h, player_name))

    report.sb_hand_count = len(sb_hands)
    report.sb_vpip = round(float(len(sb_voluntary_hands)) / len(sb_hands), 2)
    report.sb_vpip_profit = profit_for_player(sb_voluntary_hands, player_name)
    report.sb_expected_profit = -sum([h.game.stakes[0] for h in sb_hands])
    report.sb_pfr = round(float(len(sb_pfr_hands)) / len(sb_hands), 2)
    report.sb_pfr_profit = profit_for_player(sb_pfr_hands, player_name)
    report.sb_flat = round(float(len(sb_flat_hands)) / len(sb_hands), 2)
    report.sb_flat_profit = profit_for_player(sb_flat_hands, player_name)
    report.sb_3bet = round(float(len(sb_3bet_hands)) / len(sb_hands), 2)
    report.sb_3bet_profit = profit_for_player(sb_3bet_hands, player_name)

    bb_hands = apply_filter(hands, create_position_filter(player_name, ['BB']))
    bb_voluntary_hands = apply_filter(bb_hands, create_voluntary_filter(player_name, 'only'))
    bb_pfr_hands = apply_filter(bb_voluntary_hands, lambda h: is_raise_preflop(h, player_name))
    bb_flat_hands = apply_filter(bb_voluntary_hands, lambda h: is_call_preflop(h, player_name))
    bb_3bet_hands = apply_filter(bb_voluntary_hands, lambda h: is_3bet_preflop(h, player_name))

    report.bb_hand_count = len(bb_hands)
    report.bb_vpip = round(float(len(bb_voluntary_hands)) / len(bb_hands), 2)
    report.bb_vpip_profit = profit_for_player(bb_voluntary_hands, player_name)
    report.bb_expected_profit = -sum([h.game.stakes[1] for h in bb_hands])
    report.bb_pfr = round(float(len(bb_pfr_hands)) / len(bb_hands), 2)
    report.bb_pfr_profit = profit_for_player(bb_pfr_hands, player_name)
    report.bb_flat = round(float(len(bb_flat_hands)) / len(bb_hands), 2)
    report.bb_flat_profit = profit_for_player(bb_flat_hands, player_name)
    report.bb_3bet = round(float(len(bb_3bet_hands)) / len(bb_hands), 2)
    report.bb_3bet_profit = profit_for_player(bb_3bet_hands, player_name)

    return report
