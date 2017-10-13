#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from poker_stats.entity import Action, Player, Hand
import re

class Parser:
    def __init__(self):
        self.amt_re = '\$(\d+(.\d+)?)'
        self.player_re = '(\S+(\s+\S+)*)'

        # Example:
        # PokerStars Hand #1:  Hold'em No Limit ($0.05/$0.10) - 2017/08/07 23:12:54 CCT [2017/08/07 11:12:54 ET]
        self.game_info_re = re.compile('(\w+) Hand #(\d+):\s+(\w.+)\s\(%s/%s\).*\[(.*)\]' \
            % (self.amt_re, self.amt_re))

        # Example:
        # Table 'Aludra' 6-max Seat #1 is the button
        self.table_info_re = re.compile('Table \'(.*)\' (\S+)')

        # Example:
        # Seat 1: PLAYER_BTN ($21.05 in chips)
        self.player_info_re = re.compile('Seat (\d+): %s \(%s' % (self.player_re, self.amt_re))

        self.table_type_to_player_count = { '6-max': 6, '9-max': 9, '10-max': 10, 'heads-up': 2 }
        self.seat_to_position = { '1':'BTN', '2':'SB', '3':'BB', '4':'UTG', '5':'MP', '6':'CO' }

        # Example:
        # Dealt to PLAYER_CO [Ah Ac]
        self.dealt_re = re.compile('Dealt to %s \[(.*)\]' % self.player_re)
        self.flop_re = re.compile('\*\*\* FLOP \*\*\*\s+\[(.*)\]')
        self.turn_re = re.compile('\*\*\* TURN \*\*\*\s+\[.*\]\s+\[(.*)\]')
        self.river_re = re.compile('\*\*\* RIVER \*\*\*\s+\[.*\]\s+\[(.*)\]')
        self.pot_re = re.compile('Total pot %s \| Rake %s' % (self.amt_re, self.amt_re))

        # Example:
        # PLAYER_SB: posts small blind $0.05
        self.post_re = re.compile('%s: posts (small|big) blind %s' % (self.player_re, self.amt_re))
        self.fold_re = re.compile('{}: folds'.format(self.player_re))
        self.check_re = re.compile('{}: checks'.format(self.player_re))
        self.call_re = re.compile('{}: calls \$(\d+(.\d+)?)'.format(self.player_re))
        self.bet_re = re.compile('{}: bets \$(\d+(.\d+)?)'.format(self.player_re))
        self.raise_re = re.compile( \
            '{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(self.player_re))
        self.uncalled_re = re.compile( \
            'Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(self.player_re))
        self.collected_re = re.compile( \
            '%s collected %s from pot' % (self.player_re, self.amt_re))

    def parse_game_info(self, hand):
        m = re.match(self.game_info_re, hand.lines[0])
        if m != None:
            hand.game.site = m.groups()[0]
            hand.id = m.groups()[1]
            hand.game.type = m.groups()[2]
            hand.game.stakes = ( float(m.groups()[3]), float(m.groups()[5]) )
            hand.timestamp = m.groups()[7]

    def parse_table_info(self, hand):
        m = re.match(self.table_info_re, hand.lines[1])
        if m != None:
            hand.game.table_name = m.groups()[0]
            hand.game.table_type = m.groups()[1]

    def parse_player_info(self, hand):
        for idx in xrange(2, 2 + self.table_type_to_player_count[hand.game.table_type]):
            m = re.match(self.player_info_re, hand.lines[idx])
            if m != None:
                player = Player()
                player.name = m.groups()[1]
                player.position = self.seat_to_position[m.groups()[0]]
                player.starting_stack = float(m.groups()[3])
                hand.players[m.groups()[1]] = player
        return idx + 1

    def parse_blind_posts(self, hand, idx):
        m = re.match(self.post_re, hand.lines[idx])
        if m != None:
            action = Action(Action.Post, float(m.groups()[3]))
            action.player = hand.players[m.groups()[0]]
            hand.players[m.groups()[0]].preflop.append(action)

    def parse_action(self, hand, idx, inserter):
        fold_mod = lambda match: inserter(hand, match[0], Action(Action.Fold, 0))
        check_mod = lambda match: inserter(hand, match[0], Action(Action.Check, 0))
        call_mod = lambda match: inserter(hand, match[0], Action(Action.Call, float(match[2])))
        bet_mod = lambda match: inserter(hand, match[0], Action(Action.Bet, float(match[2])))
        raise_mod = lambda match: inserter(hand, match[0], Action(Action.Raise, float(match[4])))
        uncalled_mod = lambda match: inserter(hand, match[2], Action(Action.Uncalled, float(match[0])))
        collected_mod = lambda match: setattr(hand.players[match[0]], 'collected', float(match[2]))

        def match_and_return_index(idx, hand, pattern, modifier):
            m = re.match(pattern, hand.lines[idx])
            if m != None:
                modifier(m.groups())
                return idx + 1
            return idx

        def ignore_line(idx, line):
            if 'has timed out' in line or \
                'is disconnected' in line or \
                '*** SHOW DOWN ***' in line or \
                ' shows [' in line or \
                ' mucks hand' in line:
                return idx + 1
            return idx

        while True:
            old_idx = idx
            idx = match_and_return_index(idx, hand, self.fold_re, fold_mod)
            idx = match_and_return_index(idx, hand, self.check_re, check_mod)
            idx = match_and_return_index(idx, hand, self.call_re, call_mod)
            idx = match_and_return_index(idx, hand, self.bet_re, bet_mod)
            idx = match_and_return_index(idx, hand, self.raise_re, raise_mod)
            idx = match_and_return_index(idx, hand, self.uncalled_re, uncalled_mod)
            idx = match_and_return_index(idx, hand, self.collected_re, collected_mod)
            idx = ignore_line(idx, hand.lines[idx])
            if old_idx == idx:
                break
        return idx

    def parse_preflop_action(self, hand, idx):
        if '*** HOLE CARDS ***' not in hand.lines[idx]:
            return idx
        idx += 1
        m = re.match(self.dealt_re, hand.lines[idx])
        while m != None:
            hand.players[m.groups()[0]].holding = m.groups()[2]
            idx += 1
            m = re.match(self.dealt_re, hand.lines[idx])

        def insert_action(hand, player, action):
            hand.players[player].preflop.append(action)
            action.player = hand.players[player]
            hand.preflop.append(action)

        return self.parse_action(hand, idx, insert_action)

    def parse_flop_action(self, hand, idx):
        m = re.match(self.flop_re, hand.lines[idx])
        if m == None:
            return idx
        hand.board.flop = m.groups()[0]

        def insert_action(hand, player, action):
            hand.players[player].flop.append(action)
            action.player = hand.players[player]
            hand.flop.append(action)

        return self.parse_action(hand, idx + 1, insert_action)

    def parse_turn_action(self, hand, idx):
        m = re.match(self.turn_re, hand.lines[idx])
        if m == None:
            return idx
        hand.board.turn = m.groups()[0]

        def insert_action(hand, player, action):
            hand.players[player].turn.append(action)
            action.player = hand.players[player]
            hand.turn.append(action)

        return self.parse_action(hand, idx + 1, insert_action)

    def parse_river_action(self, hand, idx):
        m = re.match(self.river_re, hand.lines[idx])
        if m == None:
            return idx
        hand.board.river = m.groups()[0]

        def insert_action(hand, player, action):
            hand.players[player].river.append(action)
            action.player = hand.players[player]
            hand.river.append(action)

        return self.parse_action(hand, idx + 1, insert_action)

    def parse_summary(self, hand, idx):
        for i in xrange(idx, len(hand.lines)):
            if '*** SUMMARY ***' in hand.lines[i]:
                m = re.match(self.pot_re, hand.lines[i+1])
                if m != None:
                    hand.pot = float(m.groups()[0])
                    hand.rake = float(m.groups()[2])
                break

    def parse_hand(self, hand):
        self.parse_game_info(hand)
        self.parse_table_info(hand)
        idx = self.parse_player_info(hand)
        self.parse_blind_posts(hand, idx)
        self.parse_blind_posts(hand, idx+1)
        idx = self.parse_preflop_action(hand, idx+2)
        idx = self.parse_flop_action(hand, idx)
        idx = self.parse_turn_action(hand, idx)
        idx = self.parse_river_action(hand, idx)
        self.parse_summary(hand, idx)

    def parse_file_contents(self, lines):
        result = []
        hand_in_process = False
        for line in lines:
            if line == '\r\n' or line == '\n':
                if hand_in_process:
                    hand.lines[0].replace('PokerStars Zoom Hand', 'PokerStars Hand')
                    hand.lines.append('\r\n')
                    hand.lines.append('\r\n')
                    hand.lines.append('\r\n')
                    self.parse_hand(hand)
                    if hand.pot != None:
                        result.append(hand)
                    hand_in_process = False
            else:
                if not hand_in_process:
                    hand = Hand()
                    hand_in_process = True

                hand.lines.append(line)

        return result

def parse_files(file_names):
    hands = []
    parser = Parser()

    for fn in file_names:
        with open(fn, 'r') as f:
            lines = f.readlines()
        hands.extend(parser.parse_file_contents(lines))

    return hands
