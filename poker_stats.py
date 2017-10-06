#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import getopt
import logging
import operator
import sys

import poker_stats.config as config
import poker_stats.entity as entity
import poker_stats.report as report

def parseHandsFromFile(filename, player):
    result = []

    with open(filename, 'r') as inputfile:
        lines = inputfile.readlines()

    handInProcess = False
    for line in lines:
        if line == '\r\n':
            if handInProcess:
                hand.lines[0].replace('PokerStars Zoom Hand', 'PokerStars Hand')
                hand.lines.append('\r\n')
                hand.lines.append('\r\n')
                hand.lines.append('\r\n')
                hand.parse(player)

                if hand.position != None:
                    result.append(hand)
                handInProcess = False
        else:
            if not handInProcess:
                hand = entity.Hand()
                handInProcess = True

            hand.lines.append(line)

    return result

def dump_hands(hands):
    sys.stdout.writelines(reduce(lambda acc, h: acc + h.lines, hands, []))

def main():
    logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')

    hands = []
    for filename in config.args.files:
        logging.info('Parsing hands from {}'.format(filename))
        hands.extend(parseHandsFromFile(filename, config.args.player))
    logging.info('Parsed {} hands'.format(len(hands)))

    hands = filter(lambda h: len(h.preflop) > 0, hands)
    logging.info('{} participated in {} hands'.format(config.args.player, len(hands)))

    if config.args.voluntary:
        def flt(h):
            a = h.preflop
            if 'SB' in h.position or 'BB' in h.position:
                return a[1].type != entity.Action.Uncalled and a[1].type != entity.Action.Fold
            else:
                return a[0].type != entity.Action.Fold

        hands = filter(flt, hands)
        logging.info('Voluntarily entered the pot with {} hands'.format(len(hands)))

    if config.args.position != None:
        hands = filter(lambda hand: hand.position == config.args.position, hands)
        logging.info('{} hands played on {}'.format(len(hands), config.args.position))

    if config.args.sort:
        hands.sort(key = lambda hand: hand.pot, reverse=True)

    if config.args.dump:
        dump_hands(hands)

    report.print_stats(hands)

if __name__ == '__main__':
    main()
