#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from logging import basicConfig, INFO
from sys import stdout

import poker_stats.config as config
import poker_stats.hand_filter as hand_filter
import poker_stats.hand_parser as hand_parser
import poker_stats.report as report
import poker_stats.report_printer as report_printer

def initialize():
    basicConfig(level=INFO, format='[ %(levelname)s ] %(message)s')
    config.parse_and_validate_args()

def main():
    initialize()

    hands = hand_parser.parse_files(config.files)
    hand_filters = hand_filter.create(config.hand_filter)
    hands = hand_filter.apply_filters(hands, hand_filters, config.sort)

    if config.action == 'dump_ps':
        stdout.writelines(reduce(lambda a, h: a + h.lines, hands, []))

    if config.action == 'report':
        report_printer.print_stats(hands, config.hand_filter['player'])

    if config.action == 'blind_report':
        rep = report.create_blind_report(hands, config.player_name)
        report_printer.print_blind_report(rep)

    if config.action == 'position_report':
        positions = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
        reports = [report.create_position_report(hands, config.player_name, p) for p in positions]
        for rep in reports:
            report_printer.print_position_report(rep)

if __name__ == '__main__':
    main()
