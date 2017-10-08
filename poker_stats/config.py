#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import logging

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--dump', action='store_true', help='Dump hands')
group.add_argument('-r', '--report', action='store_true', help='Print hand report')

parser.add_argument('-p', '--player', help='Player')
parser.add_argument('-f', '--position', help='Position', choices=['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN'])
parser.add_argument('-v', '--voluntary', action='store_true', help='Voluntarily enter the pot')

parser.add_argument('-s', '--sort', action='store_true', help='Sort the dump by the size of the pot')
parser.add_argument('files', help='File list', nargs='+')

args = parser.parse_args()
del parser

logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')
