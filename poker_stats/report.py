#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from poker_stats.entity import is_call_preflop, is_raise_preflop, is_3bet_preflop, profit_for_player # pylint: disable=no-name-in-module
from poker_stats.hand_filter import apply_filter, create_position_filter, create_voluntary_filter

class BlindReport(object): # pylint: disable=too-many-instance-attributes,too-few-public-methods
    def __init__(self):
        self.sb_expected_profit = 0
        self.sb_expected_vpip_profit = 0
        self.sb_vpip_profit = 0
        self.sb_expected_forced_profit = 0
        self.sb_forced_profit = 0
        self.sb_report = None

        self.bb_expected_profit = 0
        self.bb_expected_vpip_profit = 0
        self.bb_vpip_profit = 0
        self.bb_expected_forced_profit = 0
        self.bb_forced_profit = 0
        self.bb_report = None

class PositionReport(object): # pylint: disable=too-many-instance-attributes,too-few-public-methods
    def __init__(self):
        self.position = None
        self.hand_count = 0
        self.profit = 0
        self.vpip = 0
        self.pfr = 0
        self.pfr_profit = 0
        self.flat = 0
        self.flat_profit = 0
        self.threebet = 0
        self.threebet_profit = 0

def create_blind_report(hands, player_name):
    report = BlindReport()

    sb_hands = apply_filter(hands, create_position_filter(player_name, ['SB']))
    sb_voluntary_hands = apply_filter(sb_hands, create_voluntary_filter(player_name, 'only'))
    sb_forced_hands = apply_filter(sb_hands, create_voluntary_filter(player_name, 'forced'))

    report.sb_report = create_position_report(hands, player_name, 'SB')
    report.sb_expected_profit = round(-sum([h.stakes[0] for h in sb_hands]), 2)
    report.sb_expected_vpip_profit = round(-sum([h.stakes[0] for h in sb_voluntary_hands]), 2)
    report.sb_vpip_profit = round(profit_for_player(sb_voluntary_hands, player_name), 2)
    report.sb_expected_forced_profit = round(-sum([h.stakes[0] for h in sb_forced_hands]), 2)
    report.sb_forced_profit = round(profit_for_player(sb_forced_hands, player_name), 2)

    bb_hands = apply_filter(hands, create_position_filter(player_name, ['BB']))
    bb_voluntary_hands = apply_filter(bb_hands, create_voluntary_filter(player_name, 'only'))
    bb_forced_hands = apply_filter(bb_hands, create_voluntary_filter(player_name, 'forced'))

    report.bb_report = create_position_report(hands, player_name, 'BB')
    report.bb_expected_profit = round(-sum([h.stakes[1] for h in bb_hands]), 2)
    report.bb_expected_vpip_profit = round(-sum([h.stakes[1] for h in bb_voluntary_hands]), 2)
    report.bb_vpip_profit = round(profit_for_player(bb_voluntary_hands, player_name), 2)
    report.bb_expected_forced_profit = round(-sum([h.stakes[1] for h in bb_forced_hands]), 2)
    report.bb_forced_profit = round(profit_for_player(bb_forced_hands, player_name), 2)

    return report

def create_position_report(hands, player_name, position):
    report = PositionReport()

    position_hands = apply_filter(hands, create_position_filter(player_name, [position]))
    voluntary_hands = apply_filter(position_hands, create_voluntary_filter(player_name, 'only'))
    pfr_hands = apply_filter(voluntary_hands, lambda h: is_raise_preflop(h.preflop, player_name))
    flat_hands = apply_filter(voluntary_hands, lambda h: is_call_preflop(h.preflop, player_name))
    threebet_hands = apply_filter(voluntary_hands, lambda h: is_3bet_preflop(h.preflop, player_name))

    report.position = position
    report.hand_count = len(position_hands)
    if report.hand_count == 0:
        return report

    report.profit = profit_for_player(position_hands, player_name)
    report.vpip = round(float(len(voluntary_hands) * 100) / report.hand_count, 2)
    report.pfr = round(float(len(pfr_hands) * 100) / report.hand_count, 2)
    report.pfr_profit = profit_for_player(pfr_hands, player_name)
    report.flat = round(float(len(flat_hands) * 100) / report.hand_count, 2)
    report.flat_profit = profit_for_player(flat_hands, player_name)
    report.threebet = round(float(len(threebet_hands) * 100) / report.hand_count, 2)
    report.threebet_profit = profit_for_player(threebet_hands, player_name)

    return report
