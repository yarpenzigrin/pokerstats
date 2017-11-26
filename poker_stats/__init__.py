#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from codecs import BOM_UTF8
from logging import basicConfig, INFO
from sys import stdout

from . import config
from . import hand_filter
from . import hand_parser
from . import report
from . import report_printer

def initialize():
    basicConfig(level=INFO, format='[ %(levelname)s ] %(message)s')
    config.parse_and_validate_args()

def main():
    initialize()

    store_lines = config.action == 'dump_ps'
    hands = hand_parser.parse_files(config.files, store_lines)
    hand_filters = hand_filter.create(config.hand_filter, config.player_name)
    hands = hand_filter.apply_filters(hands, hand_filters, config.sort)

    if config.action == 'dump_ps':
        stdout.write(BOM_UTF8)
        stdout.writelines(reduce(lambda a, h: a + h.lines, hands, []))

    if config.action == 'report':
        report_printer.print_stats(hands, config.player_name)

    if config.action == 'blind_report':
        rep = report.create_blind_report(hands, config.player_name)
        report_printer.print_blind_report(rep)

    if config.action == 'position_report':
        positions = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
        reports = [report.create_position_report(hands, config.player_name, p) for p in positions]
        for rep in reports:
            report_printer.print_position_report(rep)

    if config.action == 'preflop_report':
        rep = report.create_preflop_report(hands, config.player_name)
        report_printer.print_preflop_report(rep)

if __name__ == '__main__':
    main()
