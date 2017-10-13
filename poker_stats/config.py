#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pyparsing import Word, StringEnd, Suppress, ZeroOrMore, alphas, nums

action = None
files = []
hand_filter = {'player':None, 'positions':None, 'voluntary': False}
sort = False

def parse_filter(line):
    position = Word('SB') ^ Word('BB') ^ Word('UTG') ^ Word('MP') ^ Word('CO') ^ Word('BTN')
    position_list = position + ZeroOrMore(Suppress(Word(',')) + position)
    position_filter = (Word('p') ^ Word('pos') ^ Word('position')) + Suppress('=') + position_list("positions")
    player_filter = (Word('n') ^ Word('name')) + Suppress('=') + Word(alphas)("player")
    voluntary_filter = (Word('v') ^ Word('voluntary')) + Suppress('=') + Word(nums)("voluntary")
    any_filter = player_filter ^ position_filter ^ voluntary_filter
    grammar = any_filter + ZeroOrMore(Suppress(Word(';')) + any_filter) + StringEnd()

    return grammar.parseString(line).asDict()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--filter', help='Hand filter e. g. --filter "N=HubertusB;P=BTN,CO;V=1"', type=str, default='V=1')
    action_parser = parser.add_subparsers(help='Available actions', dest='action')

    dump_parser = action_parser.add_parser('dump_ps', help='Dump hands in PS format')
    dump_parser.add_argument('-s', '--sort', action='store_true', help='Sort the dump by the size of the pot')
    dump_parser.add_argument('files', help='File list', nargs='+')

    report_parser = action_parser.add_parser('report', help='Print hand report for a player')
    report_parser.add_argument('files', help='File list', nargs='+')

    return parser.parse_args()

def parse_and_validate_args():
    global action, files, sort
    args = parse_args()
    action = args.action
    files = args.files
    if args.__contains__('sort'):
        sort = args.sort

    hand_filter.update(parse_filter(args.filter))
