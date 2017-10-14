#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from sets import Set
import poker_stats.entity as entity

def create(hand_filter):
    result = []

    player = hand_filter.get('player', None)
    if player:
        result.append(lambda h: player in h.players.keys())

    positions = hand_filter.get('positions', None)
    if player and positions:
        result.append(lambda h: h.players[player].position in positions)

    voluntary = hand_filter.get('voluntary', None)
    if player and voluntary:
        pred = lambda h: [1 for a in h.preflop + h.flop + h.turn + h.river if a.voluntary() and a.player.name == player]
        if voluntary == 'only':
            result.append(pred)
        else:
            result.append(lambda h: not pred(h))

    preflop_players = hand_filter.get('preflop_players', None)
    if preflop_players:
        result.append(lambda h: h.preflop_vpip_player_count() == int(preflop_players))

    flop_players = hand_filter.get('flop_players', None)
    if flop_players:
        result.append(lambda h: h.flop_player_count() == int(flop_players))

    return result

def applyf(hands, filters, sort):
    def pred(hand):
        return reduce(lambda acc, flt: acc and flt(hand), filters, True)

    hands = [hand for hand in hands if pred(hand)]
    if sort:
        hands = sorted(hands, key=lambda h: h.pot, reverse=True)
    return hands
