#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from logging import basicConfig, INFO
from sys import stdout

import poker_stats.config as config
import poker_stats.handfilter as handfilter
import poker_stats.handparser as handparser
import poker_stats.report as report

def initialize():
    basicConfig(level=INFO, format='[ %(levelname)s ] %(message)s')
    config.parse_and_validate_args()

def dump_hands(hands):
    if config.sort_dump:
        hands = sorted(hands, key=lambda hand: hand.pot, reverse=True)
    stdout.writelines(reduce(lambda acc, h: acc + h.lines, hands, []))

def main():
    initialize()

    hands = handparser.parse_files(config.files)
    hand_filter = handfilter.create(config.hand_filter)
    hands = handfilter.applyf(hands, hand_filter)

    if config.action == 'dump_ps':
        dump_hands(hands)

    if config.action == 'report':
        report.print_stats(hands, config.hand_filter['player'])

if __name__ == '__main__':
    main()
