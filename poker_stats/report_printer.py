#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

def print_holding_report(report):
    print 'Holdings profitability'
    print
    print '<holding> <hands played> <profit>'
    for st in report.stats:
        print '{:3} {:6} {:>8.2f}'.format(st.holding, st.holding_count, st.profit)

def print_blind_report(report):
    print_position_report(report.sb_report)
    print "Expected loss if fold all hands: {}".format(report.sb_expected_profit)
    print "VPIP profit: {}".format(report.sb_vpip_profit)
    print "Expected loss if fold all VPIP hands: {}".format(report.sb_expected_vpip_profit)
    print "Loss from folded hands: {}".format(report.sb_forced_profit)
    print
    print_position_report(report.bb_report)
    print "Expected loss if fold all hands: {}".format(report.bb_expected_profit)
    print "VPIP profit: {}".format(report.bb_vpip_profit)
    print "Expected loss if fold all VPIP hands: {}".format(report.bb_expected_vpip_profit)
    print "Loss from folded hands: {}".format(report.bb_forced_profit)
    print "Expected loss from folded hands: {}".format(report.bb_expected_forced_profit)
    print

def print_profit_report(report):
    print "Hands played: {}".format(report.hand_count)
    print "VPIP%: {}".format(report.vpip)
    print "PFR%: {}".format(report.pfr)
    print "PFR profit: {}".format(report.pfr_profit)
    print "Flat%: {}".format(report.flat)
    print "Flat profit: {}".format(report.flat_profit)
    print "3bet%: {}".format(report.threebet)
    print "3bet profit: {}".format(report.threebet_profit)
    print "4bet%: {}".format(report.fourbet)
    print "4bet profit: {}".format(report.fourbet_profit)
    print "Total net profit: {}".format(report.profit)
    print "Total net profit (/100): {}".format(report.profit_per_100)
    print "Total rake: {}".format(report.rake)
    print

def print_position_report(report):
    print report.position
    print_profit_report(report.profit_report)

def print_preflop_report(report):
    print_profit_report(report.profit_report)
    print 'Steal success%: {}'.format(report.steal_success)
    print 'Steal fail%: {}'.format(report.steal_fail)
    print 'Steal profit: {}'.format(report.steal_profit)
    print 'Steal profit (/100): {}'.format(report.steal_profit_per_100)
    print 'AI preflop profit: {}'.format(report.ai_preflop_profit)
    print

# pylint: skip-file
def print_stats(hands, player):
    for h in []: #hands:
        print(h.lines[0].strip())
        print('PREFLOP')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.players[player].preflop, "|")))
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.preflop, "|")))

        print('FLOP')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.players[player].flop, "|")))
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.flop, "|")))

        print('TURN')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.players[player].turn, "|")))
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.turn, "|")))

        print('RIVER')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.players[player].river, "|")))
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.river, "|")))

    print('Hand statistics')
    print('Hands: {}'.format(len(hands)))
    positions = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
    for pos in positions:
        print('{} profit: {}'.format(pos, reduce(lambda acc, h: acc + h.profit_for_player(player), filter(lambda h: h.players[player].position == pos, hands), 0)))
    print('Total profit: {}'.format(reduce(lambda acc, h: acc + h.profit_for_player(player), hands, 0)))
    print('Profit/100: {}'.format(reduce(lambda acc, h: acc + h.profit_for_player(player), hands, 0) * 100 / len(hands)))

    preflop_lines = {}
    flop_lines = {}
    turn_lines = {}
    river_lines = {}
    for h in hands:
        l = reduce(lambda acc, a: acc + a.type.value, h.preflop_actions(player), '')
        preflop_lines[l] = preflop_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type.value, h.flop_actions(player), '')
        flop_lines[l] = flop_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type.value, h.turn_actions(player), '')
        turn_lines[l] = turn_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type.value, h.river_actions(player), '')
        river_lines[l] = river_lines.get(l, 0) + 1

    print('Lines taken (p - post, x - check, c - call, b - bet, r - raise, u - bet uncalled)')
    for (l,c) in preflop_lines.iteritems():
        print('Preflop {}: {}'.format(l, c))
    for (l,c) in flop_lines.iteritems():
        if l != '':
            print('Flop {}: {}'.format(l, c))
    for (l,c) in turn_lines.iteritems():
        if l != '':
            print('Turn {}: {}'.format(l, c))
    for (l,c) in river_lines.iteritems():
        if l != '':
            print('River {}: {}'.format(l, c))
