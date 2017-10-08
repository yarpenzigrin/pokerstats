#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

import poker_stats.config as config
import poker_stats.entity as entity
import poker_stats.handfilter as handfilter
import poker_stats.handparser as handparser
import poker_stats.report as report

def dump_hands(hands):
    if config.args.sort:
        hands = sorted(hands, key = lambda hand: hand.pot, reverse=True)
    sys.stdout.writelines(reduce(lambda acc, h: acc + h.lines, hands, []))

def main():
    hands = handparser.parse_files(config.args.files, config.args.player)
    hands = handfilter.apply(hands, config.args.voluntary, config.args.position)

    if config.args.action == 'dump':
        dump_hands(hands)

    if config.args.action == 'report':
        report.print_stats(hands)

if __name__ == '__main__':
    main()
