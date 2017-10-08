#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import entity
import logging

def apply(hands, player, voluntary, position):
    if voluntary:
        def flt(h):
            a = h.players[player].preflop
            if 'SB' in h.players[player].position or 'BB' in h.players[player].position:
                return a[1].type != entity.Action.Uncalled and a[1].type != entity.Action.Fold
            else:
                return a[0].type != entity.Action.Fold

        hands = filter(flt, hands)
        logging.debug('Voluntarily entered the pot with {} hands'.format(len(hands)))

    if position:
        hands = filter(lambda hand: hand.players[player].position in position, hands)
        logging.debug('{} hands played on {}'.format(len(hands), position))

    return hands
