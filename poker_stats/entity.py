#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from sets import Set
from enum import Enum

class ActionType(Enum):
    Fold = 'f'
    Check = 'x'
    Call = 'c'
    CallAi = 'cai'
    Bet = 'b'
    BetAi = 'bai'
    Raise = 'r'
    RaiseAi = 'rai'
    Post = 'p'
    Uncalled = 'u'

class Action(object):
    def __init__(self, atype, avalue=0):
        self.type = atype
        self.value = avalue
        self.player = None

    def __str__(self):
        if self.type == ActionType.Fold:
            return '{} fold'.format(self.player.name)
        if self.type == ActionType.Check:
            return '{} check'.format(self.player.name)
        if self.type == ActionType.Call:
            return '{} call {}'.format(self.player.name, self.value)
        if self.type == ActionType.Bet:
            return '{} bet {}'.format(self.player.name, self.value)
        if self.type == ActionType.Raise:
            return '{} raise {}'.format(self.player.name, self.value)
        if self.type == ActionType.Post:
            return '{} post {}'.format(self.player.name, self.value)
        if self.type == ActionType.Uncalled:
            return '{} uncalled bet returned {}'.format(self.player.name, self.value)

    def voluntary(self):
        return self.type in [ActionType.Call, ActionType.CallAi, ActionType.Bet, ActionType.BetAi, ActionType.Raise, ActionType.RaiseAi]

class Game(object):
    def __init__(self):
        self.site = None
        self.type = None
        self.stakes = None
        self.table_name = None
        self.table_type = None

class Player(object):
    def __init__(self):
        self.name = None
        self.position = None
        self.starting_stack = None
        self.collected = 0.00

class Board(object):
    def __init__(self):
        self.flop = None
        self.turn = None
        self.river = None

class Hand(object):
    def __init__(self):
        self.lines = []
        self.id = None
        self.timestamp = None
        self.game = Game()
        self.players = {}
        self.board = Board()
        self.pot = None
        self.rake = None
        self.preflop = []
        self.flop = []
        self.turn = []
        self.river = []

    def preflop_vpip_player_count(self):
        return len(Set([a.player.name for a in self.preflop if a.voluntary()]))

    def flop_player_count(self):
        return len(Set([a.player.name for a in self.flop]))

    def preflop_actions(self, player_name):
        return [a for a in self.preflop if a.player.name == player_name]

    def flop_actions(self, player_name):
        return [a for a in self.flop if a.player.name == player_name]

    def turn_actions(self, player_name):
        return [a for a in self.turn if a.player.name == player_name]

    def river_actions(self, player_name):
        return [a for a in self.river if a.player.name == player_name]

    def profit_for_player(self, player_name):
        def invested(acc, action):
            if action.type in [ActionType.Raise, ActionType.RaiseAi]:
                return action.value
            elif action.type == ActionType.Uncalled:
                return acc - action.value
            else:
                return acc + action.value

        return self.players[player_name].collected \
                - reduce(invested, self.preflop_actions(player_name), 0) \
                - reduce(invested, self.flop_actions(player_name), 0) \
                - reduce(invested, self.turn_actions(player_name), 0) \
                - reduce(invested, self.river_actions(player_name), 0)

def profit_for_player(hands, player_name):
    return round(reduce(lambda acc, h: acc + h.profit_for_player(player_name), hands, 0), 2)

def is_call_preflop(hand, player_name):
    for action in hand.preflop:
        if action.voluntary() and action.player.name == player_name:
            return action.type in [ActionType.Call, ActionType.CallAi]

    return False

def is_raise_preflop(hand, player_name):
    for action in hand.preflop:
        if action.voluntary() and action.player.name == player_name:
            return action.type in [ActionType.Raise, ActionType.RaiseAi]

    return False

def is_3bet_preflop(hand, player_name):
    villain_raised = False

    for action in hand.preflop:
        if action.type not in [ActionType.Raise, ActionType.RaiseAi]:
            continue
        if villain_raised:
            return action.player.name == player_name
        if not villain_raised and action.player.name != player_name:
            villain_raised = True

    return False
