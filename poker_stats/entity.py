#!/usr/bin/env python2.7

import re

class Action:
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

    def __str__(self):
        if self.type == self.Fold:
            return 'fold'
        if self.type == self.Check:
            return 'check'
        if self.type == self.Call:
            return 'call {}'.format(self.value)
        if self.type == self.Bet:
            return 'bet {}'.format(self.value)
        if self.type == self.Raise:
            return 'raise {}'.format(self.value)
        if self.type == self.Post:
            return 'post {}'.format(self.value)
        if self.type == self.Uncalled:
            return 'uncalled bet returned {}'.format(self.value)

class Game:
    def __init__(self):
        self.site = None
        self.type = None
        self.stakes = None
        self.table_name = None
        self.table_type = None

class Player:
    def __init__(self):
        self.position = None
        self.starting_stack = None
        self.preflop = []
        self.flop = []
        self.turn = []
        self.river = []
        self.collected = 0.00

class Board:
    def __init__(self):
        self.flop = None
        self.turn = None
        self.river = None

class Hand:
    def __init__(self):
        self.lines = []
        self.id = None
        self.timestamp = None
        self.game = Game()
        self.players = {}
        self.board = Board()
        self.pot = None
        self.rake = None
