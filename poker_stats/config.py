#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pyparsing import Literal, Word, StringEnd, Suppress, ZeroOrMore, alphas, nums

action = None
files = []
hand_filter = {}
sort = False

def parse_filter(line):
    preflop_players = Literal('preflop_players') + Suppress('=') + Word(nums)('preflop_players')
    flop_players = Literal('flop_players') + Suppress('=') + Word(nums)('flop_players')
    single_position = Literal('SB') ^ Literal('BB') ^ Literal('UTG') ^ Literal('MP') ^ Literal('CO') ^ Literal('BTN')
    position_list = single_position + ZeroOrMore(Suppress(Word(',')) + single_position)
    position = (Literal('pos') ^ Literal('position')) + Suppress('=') + position_list('positions')
    player = Literal('name') + Suppress('=') + Word(alphas)('player')
    voluntary = Literal('voluntary') + Suppress('=') + (Literal('only') ^ Literal('forced'))('voluntary')
    anyf = (player ^ position ^ voluntary ^ preflop_players ^ flop_players)
    grammar = anyf + ZeroOrMore(Suppress(Word(';')) + anyf) + StringEnd()

    return grammar.parseString(line).asDict()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--filter', help='Hand filter e. g. --filter "name=HubertusB;position=BTN,CO;voluntary=forced"')
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
    if args.__contains__('filter'):
        hand_filter.update(parse_filter(args.filter))
