#!/usr/bin/env python2.7

from entity import Action

def print_stats(hands):

    for h in []: #hands:
        print(h.lines[0].strip())
        print("Profit: " + str(h.getProfit()))
        print('PREFLOP')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.preflop, "|")))

        print('FLOP')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.flop, "|")))

        print('TURN')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.turn, "|")))

        print('RIVER')
        print('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.river, "|")))

    print('Hand statistics')
    print('Hands: {}'.format(len(hands)))
    positions = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
    for pos in positions:
        print('{} profit: {}'.format(pos, reduce(lambda acc, h: acc + h.getProfit(), filter(lambda h: h.position == pos, hands), 0)))
    print('Total profit: {}'.format(reduce(lambda acc, h: acc + h.getProfit(), hands, 0)))
    print('Profit/100: {}'.format(reduce(lambda acc, h: acc + h.getProfit(), hands, 0) * 100 / len(hands)))

    #print('Hand depth')
    #print('Preflop: {}'.format(len(filter(lambda h: len(h.players[player].flop) == 0, hands))))
    #print('Flop: {}'.format(len(filter(lambda h: len(h.players[player].flop) > 0 and len(h.turn) == 0, hands))))
    #print('Turn: {}'.format(len(filter(lambda h: len(h.players[player].turn) > 0 and len(h.river) == 0, hands))))
    #print('River: {}'.format(len(filter(lambda h: len(h.players[player].river) > 0, hands))))

    preflop_lines = {}
    flop_lines = {}
    turn_lines = {}
    river_lines = {}
    for h in hands:
        l = reduce(lambda acc, a: acc + a.type, h.preflop, '')
        #preflop_lines[l] = preflop_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type, h.flop, '')
        #flop_lines[l] = flop_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type, h.turn, '')
        #turn_lines[l] = turn_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type, h.river, '')
        #river_lines[l] = river_lines.get(l, 0) + 1

    #print('Lines taken (p - post, x - check, c - call, b - bet, r - raise, u - bet uncalled)')
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
