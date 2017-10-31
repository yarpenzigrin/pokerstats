#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isdir, join
import re
from poker_stats.entity import Action, ActionType, Hand, Player # pylint: disable=no-name-in-module

class Parser(object): # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.amt_re = r'\$(\d+(.\d+)?)'
        self.player_re = r'(\S+(\s+\S+)*)'

        # Example:
        # PokerStars Hand #1:  Hold'em No Limit ($0.05/$0.10) - 2017/08/07 23:12:54 CCT [2017/08/07 11:12:54 ET]
        self.game_info_re = re.compile(r'(\w+) Hand #(\d+):\s+(\w.+)\s\(%s/%s\).*\[(.*)\]' \
            % (self.amt_re, self.amt_re))

        # Example:
        # Table 'Aludra' 6-max Seat #1 is the button
        self.table_info_re = re.compile(r'Table \'(.*)\' (\S+)')

        # Example:
        # Seat 1: PLAYER_BTN ($21.05 in chips)
        self.player_info_re = re.compile(r'Seat (\d+): %s \(%s' % (self.player_re, self.amt_re))

        self.table_type_to_player_count = {'6-max': 6, '9-max': 9, '10-max': 10, 'heads-up': 2}
        self.seat_to_position = {'1':'BTN', '2':'SB', '3':'BB', '4':'UTG', '5':'MP', '6':'CO'}

        # Example:
        # Dealt to PLAYER_CO [Ah Ac]
        self.dealt_re = re.compile(r'Dealt to %s \[(.*)\]' % self.player_re)
        self.flop_re = re.compile(r'\*\*\* FLOP \*\*\*\s+\[(.*)\]')
        self.turn_re = re.compile(r'\*\*\* TURN \*\*\*\s+\[.*\]\s+\[(.*)\]')
        self.river_re = re.compile(r'\*\*\* RIVER \*\*\*\s+\[.*\]\s+\[(.*)\]')
        self.pot_re = re.compile(r'Total pot %s \| Rake %s' % (self.amt_re, self.amt_re))

        # Example:
        # PLAYER_SB: posts small blind $0.05
        self.post_re = re.compile(r'%s: posts (small|big) blind %s' % (self.player_re, self.amt_re))
        self.fold_re = re.compile(r'{}: folds'.format(self.player_re))
        self.check_re = re.compile(r'{}: checks'.format(self.player_re))
        self.call_ai_re = re.compile(r'{}: calls \$(\d+(.\d+)?) and is all-in'.format(self.player_re))
        self.call_re = re.compile(r'{}: calls \$(\d+(.\d+)?)'.format(self.player_re))
        self.bet_ai_re = re.compile(r'{}: bets \$(\d+(.\d+)?) and is all-in'.format(self.player_re))
        self.bet_re = re.compile(r'{}: bets \$(\d+(.\d+)?)'.format(self.player_re))
        self.raise_ai_re = re.compile(r'{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?) and is all-in'.format(self.player_re))
        self.raise_re = re.compile(r'{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(self.player_re))
        self.uncalled_re = re.compile(r'Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(self.player_re))
        self.collected_re = re.compile(r'%s collected %s from pot' % (self.player_re, self.amt_re))

    def parse_game_info(self, hand):
        m_res = re.match(self.game_info_re, hand.lines[0].lstrip('\xef\xbb\xbf'))
        if m_res != None:
            hand.id = m_res.groups()[1]
            hand.stakes = (float(m_res.groups()[3]), float(m_res.groups()[5]))

    def parse_table_info(self, hand):
        m_res = re.match(self.table_info_re, hand.lines[1])
        if m_res != None:
            # currently not used
            pass

    def parse_player_info(self, hand):
        idx = 2
        for idx in xrange(2, 2 + 6):
            m_res = re.match(self.player_info_re, hand.lines[idx])
            if m_res != None:
                player = Player()
                player.name = m_res.groups()[1].decode('utf-8')
                player.position = self.seat_to_position[m_res.groups()[0]]
                hand.players[m_res.groups()[1]] = player
        return idx + 1

    def parse_blind_posts(self, hand, idx):
        m_res = re.match(self.post_re, hand.lines[idx])
        if m_res != None:
            action = Action(ActionType.Post, float(m_res.groups()[3]))
            action.player = hand.players[m_res.groups()[0]]
            hand.preflop.append(action)

    def parse_action(self, hand, idx, inserter): # pylint: disable=too-many-locals
        fold_mod = lambda match: inserter(hand, match[0], Action(ActionType.Fold))
        check_mod = lambda match: inserter(hand, match[0], Action(ActionType.Check))
        call_ai_mod = lambda match: inserter(hand, match[0], Action(ActionType.CallAi, float(match[2])))
        call_mod = lambda match: inserter(hand, match[0], Action(ActionType.Call, float(match[2])))
        bet_ai_mod = lambda match: inserter(hand, match[0], Action(ActionType.BetAi, float(match[2])))
        bet_mod = lambda match: inserter(hand, match[0], Action(ActionType.Bet, float(match[2])))
        raise_ai_mod = lambda match: inserter(hand, match[0], Action(ActionType.RaiseAi, float(match[4])))
        raise_mod = lambda match: inserter(hand, match[0], Action(ActionType.Raise, float(match[4])))
        uncalled_mod = lambda match: inserter(hand, match[2], Action(ActionType.Uncalled, float(match[0])))
        collected_mod = lambda match: setattr(hand.players[match[0]], 'collected', float(match[2]))

        def match_and_return_index(idx, hand, pattern, modifier):
            m_res = re.match(pattern, hand.lines[idx])
            if m_res != None:
                modifier(m_res.groups())
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
            idx = match_and_return_index(idx, hand, self.call_ai_re, call_ai_mod)
            idx = match_and_return_index(idx, hand, self.call_re, call_mod)
            idx = match_and_return_index(idx, hand, self.bet_ai_re, bet_ai_mod)
            idx = match_and_return_index(idx, hand, self.bet_re, bet_mod)
            idx = match_and_return_index(idx, hand, self.raise_ai_re, raise_ai_mod)
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
        m_res = re.match(self.dealt_re, hand.lines[idx])
        while m_res is not None:
            hand.players[m_res.groups()[0]].holding = m_res.groups()[2]
            idx += 1
            m_res = re.match(self.dealt_re, hand.lines[idx])

        def insert_action(hand, player, action):
            action.player = hand.players[player]
            hand.preflop.append(action)

        return self.parse_action(hand, idx, insert_action)

    def parse_flop_action(self, hand, idx):
        m_res = re.match(self.flop_re, hand.lines[idx])
        if m_res is None:
            return idx

        def insert_action(hand, player, action):
            action.player = hand.players[player]
            hand.flop.append(action)

        return self.parse_action(hand, idx + 1, insert_action)

    def parse_turn_action(self, hand, idx):
        m_res = re.match(self.turn_re, hand.lines[idx])
        if m_res is None:
            return idx

        def insert_action(hand, player, action):
            action.player = hand.players[player]
            hand.turn.append(action)

        return self.parse_action(hand, idx + 1, insert_action)

    def parse_river_action(self, hand, idx):
        m_res = re.match(self.river_re, hand.lines[idx])
        if m_res is None:
            return idx

        def insert_action(hand, player, action):
            action.player = hand.players[player]
            hand.river.append(action)

        return self.parse_action(hand, idx + 1, insert_action)

    def parse_summary(self, hand, idx):
        for i in xrange(idx, len(hand.lines)):
            if '*** SUMMARY ***' in hand.lines[i]:
                m_res = re.match(self.pot_re, hand.lines[i+1])
                if m_res != None:
                    hand.pot = float(m_res.groups()[0])
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

    def parse_file_contents(self, lines, store_lines):
        result = []
        hand_in_process = False
        for line in lines:
            if line.strip():
                if not hand_in_process:
                    hand = Hand()
                    hand_in_process = True

                hand.lines.append(line)
            else:
                if hand_in_process:
                    hand.lines[0] = hand.lines[0].replace('PokerStars Zoom Hand', 'PokerStars Hand')
                    hand.lines.append('\r\n')
                    hand.lines.append('\r\n')
                    hand.lines.append('\r\n')
                    self.parse_hand(hand)
                    if hand.pot != None:
                        if not store_lines:
                            hand.lines = None
                        result.append(hand)
                    hand_in_process = False

        return result

def parse_files(file_names, store_lines=False):
    hands = []
    parser = Parser()

    for file_name in file_names:
        if isdir(file_name):
            files_in_dir = [join(file_name, f) for f in listdir(file_name)]
            hands.extend(parse_files(files_in_dir, store_lines))
        else:
            with open(file_name, 'r') as file_desc:
                lines = file_desc.readlines()
            hands.extend(parser.parse_file_contents(lines, store_lines))

    return hands
