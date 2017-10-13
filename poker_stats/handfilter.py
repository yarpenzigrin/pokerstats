#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import poker_stats.entity as entity

def create(hand_filter):
    result = []

    player = hand_filter.get('player', None)
    if player:
        result.append(lambda h: player in h.players.keys())
    positions = hand_filter.get('positions', None)
    if player and positions:
        result.append(lambda h: h.players[player].position in positions)
    voluntary = hand_filter.get('voluntary', 'all')
    if player and voluntary != 'all':
        vol = [entity.Action.Bet, entity.Action.Call, entity.Action.Raise]
        pred = lambda h: [1 for a in h.players[player].preflop + h.players[player].flop + \
                          h.players[player].turn + h.players[player].river if a.type in vol]
        if voluntary == 'only':
            result.append(pred)
        else:
            result.append(lambda h: not pred(h))

    return result

def applyf(hands, filters, sort):
    def pred(hand):
        return reduce(lambda acc, pred: acc and pred(hand), filters, True)

    hands = [hand for hand in hands if pred(hand)]
    if sort:
        hands = sorted(hands, key=lambda h: h.pot, reverse=True)
    return hands
