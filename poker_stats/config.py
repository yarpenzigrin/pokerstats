#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pyparsing import Word, StringEnd, Suppress, ZeroOrMore, alphas, nums

action = None
files = []
filter = { 'player':None, 'position':None, 'voluntary': False }
sort_dump = False
lines = 0

def parse_filter(line):
    POSITION = Word('SB') ^ Word('BB') ^ Word('UTG') ^ Word('MP') ^ Word('CO') ^ Word('BTN')
    POSITION_LIST = POSITION + ZeroOrMore(Suppress(Word(',')) + POSITION)
    POSITION_FILTER = Word('P') + Suppress('=') + POSITION_LIST("position")
    PLAYER_FILTER = Word('N') + Suppress('=') + Word(alphas)("player")
    VOLUNTARY_FILTER = Word('V') + Suppress('=') + Word(nums)("voluntary")
    ANY_FILTER = PLAYER_FILTER ^ POSITION_FILTER ^ VOLUNTARY_FILTER
    GRAMMAR = ANY_FILTER + ZeroOrMore(Suppress(Word(';')) + ANY_FILTER) + StringEnd()

    return GRAMMAR.parseString(line).asDict()

def parse_args():
    parser = ArgumentParser()
    action_parser = parser.add_subparsers(help='Available actions', dest='action')

    dump_parser = action_parser.add_parser('dump', help='Dump hands')
    dump_parser.add_argument('-f', '--filter', help='Hand filter e. g. --filter "N=HubertusB;P=BTN,CO;V=1"', type=str)
    dump_parser.add_argument('-s', '--sort', action='store_true', help='Sort the dump by the size of the pot')
    dump_parser.add_argument('files', help='File list', nargs='+')

    report_parser = action_parser.add_parser('report', help='Print hand report for a player')
    report_parser.add_argument('-f', '--filter', help='Hand filter e. g. --filter "N=HubertusB;P=BTN,CO;V=1"', type=str)
    report_parser.add_argument('files', help='File list', nargs='+')

    new_report_parser = action_parser.add_parser('new_report', help='Print old hand report for a player')
    new_report_parser.add_argument('-f', '--filter', help='Hand filter e. g. --filter "N=HubertusB;P=BTN,CO;V=1"', type=str)
    new_report_parser.add_argument('-l', '--lines', help='Count of top unprofitable lines to print (0 - no lines printed)', type=int, default=0)
    new_report_parser.add_argument('files', help='File list', nargs='+')

    return parser.parse_args()

def parse_and_validate_args():
    global action, files, filter, sort_dump, lines
    args = parse_args()
    action = args.action
    files = args.files
    if args.__contains__('sort'):
        sort_dump = args.sort
    if args.__contains__('filter') and args.filter:
        filter.update(parse_filter(args.filter))
    if args.__contains__('lines'):
        lines = args.lines
