#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from .entity import is_call_preflop, is_raise_preflop, is_3bet_preflop, is_4bet_preflop # pylint: disable=no-name-in-module

def create_player_filter(player_name):
    return lambda h: player_name in h.players.keys()

def create_position_filter(player_name, positions):
    return lambda h: player_name in h.players and h.players[player_name].position in positions

def create_voluntary_filter(player_name, voluntary):
    pred = lambda h: [1 for a in h.preflop + h.flop + h.turn + h.river if a.is_voluntary() and a.player.name == player_name]
    if voluntary == 'only':
        return pred
    return lambda h: not pred(h)

def create_call_pf_filter(player_name):
    return lambda h: is_call_preflop(h.preflop, player_name)

def create_pfr_filter(player_name):
    return lambda h: is_raise_preflop(h.preflop, player_name)

def create_3bet_filter(player_name):
    return lambda h: is_3bet_preflop(h.preflop, player_name)

def create_4bet_filter(player_name):
    return lambda h: is_4bet_preflop(h.preflop, player_name)

def create(hand_filter, player_name):
    result = []

    result.append(create_player_filter(player_name))

    positions = hand_filter.get('positions', None)
    if positions:
        result.append(create_position_filter(player_name, positions))

    voluntary = hand_filter.get('voluntary', None)
    if voluntary:
        result.append(create_voluntary_filter(player_name, voluntary))

    threebet = hand_filter.get('3bet', None)
    if threebet:
        result.append(create_3bet_filter(player_name))

    fourbet = hand_filter.get('4bet', None)
    if fourbet:
        result.append(create_4bet_filter(player_name))

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
