#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

def create_player_filter(player):
    return lambda h: player in h.players.keys()

def create_position_filter(player, positions):
    return lambda h: player in h.players and h.players[player].position in positions

def create_voluntary_filter(player, voluntary):
    pred = lambda h: [1 for a in h.preflop + h.flop + h.turn + h.river if a.voluntary() and a.player.name == player]
    if voluntary == 'only':
        return pred
    else:
        return lambda h: not pred(h)

def create_preflop_players_filter(preflop_players):
    return lambda h: h.preflop_vpip_player_count() == int(preflop_players)

def create_flop_players_filter(flop_players):
    return lambda h: h.flop_player_count() == int(flop_players)

def create(hand_filter):
    result = []

    player = hand_filter.get('player', None)
    if player:
        result.append(create_player_filter(player))

    positions = hand_filter.get('positions', None)
    if player and positions:
        result.append(create_position_filter(player, positions))

    voluntary = hand_filter.get('voluntary', None)
    if player and voluntary:
        result.append(create_voluntary_filter(player, voluntary))

    preflop_players = hand_filter.get('preflop_players', None)
    if preflop_players:
        result.append(create_preflop_players_filter(preflop_players))

    flop_players = hand_filter.get('flop_players', None)
    if flop_players:
        result.append(create_flop_players_filter(flop_players))

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
