#!/usr/bin/env python2.7

import logging

import entity

def print_stats(hands):

    for h in hands:
        logging.debug(h.lines[0].strip())
        logging.debug("Profit: " + str(h.getProfit()))
        logging.debug('PREFLOP')
        logging.debug('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.preflop, "|")))

        logging.debug('FLOP')
        logging.debug('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.flop, "|")))

        logging.debug('TURN')
        logging.debug('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.turn, "|")))

        logging.debug('RIVER')
        logging.debug('action {}'.format(reduce(lambda acc, a: acc + str(a) + '|', h.river, "|")))

    logging.info('Hand statistics')
    logging.info('Hands: {}'.format(len(hands)))
    positions = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
    for pos in positions:
        logging.info('{} profit: {}'.format(pos, reduce(lambda acc, h: acc + h.getProfit(), filter(lambda h: h.position == pos, hands), 0)))
    logging.info('Total profit: {}'.format(reduce(lambda acc, h: acc + h.getProfit(), hands, 0)))
    logging.info('Profit/100: {}'.format(reduce(lambda acc, h: acc + h.getProfit(), hands, 0) * 100 / len(hands)))

    logging.info('Hand depth')
    logging.info('Preflop: {}'.format(len(filter(lambda h: len(h.flop) == 0, hands))))
    logging.info('Flop: {}'.format(len(filter(lambda h: len(h.flop) > 0 and len(h.turn) == 0, hands))))
    logging.info('Turn: {}'.format(len(filter(lambda h: len(h.turn) > 0 and len(h.river) == 0, hands))))
    logging.info('River: {}'.format(len(filter(lambda h: len(h.river) > 0, hands))))

    preflop_lines = {}
    flop_lines = {}
    turn_lines = {}
    river_lines = {}
    for h in hands:
        l = reduce(lambda acc, a: acc + a.type, h.preflop, '')
        preflop_lines[l] = preflop_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type, h.flop, '')
        flop_lines[l] = flop_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type, h.turn, '')
        turn_lines[l] = turn_lines.get(l, 0) + 1
        l = reduce(lambda acc, a: acc + a.type, h.river, '')
        river_lines[l] = river_lines.get(l, 0) + 1

    logging.info('Lines taken (p - post, x - check, c - call, b - bet, r - raise, u - bet uncalled)')
    for (l,c) in preflop_lines.iteritems():
        logging.info('Preflop {}: {}'.format(l, c))
    for (l,c) in flop_lines.iteritems():
        if l != '':
            logging.info('Flop {}: {}'.format(l, c))
    for (l,c) in turn_lines.iteritems():
        if l != '':
            logging.info('Turn {}: {}'.format(l, c))
    for (l,c) in river_lines.iteritems():
        if l != '':
            logging.info('River {}: {}'.format(l, c))
