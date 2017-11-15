#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from enum import Enum

class ActionType(Enum): # pylint: disable=too-few-public-methods
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

class Action(object): # pylint: disable=too-few-public-methods
    def __init__(self, atype, avalue=0):
        self.type = atype
        self.value = avalue
        self.player = None

    def is_call(self):
        return self.type in [ActionType.Call, ActionType.CallAi]

    def is_raise(self):
        return self.type in [ActionType.Raise, ActionType.RaiseAi]

    def is_voluntary(self):
        return self.type in [ActionType.Call, ActionType.CallAi, ActionType.Bet, ActionType.BetAi,\
                             ActionType.Raise, ActionType.RaiseAi]

class Player(object): # pylint: disable=too-few-public-methods
    def __init__(self):
        self.name = None
        self.position = None
        self.collected = 0.00

class Hand(object): # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.id = None
        self.lines = []
        self.players = {}
        self.pot = None
        self.stakes = None
        self.preflop = []
        self.flop = []
        self.turn = []
        self.river = []

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
            if action.is_raise():
                return action.value
            elif action.type == ActionType.Uncalled:
                return acc - action.value
            return acc + action.value

        return self.players[player_name].collected \
                - reduce(invested, self.preflop_actions(player_name), 0) \
                - reduce(invested, self.flop_actions(player_name), 0) \
                - reduce(invested, self.turn_actions(player_name), 0) \
                - reduce(invested, self.river_actions(player_name), 0)

def profit_for_player(hands, player_name):
    return round(reduce(lambda acc, h: acc + h.profit_for_player(player_name), hands, 0), 2)

def is_call_preflop(actions, player_name):
    for action in actions:
        if action.player.name == player_name and action.is_voluntary():
            return action.is_call()
    return False

def is_raise_preflop(actions, player_name):
    for action in actions:
        if action.player.name == player_name and action.is_voluntary():
            return action.is_raise()
    return False

def is_successful_steal_preflop(actions, player_name):
    return not is_3bet_preflop(actions, player_name) and \
           [ActionType.Raise, ActionType.Uncalled] == [a.type for a in actions if a.player.name == player_name]

def is_unsuccessful_steal_preflop(actions, player_name):
    return not is_3bet_preflop(actions, player_name) and \
           [ActionType.Raise, ActionType.Fold] == [a.type for a in actions if a.player.name == player_name]

def is_3bet_preflop(actions, player_name):
    raises = [a for a in actions if a.is_raise()]
    return is_raise_preflop(actions, player_name) and len(raises) >= 2 and \
           raises[0].player.name != player_name and raises[1].player.name == player_name

def is_4bet_preflop(actions, player_name):
    raises = [a for a in actions if a.is_raise()]
    return is_raise_preflop(actions, player_name) and len(raises) >= 3 and \
          raises[2].player.name == player_name
