#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import entity
import logging

def parseHandsFromFiles(fileNames, playerName):
    hands = []

    for filename in fileNames:
        logging.debug('Parsing hands from {}'.format(filename))
        hands.extend(parseHandsFromFile(filename, playerName))
    logging.debug('Parsed {} hands'.format(len(hands)))

    return hands

def parseHandsFromFile(filename, player):
    result = []

    with open(filename, 'r') as inputfile:
        lines = inputfile.readlines()

    handInProcess = False
    for line in lines:
        if line == '\r\n':
            if handInProcess:
                hand.lines[0].replace('PokerStars Zoom Hand', 'PokerStars Hand')
                hand.lines.append('\r\n')
                hand.lines.append('\r\n')
                hand.lines.append('\r\n')
                hand.parse(player)

                if hand.position != None:
                    result.append(hand)
                else:
                    logging.error("KNAGA")

                handInProcess = False
        else:
            if not handInProcess:
                hand = entity.Hand()
                handInProcess = True

            hand.lines.append(line)

    return result
