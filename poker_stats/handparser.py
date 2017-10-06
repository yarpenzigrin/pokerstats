#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import entity
import logging
import re

def parse_files(file_names, player_name):
    hands = []

    for fn in file_names:
        with open(fn, 'r') as f:
            lines = f.readlines()
        hands.extend(parse_file_content(lines, player_name))

    return hands

def parse_file_content(lines, player):
    hands = []

    hand_in_process = False
    hand_lines = []
    for line in lines:
        if line == '\r\n':
            if hand_in_process:
                hand_lines[0].replace('PokerStars Zoom Hand', 'PokerStars Hand')
                hand_lines.append('\r\n')
                hand_lines.append('\r\n')
                hand_lines.append('\r\n')

                hands.append(parse_hand(hand_lines, player))
                hand_in_process = False
        else:
            if not hand_in_process:
                hand_lines = []
                hand_in_process = True

            hand_lines.append(line)

    return hands

def parse_hand(lines, player):
    hand = entity.Hand()
    hand.lines = lines
    hand.pot = getTotalPot(lines)

    if player != None:
        hand.collected = getCollectedFromPot(lines, player)
        hand.position = getPlayerPosition(lines, player)
        hand.preflop = getPlayerPreflopActions(lines, player)
        hand.flop = getPlayerFlopActions(lines, player)
        hand.turn = getPlayerTurnActions(lines, player)
        hand.river = getPlayerRiverActions(lines, player)

    return hand

def getPlayerPosition(lines, player):
    result = None
    positionMap = { None:None, '1':'BTN', '2':'SB', '3':'BB', '4':'UTG', '5':'MP', '6':'CO' }

    r = re.compile('Seat (\d): {} \(\$'.format(player))
    for l in lines:
        m = re.match(r, l)
        if m != None:
            result = m.groups()[0]
            break

    return positionMap[result]

def getPlayerPreflopActions(lines, player):
    result = []

    foldRe = re.compile('{}: folds'.format(player))
    checkRe = re.compile('{}: checks'.format(player))
    callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
    betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
    postRe = re.compile('{}: posts (small|big) blind \$(\d+(.\d+)?)'.format(player))
    raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
    uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

    preflop = False
    for l in lines:
        line = l.rstrip()

        m = re.match(postRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Post, float(m.groups()[1])))

        if not preflop:
            if '*** HOLE CARDS ***' in line:
                preflop = True
            else:
                continue

        if preflop and ('*** SUMMARY ***' in line or '*** FLOP ***' in line):
            break

        m = re.match(foldRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Fold, 0))

        m = re.match(checkRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Check, 0))

        m = re.match(callRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Call, float(m.groups()[0])))

        m = re.match(betRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Bet, float(m.groups()[0])))

        m = re.match(raiseRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Raise, float(m.groups()[2])))

        m = re.match(uncalledRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Uncalled, -float(m.groups()[0])))

    return result

def getPlayerFlopActions(lines, player):
    result = []

    foldRe = re.compile('{}: folds'.format(player))
    checkRe = re.compile('{}: checks'.format(player))
    callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
    betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
    raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
    uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

    flop = False
    for l in lines:
        line = l.rstrip()

        if not flop:
            if '*** FLOP ***' in line:
                flop = True
            else:
                continue

        if flop and ('*** SUMMARY ***' in line or '*** TURN ***' in line):
            break

        m = re.match(foldRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Fold, 0))

        m = re.match(checkRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Check, 0))

        m = re.match(callRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Call, float(m.groups()[0])))

        m = re.match(betRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Bet, float(m.groups()[0])))

        m = re.match(raiseRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Raise, float(m.groups()[2])))

        m = re.match(uncalledRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Uncalled, -float(m.groups()[0])))

    return result

def getPlayerTurnActions(lines, player):
    result = []

    foldRe = re.compile('{}: folds'.format(player))
    checkRe = re.compile('{}: checks'.format(player))
    callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
    betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
    raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
    uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

    turn = False
    for l in lines:
        line = l.rstrip()

        if not turn:
            if '*** TURN ***' in line:
                turn = True
            else:
                continue

        if turn and ('*** SUMMARY ***' in line or '*** RIVER ***' in line):
            break

        m = re.match(foldRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Fold, 0))

        m = re.match(checkRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Check, 0))

        m = re.match(callRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Call, float(m.groups()[0])))

        m = re.match(betRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Bet, float(m.groups()[0])))

        m = re.match(raiseRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Raise, float(m.groups()[2])))

        m = re.match(uncalledRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Uncalled, -float(m.groups()[0])))

    return result

def getPlayerRiverActions(lines, player):
    result = []

    foldRe = re.compile('{}: folds'.format(player))
    checkRe = re.compile('{}: checks'.format(player))
    callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
    betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
    raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
    uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

    river = False
    for l in lines:
        line = l.rstrip()

        if not river:
            if '*** RIVER ***' in line:
                river = True
            else:
                continue

        if river and ('*** SUMMARY ***' in line):
            break

        m = re.match(foldRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Fold, 0))

        m = re.match(checkRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Check, 0))

        m = re.match(callRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Call, float(m.groups()[0])))

        m = re.match(betRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Bet, float(m.groups()[0])))

        m = re.match(raiseRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Raise, float(m.groups()[2])))

        m = re.match(uncalledRe, line)
        if m != None:
            result.append(entity.Action(entity.Action.Uncalled, -float(m.groups()[0])))

    return result

def getTotalPot(lines):
    result = None

    r = re.compile('Total pot \$(\d+(.\d+)?) \| Rake \$(\d+(.\d+)?)')
    for l in lines:
        m = re.match(r, l)
        if m != None:
            result = float(m.groups()[0])
            break

    return result

def getCollectedFromPot(lines, player):
    result = 0

    collectedRe = re.compile('{} collected \$(\d+(.\d+)?) from pot'.format(player))

    for l in lines:
        line = l.rstrip()

        m = re.match(collectedRe, line)
        if m != None:
            result = float(m.groups()[0])
            break

    return result
