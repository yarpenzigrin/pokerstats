#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from os.path import dirname, realpath
from sys import path
from unittest import main, TestCase

test_dir = dirname(realpath(__file__))
path.append(test_dir + '/../..')

from poker_stats.entity import *

def actions(*action_list):
    result = []
    for act in action_list:
        player = Player()
        player.name = act[0]
        action = Action(act[1])
        action.player = player
        result.append(action)
    return result

hero = 'HERO'
villain = 'VILLAIN'
villain1 = 'VILLAIN1'
villain2 = 'VILLAIN2'
villain3 = 'VILLAIN3'

class Test_is_call_preflop(TestCase):
    def test_no_actions(self):
        acts = actions()
        self.assertFalse(is_call_preflop(acts, hero))

    def test_open_raise(self):
        acts = actions((villain, ActionType.Post), (hero, ActionType.Raise))
        self.assertFalse(is_call_preflop(acts, hero))

    def test_fold(self):
        acts = actions((villain, ActionType.Raise), (hero, ActionType.Fold))
        self.assertFalse(is_call_preflop(acts, hero))

    def test_freeplay(self):
        acts = actions((hero, ActionType.Post), (villain, ActionType.Call), (hero, ActionType.Check))
        self.assertFalse(is_call_preflop(acts, hero))

    def test_call_a_raise(self):
        acts = actions((villain, ActionType.Raise), (hero, ActionType.Call))
        self.assertTrue(is_call_preflop(acts, hero))

    def test_call_fold(self):
        acts = actions((hero, ActionType.Call), (villain, ActionType.Raise), (hero, ActionType.Call))
        self.assertTrue(is_call_preflop(acts, hero))

    def test_call_ai(self):
        acts = actions((villain, ActionType.Raise), (hero, ActionType.CallAi))
        self.assertTrue(is_call_preflop(acts, hero))

    def test_limp_reraise_ai(self):
        acts = actions((villain1, ActionType.Post), (hero, ActionType.Call), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Fold), (hero, ActionType.RaiseAi))
        self.assertTrue(is_call_preflop(acts, hero))

class Test_is_raise_preflop(TestCase):
    def test_no_actions(self):
        acts = actions()
        self.assertFalse(is_raise_preflop(acts, hero))

    def test_call_reraise_ai(self):
        acts = actions((villain1, ActionType.Raise), (hero, ActionType.Call), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Call), (hero, ActionType.RaiseAi))
        self.assertFalse(is_raise_preflop(acts, hero))

    def test_limp_reraise_ai(self):
        acts = actions((villain1, ActionType.Post), (hero, ActionType.Call), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Fold), (hero, ActionType.RaiseAi))
        self.assertFalse(is_raise_preflop(acts, hero))

    def test_open_raise(self):
        acts = actions((villain, ActionType.Post), (hero, ActionType.Raise))
        self.assertTrue(is_raise_preflop(acts, hero))

    def test_blind_3bet(self):
        acts = actions((hero, ActionType.Post), (villain, ActionType.Raise), (hero, ActionType.Raise))
        self.assertTrue(is_raise_preflop(acts, hero))

    def test_blind_cold_4bet(self):
        acts = actions((hero, ActionType.Post), (villain1, ActionType.Raise), (villain2, ActionType.Raise),\
                               (hero, ActionType.Raise))
        self.assertTrue(is_raise_preflop(acts, hero))

class Test_is_3bet_preflop(TestCase):
    def test_no_actions(self):
        acts = actions()
        self.assertFalse(is_3bet_preflop(acts, hero))

    def test_open_raise(self):
        acts = actions((villain, ActionType.Post), (hero, ActionType.Raise))
        self.assertFalse(is_3bet_preflop(acts, hero))

    def test_isolate_limper(self):
        acts = actions((villain1, ActionType.Post), (villain2, ActionType.Call), (hero, ActionType.Raise))
        self.assertFalse(is_3bet_preflop(acts, hero))

    def test_call_reraise_ai(self):
        acts = actions((villain1, ActionType.Raise), (hero, ActionType.Call), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Call), (hero, ActionType.RaiseAi))
        self.assertFalse(is_3bet_preflop(acts, hero))

    def test_limp_reraise_ai(self):
        acts = actions((villain1, ActionType.Post), (hero, ActionType.Call), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Fold), (hero, ActionType.RaiseAi))
        self.assertFalse(is_3bet_preflop(acts, hero))

    def test_4bet(self):
        acts = actions((villain1, ActionType.Post), (hero, ActionType.Raise), (villain2, ActionType.Raise),\
                       (hero, ActionType.Raise))
        self.assertFalse(is_3bet_preflop(acts, hero))

    def test_squeeze(self):
        acts = actions((villain1, ActionType.Post), (villain2, ActionType.Raise), (villain3, ActionType.Call),\
                       (hero, ActionType.Raise))
        self.assertTrue(is_3bet_preflop(acts, hero))

    def test_sb_3bet(self):
        acts = actions((hero, ActionType.Post), (villain1, ActionType.Post), (villain2, ActionType.Raise),\
                       (hero, ActionType.Raise), (villain1, ActionType.Fold), (villain2, ActionType.Fold))
        self.assertTrue(is_3bet_preflop(acts, hero))

    def test_bb_3bet_ai(self):
        acts = actions((villain1, ActionType.Post), (hero, ActionType.Post), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Fold), (hero, ActionType.RaiseAi), (villain2, ActionType.Call))
        self.assertTrue(is_3bet_preflop(acts, hero))

    def test_5bet_shove(self):
        acts = actions((villain, ActionType.Raise), (hero, ActionType.Raise), (villain, ActionType.Raise),\
                       (hero, ActionType.RaiseAi), (villain, ActionType.Fold))
        self.assertTrue(is_3bet_preflop(acts, hero))

class Test_is_4bet_preflop(TestCase):
    def test_no_actions(self):
        acts = actions()
        self.assertFalse(is_4bet_preflop(acts, hero))

    def test_open_raise(self):
        acts = actions((villain, ActionType.Post), (hero, ActionType.Raise))
        self.assertFalse(is_4bet_preflop(acts, hero))

    def test_5bet_shove(self):
        acts = actions((villain, ActionType.Raise), (hero, ActionType.Raise), (villain, ActionType.Raise),\
                       (hero, ActionType.RaiseAi), (villain, ActionType.Fold))
        self.assertFalse(is_4bet_preflop(acts, hero))

    def test_4bet(self):
        acts = actions((villain1, ActionType.Post), (hero, ActionType.Raise), (villain2, ActionType.Raise),\
                       (villain1, ActionType.Fold), (hero, ActionType.Raise))
        self.assertTrue(is_4bet_preflop(acts, hero))

    def test_cold_4bet(self):
        acts = actions((villain1, ActionType.Post), (villain2, ActionType.Raise), (villain3, ActionType.Raise),\
                       (hero, ActionType.Raise))
        self.assertTrue(is_4bet_preflop(acts, hero))

    def test_bb_4bet_villain_limp_reraises(self):
        acts = actions((villain, ActionType.Post), (hero, ActionType.Post), (villain, ActionType.Call),\
                       (hero, ActionType.Raise), (villain, ActionType.Raise), (hero, ActionType.Raise))
        self.assertTrue(is_4bet_preflop(acts, hero))

if __name__ == '__main__':
    main()
