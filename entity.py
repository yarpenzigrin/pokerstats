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

class Hand:
    def __init__(self):
        self.lines = []
        self.position = None
        self.preflop = []
        self.collected = 0
        self.pot = 0

    def parse(self, player):
        self.position = self.getPlayerPosition(player)
        self.pot = self.getTotalPot(player)
        self.collected = self.getCollectedFromPot(player)
        self.preflop = self.getPlayerPreflopActions(player)
        self.flop = self.getPlayerFlopActions(player)
        self.turn = self.getPlayerTurnActions(player)
        self.river = self.getPlayerRiverActions(player)

    def getPlayerPosition(self, player):
        result = None
        positionMap = { None:None, '1':'BTN', '2':'SB', '3':'BB', '4':'UTG', '5':'MP', '6':'CO' }

        r = re.compile('Seat (\d): {} \(\$'.format(player))
        for l in self.lines:
            m = re.match(r, l)
            if m != None:
                result = m.groups()[0]
                break

        return positionMap[result]

    def getPlayerPreflopActions(self, player):
        result = []

        foldRe = re.compile('{}: folds'.format(player))
        checkRe = re.compile('{}: checks'.format(player))
        callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
        betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
        postRe = re.compile('{}: posts (small|big) blind \$(\d+(.\d+)?)'.format(player))
        raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
        uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

        preflop = False
        for l in self.lines:
            line = l.rstrip()

            m = re.match(postRe, line)
            if m != None:
                result.append(Action(Action.Post, float(m.groups()[1])))

            if not preflop:
                if '*** HOLE CARDS ***' in line:
                    preflop = True
                else:
                    continue

            if preflop and ('*** SUMMARY ***' in line or '*** FLOP ***' in line):
                break

            m = re.match(foldRe, line)
            if m != None:
                result.append(Action(Action.Fold, 0))

            m = re.match(checkRe, line)
            if m != None:
                result.append(Action(Action.Check, 0))

            m = re.match(callRe, line)
            if m != None:
                result.append(Action(Action.Call, float(m.groups()[0])))

            m = re.match(betRe, line)
            if m != None:
                result.append(Action(Action.Bet, float(m.groups()[0])))

            m = re.match(raiseRe, line)
            if m != None:
                result.append(Action(Action.Raise, float(m.groups()[2])))

            m = re.match(uncalledRe, line)
            if m != None:
                result.append(Action(Action.Uncalled, -float(m.groups()[0])))

        return result

    def getPlayerFlopActions(self, player):
        result = []

        foldRe = re.compile('{}: folds'.format(player))
        checkRe = re.compile('{}: checks'.format(player))
        callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
        betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
        raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
        uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

        flop = False
        for l in self.lines:
            line = l.rstrip()

            if not flop:
                if '*** FLOP ***' in line:
                    flop = True
                else:
                    continue

            if flop and ('*** SUMMARY ***' in line or '*** TURN ***' in line):
                break

            m = re.match(foldRe, line)
            if m != None:
                result.append(Action(Action.Fold, 0))

            m = re.match(checkRe, line)
            if m != None:
                result.append(Action(Action.Check, 0))

            m = re.match(callRe, line)
            if m != None:
                result.append(Action(Action.Call, float(m.groups()[0])))

            m = re.match(betRe, line)
            if m != None:
                result.append(Action(Action.Bet, float(m.groups()[0])))

            m = re.match(raiseRe, line)
            if m != None:
                result.append(Action(Action.Raise, float(m.groups()[2])))

            m = re.match(uncalledRe, line)
            if m != None:
                result.append(Action(Action.Uncalled, -float(m.groups()[0])))

        return result

    def getPlayerTurnActions(self, player):
        result = []

        foldRe = re.compile('{}: folds'.format(player))
        checkRe = re.compile('{}: checks'.format(player))
        callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
        betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
        raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
        uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

        turn = False
        for l in self.lines:
            line = l.rstrip()

            if not turn:
                if '*** TURN ***' in line:
                    turn = True
                else:
                    continue

            if turn and ('*** SUMMARY ***' in line or '*** RIVER ***' in line):
                break

            m = re.match(foldRe, line)
            if m != None:
                result.append(Action(Action.Fold, 0))

            m = re.match(checkRe, line)
            if m != None:
                result.append(Action(Action.Check, 0))

            m = re.match(callRe, line)
            if m != None:
                result.append(Action(Action.Call, float(m.groups()[0])))

            m = re.match(betRe, line)
            if m != None:
                result.append(Action(Action.Bet, float(m.groups()[0])))

            m = re.match(raiseRe, line)
            if m != None:
                result.append(Action(Action.Raise, float(m.groups()[2])))

            m = re.match(uncalledRe, line)
            if m != None:
                result.append(Action(Action.Uncalled, -float(m.groups()[0])))

        return result

    def getPlayerRiverActions(self, player):
        result = []

        foldRe = re.compile('{}: folds'.format(player))
        checkRe = re.compile('{}: checks'.format(player))
        callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(player))
        betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(player))
        raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(player))
        uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(player))

        river = False
        for l in self.lines:
            line = l.rstrip()

            if not river:
                if '*** RIVER ***' in line:
                    river = True
                else:
                    continue

            if river and ('*** SUMMARY ***' in line):
                break

            m = re.match(foldRe, line)
            if m != None:
                result.append(Action(Action.Fold, 0))

            m = re.match(checkRe, line)
            if m != None:
                result.append(Action(Action.Check, 0))

            m = re.match(callRe, line)
            if m != None:
                result.append(Action(Action.Call, float(m.groups()[0])))

            m = re.match(betRe, line)
            if m != None:
                result.append(Action(Action.Bet, float(m.groups()[0])))

            m = re.match(raiseRe, line)
            if m != None:
                result.append(Action(Action.Raise, float(m.groups()[2])))

            m = re.match(uncalledRe, line)
            if m != None:
                result.append(Action(Action.Uncalled, -float(m.groups()[0])))

        return result

    def getTotalPot(self, line):
        result = None

        r = re.compile('Total pot \$(\d+(.\d+)?) \| Rake \$(\d+(.\d+)?)')
        for l in self.lines:
            m = re.match(r, l)
            if m != None:
                result = float(m.groups()[0])
                break

        return result

    def getCollectedFromPot(self, player):
        result = 0

        collectedRe = re.compile('{} collected \$(\d+(.\d+)?) from pot'.format(player))

        for l in self.lines:
            line = l.rstrip()

            m = re.match(collectedRe, line)
            if m != None:
                result = float(m.groups()[0])
                break

        return result

    def getProfit(self):
        def invested(acc, a):
            if a.type == Action.Raise:
                return a.value
            else:
                return acc + a.value
        return self.collected - reduce(invested, self.preflop, 0) - reduce(invested, self.flop, 0) - reduce(invested, self.turn, 0) - reduce(invested, self.river, 0)
