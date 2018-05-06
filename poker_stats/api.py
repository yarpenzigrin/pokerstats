#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import flask
from . import hand_filter
from . import hand_parser
from . import report

all_hands = hand_parser.parse_files(['./session'])
app = flask.Flask(__name__)

@app.route('/api/0.3/position_report/<player_name>', methods=['GET'])
def api_position_report(player_name):
    hands = hand_filter.apply_filters(all_hands, hand_filter.create({}, player_name))
    result = {}
    for position in ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']:
        rep = report.create_position_report(hands, player_name, position)
        result[position] = vars(rep.profit_report)
    result['ALL'] = vars(report.create_profit_report(hands, player_name))

    return flask.jsonify(result)

@app.route('/api/0.3/position_report/<player_name>/<position>', methods=['GET'])
def api_position_detail_report(player_name, position):
    hands = hand_filter.apply_filters(all_hands, hand_filter.create({}, player_name))
    rep = report.create_position_report(hands, player_name, position)
    rep_json = vars(rep)
    rep_json['profit_report'] = vars(rep.profit_report)
    return flask.jsonify(rep_json)

@app.route('/api/0.3/blind_report/<player_name>', methods=['GET'])
def api_blind_report(player_name):
    hands = hand_filter.apply_filters(all_hands, hand_filter.create({}, player_name))
    rep = report.create_blind_report(hands, player_name)
    rep_json = vars(rep)
    rep_json['sb_report'] = vars(rep.sb_report.profit_report)
    rep_json['bb_report'] = vars(rep.bb_report.profit_report)
    return flask.jsonify(rep_json)

@app.route('/api/0.3/holding_report/<player_name>', methods=['GET'])
def api_preflop_report(player_name):
    hands = hand_filter.apply_filters(all_hands, hand_filter.create({}, player_name))
    rep = report.create_holding_report(hands, player_name)
    rep_json = vars(rep)
    rep_json['stats'] = [vars(o) for o in rep.stats]
    return flask.jsonify(rep_json)

if __name__ == '__main__':
    app.run()
