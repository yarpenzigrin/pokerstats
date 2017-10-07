#!/usr/bin/env python2.7

import getopt
import logging
import operator
import sys

import entity
import report

def usage():
    print '''
Usage:
$ poker_stats.py [ARGS] [FILE]

Program arguments (ARGS):
    -p, --player: Name of the player, argument is mandatory
    -f, --position: Filter hands by position (BTN, SB, BB, UTG, MP, CO)
    -s, --sort: Sort hands by pot size
    -v, --voluntary: Filter hands which were played voluntarily
    -d, --dump: Dump hands in PokerStars format
'''

def fail(msg):
    logging.error(msg)
    usage()
    sys.exit(1)

def parseHandsFromFile(filename, player):
    result = []

    with open(filename, 'r') as inputfile:
        lines = inputfile.readlines()

    handInProcess = False
    for line in lines:
        if line == '\r\n' or line == '\n':
            if handInProcess:
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

def parse_arguments(argv):
    if len(argv) == 0:
        fail('No input arguments specified')

    try:                                
        opts, args = getopt.getopt(argv, 'p:f:svd', ['player=', 'position=', 'sort', 'voluntary', 'dump'])
    except getopt.GetoptError as e:
        fail(str(e))

    player = None
    sort = False
    posfilter = None
    voluntary = False
    dump = False
    for opt, arg in opts:
        if opt in ('-p', '--player'):
            player = arg
        if opt in ('-f', '--position'):
            posfilter = arg
        if opt in ('-s', '--sort'):
            sort = True
        if opt in ('-v', '--voluntary'):
            voluntary = True
        if opt in ('-d', '--dump'):
            dump = True

    if player == None:
        fail('Player not defined')

    if posfilter not in [None, 'BTN', 'SB', 'BB', 'UTG', 'MP', 'CO']:
        fail('Filter provided is invalid. Should one of: (BTN, SB, BB, UTG, MP, CO)')

    logging.info('Configuration')
    logging.info('Player: {}'.format(player))
    logging.info('Position: {}'.format(posfilter))
    logging.info('Sort: {}'.format(sort))
    logging.info('Voluntarily enter the pot: {}'.format(voluntary))
    logging.info('Dump hands: {}'.format(dump))

    return (player, posfilter, sort, voluntary, dump, args)

def dump_hands(hands):
    result = []
    for hand in hands:
        result.append(hand.lines[0].replace('PokerStars Zoom Hand', 'PokerStars Hand'))
        result.extend(hand.lines[1:])
        result.append('\r\n')
        result.append('\r\n')
        result.append('\r\n')

    sys.stdout.writelines(result)

def main(argv):
    logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')

    (player, position, sort, voluntary, dump, files) = parse_arguments(argv)

    hands = []
    for filename in files:
        logging.info('Parsing hands from {}'.format(filename))
        hands.extend(parseHandsFromFile(filename, player))
    logging.info('Parsed {} hands'.format(len(hands)))

    hands = filter(lambda h: len(h.preflop) > 0, hands)
    logging.info('{} participated in {} hands'.format(player, len(hands)))

    if voluntary:
        def flt(h):
            a = h.preflop
            if 'SB' in h.position or 'BB' in h.position:
                return a[1].type != entity.Action.Uncalled and a[1].type != entity.Action.Fold
            else:
                return a[0].type != entity.Action.Fold

        hands = filter(flt, hands)
        logging.info('Voluntarily entered the pot with {} hands'.format(len(hands)))

    if position != None:
        hands = filter(lambda hand: hand.position == position, hands)
        logging.info('{} hands played on {}'.format(len(hands), position))

    if sort:
        hands.sort(key = lambda hand: hand.pot, reverse=True)

    if dump:
        dump_hands(hands)

    report.print_stats(hands)

if __name__ == '__main__':
    main(sys.argv[1:])
