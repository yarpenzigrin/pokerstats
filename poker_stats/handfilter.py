#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import entity
import logging

def apply(hands, voluntary, position):
    if voluntary:
        def flt(h):
            a = h.preflop
            if 'SB' in h.position or 'BB' in h.position:
                return a[1].type != entity.Action.Uncalled and a[1].type != entity.Action.Fold
            else:
                return a[0].type != entity.Action.Fold

        hands = filter(flt, hands)
        logging.debug('Voluntarily entered the pot with {} hands'.format(len(hands)))

    if position != None:
        hands = filter(lambda hand: hand.position == position, hands)
        logging.debug('{} hands played on {}'.format(len(hands), position))

    return hands
