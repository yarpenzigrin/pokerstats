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
    allHands = handparser.parseHandsFromFiles(config.args.files, config.args.player)
    filteredHands = handfilter.apply(allHands, config.args.voluntary, config.args.position)

    if config.args.dump:
        dump_hands(filteredHands)

    report.print_stats(filteredHands)

if __name__ == '__main__':
    main()
