#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import poker_stats.hand_parser as hand_parser
import poker_stats.report as report

app = Flask(__name__)
hands = hand_parser.parse_files(['./session'])

@app.route('/api/0.1/position_report/<player_name>/<position>', methods=['GET'])
def api_position_report(player_name, position):
    rep = report.create_position_report(hands, player_name, position)
    return jsonify(vars(rep))

@app.route('/api/0.1/blind_report/<player_name>', methods=['GET'])
def api_blind_report(player_name):
    rep = report.create_blind_report(hands, player_name)
    rep_json = vars(rep)
    rep_json['sb_report'] = vars(rep.sb_report)
    rep_json['bb_report'] = vars(rep.bb_report)
    return jsonify(rep_json)

if __name__ == '__main__':
    app.run()