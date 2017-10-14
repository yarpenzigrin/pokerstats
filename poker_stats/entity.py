#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from sets import Set

class Action(object):
    Fold = 'f'
    Check = 'x'
    Call = 'c'
    Bet = 'b'
    Raise = 'r'
    Post = 'p'
    Uncalled = 'u'

    def __init__(self, atype, avalue):
        self.type = atype
        self.value = avalue
        self.player = None

    def __str__(self):
        if self.type == self.Fold:
            return '{} fold'.format(self.player.name)
        if self.type == self.Check:
            return '{} check'.format(self.player.name)
        if self.type == self.Call:
            return '{} call {}'.format(self.player.name, self.value)
        if self.type == self.Bet:
            return '{} bet {}'.format(self.player.name, self.value)
        if self.type == self.Raise:
            return '{} raise {}'.format(self.player.name, self.value)
        if self.type == self.Post:
            return '{} post {}'.format(self.player.name, self.value)
        if self.type == self.Uncalled:
            return '{} uncalled bet returned {}'.format(self.player.name, self.value)

    def voluntary(self):
        return self.type in [self.Call, self.Bet, self.Raise]

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
        self.preflop = []
        self.flop = []
        self.turn = []
        self.river = []
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
        return len(Set([a.player for a in self.preflop if a.voluntary()]))

    def flop_player_count(self):
        return len(Set([a.player for a in self.flop]))
