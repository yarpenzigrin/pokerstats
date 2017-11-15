#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

def create_player_filter(player):
    return lambda h: player in h.players.keys()

def create_position_filter(player, positions):
    return lambda h: player in h.players and h.players[player].position in positions

def create_voluntary_filter(player, voluntary):
    pred = lambda h: [1 for a in h.preflop + h.flop + h.turn + h.river if a.is_voluntary() and a.player.name == player]
    if voluntary == 'only':
        return pred
    return lambda h: not pred(h)

def create(hand_filter, player_name):
    result = []

    result.append(create_player_filter(player_name))

    positions = hand_filter.get('positions', None)
    if positions:
        result.append(create_position_filter(player_name, positions))

    voluntary = hand_filter.get('voluntary', None)
    if voluntary:
        result.append(create_voluntary_filter(player_name, voluntary))

    return result

def apply_filters(hands, filters, sort=False):
    def pred(hand):
        return reduce(lambda acc, flt: acc and flt(hand), filters, True)

    hands = [hand for hand in hands if pred(hand)]
    if sort:
        hands = sorted(hands, key=lambda h: h.pot, reverse=True)
    return hands

def apply_filter(hands, flt):
    return [hand for hand in hands if flt(hand)]
