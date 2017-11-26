#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from .entity import is_successful_steal_preflop, is_unsuccessful_steal_preflop, profit_for_player # pylint: disable=no-name-in-module
from .hand_filter import apply_filter, create_call_pf_filter, create_pfr_filter, create_3bet_filter
from .hand_filter import create_4bet_filter, create_position_filter, create_voluntary_filter

def div(num1, num2):
    return round(float(num1) / num2, 2)

class BlindReport(object): # pylint: disable=too-many-instance-attributes,too-few-public-methods
    def __init__(self):
        self.sb_expected_profit = 0
        self.sb_expected_vpip_profit = 0
        self.sb_vpip_profit = 0
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
        self.fourbet = 0
        self.fourbet_profit = 0

class PreflopReport(object): # pylint: disable=too-many-instance-attributes,too-few-public-methods
    def __init__(self):
        self.hand_count = None
        self.steal_success = None
        self.steal_fail = None
        self.steal_profit = None
        self.steal_profit_per_100 = None
        self.vpip = None
        self.pfr = None
        self.threebet = None
        self.threebet_profit = None
        self.fourbet = None
        self.fourbet_profit = None
        self.profit = None
        self.profit_per_100 = None

def create_blind_report(hands, player_name):
    report = BlindReport()

    sb_hands = apply_filter(hands, create_position_filter(player_name, ['SB']))
    sb_voluntary_hands = apply_filter(sb_hands, create_voluntary_filter(player_name, 'only'))
    sb_forced_hands = apply_filter(sb_hands, create_voluntary_filter(player_name, 'forced'))

    report.sb_report = create_position_report(hands, player_name, 'SB')
    report.sb_expected_profit = round(-sum([h.stakes[0] for h in sb_hands]), 2)
    report.sb_expected_vpip_profit = round(-sum([h.stakes[0] for h in sb_voluntary_hands]), 2)
    report.sb_vpip_profit = profit_for_player(sb_voluntary_hands, player_name)
    report.sb_forced_profit = profit_for_player(sb_forced_hands, player_name)

    bb_hands = apply_filter(hands, create_position_filter(player_name, ['BB']))
    bb_voluntary_hands = apply_filter(bb_hands, create_voluntary_filter(player_name, 'only'))
    bb_forced_hands = apply_filter(bb_hands, create_voluntary_filter(player_name, 'forced'))

    report.bb_report = create_position_report(hands, player_name, 'BB')
    report.bb_expected_profit = round(-sum([h.stakes[1] for h in bb_hands]), 2)
    report.bb_expected_vpip_profit = round(-sum([h.stakes[1] for h in bb_voluntary_hands]), 2)
    report.bb_vpip_profit = profit_for_player(bb_voluntary_hands, player_name)
    report.bb_expected_forced_profit = round(-sum([h.stakes[1] for h in bb_forced_hands]), 2)
    report.bb_forced_profit = profit_for_player(bb_forced_hands, player_name)

    return report

def create_position_report(hands, player_name, position):
    report = PositionReport()

    position_hands = apply_filter(hands, create_position_filter(player_name, [position]))
    position_hands_len = len(position_hands)
    voluntary_hands = apply_filter(position_hands, create_voluntary_filter(player_name, 'only'))
    pfr_hands = apply_filter(voluntary_hands, create_pfr_filter(player_name))
    flat_hands = apply_filter(voluntary_hands, create_call_pf_filter(player_name))
    threebet_hands = apply_filter(voluntary_hands, create_3bet_filter(player_name))
    fourbet_hands = apply_filter(voluntary_hands, create_4bet_filter(player_name))

    report.position = position
    report.hand_count = position_hands_len
    if report.hand_count == 0:
        return report

    report.profit = profit_for_player(position_hands, player_name)
    report.vpip = div(len(voluntary_hands) * 100, position_hands_len)
    report.pfr = div(len(pfr_hands) * 100, position_hands_len)
    report.pfr_profit = profit_for_player(pfr_hands, player_name)
    report.flat = div(len(flat_hands) * 100, position_hands_len)
    report.flat_profit = profit_for_player(flat_hands, player_name)
    report.threebet = div(len(threebet_hands) * 100, position_hands_len)
    report.threebet_profit = profit_for_player(threebet_hands, player_name)
    report.fourbet = div(len(fourbet_hands) * 100, position_hands_len)
    report.fourbet_profit = profit_for_player(fourbet_hands, player_name)

    return report

def create_preflop_report(hands, player_name):
    report = PreflopReport()

    hands_len = len(hands)
    voluntary_hands = apply_filter(hands, create_voluntary_filter(player_name, 'only'))
    voluntary_hands_len = len(voluntary_hands)
    pfr_hands = apply_filter(voluntary_hands, create_pfr_filter(player_name))
    stolen_pot_hands = apply_filter(voluntary_hands, lambda h: is_successful_steal_preflop(h.preflop, player_name))
    failed_steal_hands = apply_filter(voluntary_hands, lambda h: is_unsuccessful_steal_preflop(h.preflop, player_name))
    threebet_hands = apply_filter(voluntary_hands, create_3bet_filter(player_name))
    fourbet_hands = apply_filter(voluntary_hands, create_4bet_filter(player_name))

    report.hand_count = hands_len
    report.steal_success = div(len(stolen_pot_hands) * 100, voluntary_hands_len)
    report.steal_fail = div(len(failed_steal_hands) * 100, voluntary_hands_len)
    report.steal_profit = profit_for_player(stolen_pot_hands + failed_steal_hands, player_name)
    report.steal_profit_per_100 = div(report.steal_profit * 100, voluntary_hands_len)
    report.vpip = div(voluntary_hands_len * 100, hands_len)
    report.pfr = div(len(pfr_hands) * 100, hands_len)
    report.threebet = div(len(threebet_hands) * 100, hands_len)
    report.threebet_profit = profit_for_player(threebet_hands, player_name)
    report.fourbet = div(len(fourbet_hands) * 100, hands_len)
    report.fourbet_profit = profit_for_player(fourbet_hands, player_name)
    report.profit = profit_for_player(hands, player_name)
    report.profit_per_100 = div(report.profit * 100, hands_len)

    return report
