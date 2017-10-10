#!/usr/bin/env python2.7

from entity import Action

def get_profit_for_player(hand, player):
    def invested(acc, a):
        if a.type == Action.Raise:
            return a.value
        elif a.type == Action.Uncalled:
            return acc - a.value
        else:
            return acc + a.value
    return hand.players[player].collected \
        - reduce(invested, hand.players[player].preflop, 0) \
        - reduce(invested, hand.players[player].flop, 0) \
        - reduce(invested, hand.players[player].turn, 0) \
        - reduce(invested, hand.players[player].river, 0)

def calculate_profit_for_hands(hands, player):
    return reduce(lambda acc, h: acc + get_profit_for_player(h, player), hands, 0.0)

def print_basic_stats(hands, player, prefix):
    profit = calculate_profit_for_hands(hands, player)
    print '%s: %.2f$ | %d hands | %.2f$ / 100 hands' % (
            prefix, profit, len(hands), profit/len(hands)*100 if len(hands) else 0
        )

def get_line_signature(hand, player):
    signature = reduce(lambda acc, a: acc + a.type, hand.players[player].preflop, "|")
    signature += reduce(lambda acc, a: acc + a.type, hand.players[player].flop, "|")
    signature += reduce(lambda acc, a: acc + a.type, hand.players[player].turn, "|")
    signature += reduce(lambda acc, a: acc + a.type, hand.players[player].river, "|")
    return signature

def print_holdings(hands, player):
    print reduce(lambda acc, hand: acc + hand.players[player].holding + ' | ', hands, "")

def print_line_stats(hands, player, linesCnt):
    lineToHands = {}
    for hand in hands:
        signature = get_line_signature(hand, player)
        if signature in lineToHands.keys():
            lineToHands[signature].append(hand)
        else:
            lineToHands[signature] = [ hand ]

    lineToHandsByProfit = {}
    for line, handsForLine in lineToHands.iteritems():
        lineToHandsByProfit[calculate_profit_for_hands(handsForLine, player)] = (line, handsForLine)

    count = 1
    for line, lineAndHands in lineToHandsByProfit.iteritems():
        if count > linesCnt:
            break
        print_basic_stats(lineAndHands[1], player, lineAndHands[0])
        print_holdings(lineAndHands[1], player)
        count += 1

def print_stats_total(hands, player, linesCnt):
    print '============================================================'
    print_basic_stats(hands, player, 'Total')
    if linesCnt:
        print '\nLines:'
    print_line_stats(hands, player, linesCnt)

def print_stats_position(hands, player, position, linesCnt):
    print '------------------------------------------------------------'
    filtered_hands = filter(lambda h: h.players[player].position == position, hands)
    print_basic_stats(filtered_hands, player, position)
    if linesCnt:
        print '\nLines:'
    print_line_stats(filtered_hands, player, linesCnt)

def print_stats(hands, player, linesCnt):
    print 'Hand statistics for {0} ({1!s} hands)\n'.format(player, len(hands))
    print_stats_total(hands, player, linesCnt)
    print_stats_position(hands, player, 'BTN', linesCnt)
    print_stats_position(hands, player, 'SB', linesCnt)
    print_stats_position(hands, player, 'BB', linesCnt)
    print_stats_position(hands, player, 'UTG', linesCnt)
    print_stats_position(hands, player, 'MP', linesCnt)
    print_stats_position(hands, player, 'CO', linesCnt)
