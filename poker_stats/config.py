#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import logging

def parse_args():
    parser = argparse.ArgumentParser()
    action_parser = parser.add_subparsers(help='Available actions', dest='action')

    dump_parser = action_parser.add_parser('dump', help='Dump hands')
    dump_parser.add_argument('-p', '--player', help='Player')
    dump_parser.add_argument('-f', '--position', help='Position', choices=['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN'])
    dump_parser.add_argument('-v', '--voluntary', action='store_true', help='Voluntarily enter the pot')
    dump_parser.add_argument('-s', '--sort', action='store_true', help='Sort the dump by the size of the pot')
    dump_parser.add_argument('files', help='File list', nargs='+')

    report_parser = action_parser.add_parser('report', help='Print hand report for a player')
    report_parser.add_argument('-p', '--player', help='Player', required=True)
    report_parser.add_argument('-f', '--position', help='Position', choices=['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN'])
    report_parser.add_argument('-v', '--voluntary', action='store_true', help='Voluntarily enter the pot')
    report_parser.add_argument('files', help='File list', nargs='+')

    return parser.parse_args()

args = parse_args()
logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')
