#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pyparsing import Literal, Word, StringEnd, Suppress, ZeroOrMore

action = None
files = []
hand_filter = {}
player_name = None
sort = False

def parse_filter(line):
    single_position = Literal('SB') ^ Literal('BB') ^ Literal('UTG') ^ Literal('MP') ^ Literal('CO') ^ Literal('BTN')
    position_list = single_position + ZeroOrMore(Suppress(Word(',')) + single_position)
    position = (Literal('pos') ^ Literal('position')) + Suppress('=') + position_list('positions')
    voluntary = Literal('voluntary') + Suppress('=') + (Literal('only') ^ Literal('forced'))('voluntary')
    threebet = Literal('3bet')('3bet')
    fourbet = Literal('4bet')('4bet')
    anyf = (position ^ voluntary ^ threebet ^ fourbet)
    grammar = anyf + ZeroOrMore(Suppress(Word(';')) + anyf) + StringEnd()

    return grammar.parseString(line).asDict()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--filter', help='Hand filter e. g. --filter "position=BTN,CO;voluntary=forced"')
    action_parser = parser.add_subparsers(help='Available actions', dest='action')

    dump_parser = action_parser.add_parser('dump_ps', help='Dump hands in PS format')
    dump_parser.add_argument('-s', '--sort', action='store_true', help='Sort the dump by the size of the pot')
    dump_parser.add_argument('player_name', help='Player nickname')
    dump_parser.add_argument('files', help='File list', nargs='+')

    report_parser = action_parser.add_parser('report', help='Print hand report for a player')
    report_parser.add_argument('player_name', help='Player nickname')
    report_parser.add_argument('files', help='File list', nargs='+')

    blind_report_parser = action_parser.add_parser('blind_report', help='Print report for a player about play on the blinds')
    blind_report_parser.add_argument('player_name', help='Player nickname')
    blind_report_parser.add_argument('files', help='File list', nargs='+')

    position_report_parser = action_parser.add_parser('position_report', help='Print positional report for a player')
    position_report_parser.add_argument('player_name', help='Player nickname')
    position_report_parser.add_argument('files', help='File list', nargs='+')

    preflop_report_parser = action_parser.add_parser('preflop_report', help='Print report for a player about preflop play')
    preflop_report_parser.add_argument('player_name', help='Player nickname')
    preflop_report_parser.add_argument('files', help='File list', nargs='+')

    return parser.parse_args()

def parse_and_validate_args():
    global action, files, player_name, sort
    args = parse_args()
    action = args.action
    files = args.files
    if args.__contains__('sort') and args.sort:
        sort = args.sort
    if args.__contains__('filter') and args.filter:
        hand_filter.update(parse_filter(args.filter))
    if args.__contains__('player_name') and args.player_name:
        player_name = args.player_name
