import re

from entity import *

amtRe = '\$(\d+(.\d+)?)'
playerRe = '(\S+(\s+\S+)*)'

def parseGameInfo(hand):
    # Example:
    # PokerStars Hand #1:  Hold'em No Limit ($0.05/$0.10) - 2017/08/07 23:12:54 CCT [2017/08/07 11:12:54 ET]
    gameInfoRe = re.compile('(\w+) Hand #(\d+):\s+(\w.+)\s\(%s/%s\).*\[(.*)\]' % (amtRe, amtRe))
    m = re.match(gameInfoRe, hand.lines[0])
    if m != None:
        hand.game.site = m.groups()[0]
        hand.id = m.groups()[1]
        hand.game.type = m.groups()[2]
        hand.game.stakes = ( float(m.groups()[3]), float(m.groups()[5]) )
        hand.timestamp = m.groups()[7]

def parseTableInfo(hand):
    # Example:
    # Table 'Aludra' 6-max Seat #1 is the button
    tableInfoRe = re.compile('Table \'(.*)\' (\S+)')
    m = re.match(tableInfoRe, hand.lines[1])
    if m != None:
        hand.game.tableName = m.groups()[0]
        hand.game.tableType = m.groups()[1]

def parsePlayerInfo(hand):
    tableTypeToPlayerCount = { '6-max': 6, '9-max': 9, '10-max': 10, 'heads-up': 2 }
    seatToPosition = { '1':'BTN', '2':'SB', '3':'BB', '4':'UTG', '5':'MP', '6':'CO' }
    # Example:
    # Seat 1: PLAYER_BTN ($21.05 in chips)
    playerInfoRe = re.compile('Seat (\d+): %s \(%s' % (playerRe, amtRe))
    for idx in xrange(2, 2 + tableTypeToPlayerCount[hand.game.tableType]):
        m = re.match(playerInfoRe, hand.lines[idx])
        if m != None:
            player = Player()
            player.position = seatToPosition[m.groups()[0]]
            player.startingStack = float(m.groups()[3])
            hand.players[m.groups()[1]] = player
    return idx + 1

def parseBlindPosts(hand, idx):
    # Example:
    # PLAYER_SB: posts small blind $0.05
    postRe = re.compile('%s: posts (small|big) blind %s' % (playerRe, amtRe))
    m = re.match(postRe, hand.lines[idx])
    if m != None:
        hand.players[m.groups()[0]].preflop.append(Action(Action.Post, float(m.groups()[3])))

def parseAction(hand, idx, inserter):
    foldRe = re.compile('{}: folds'.format(playerRe))
    checkRe = re.compile('{}: checks'.format(playerRe))
    callRe = re.compile('{}: calls \$(\d+(.\d+)?)'.format(playerRe))
    betRe = re.compile('{}: bets \$(\d+(.\d+)?)'.format(playerRe))
    raiseRe = re.compile('{}: raises \$(\d+(.\d+)?) to \$(\d+(.\d+)?)'.format(playerRe))
    uncalledRe = re.compile('Uncalled bet \(\$(\d+(.\d+)?)\) returned to {}'.format(playerRe))
    collectedRe = re.compile('%s collected %s from pot' % (playerRe, amtRe))

    foldMod = lambda match: inserter(hand, match[0], Action(Action.Fold, 0))
    checkMod = lambda match: inserter(hand, match[0], Action(Action.Check, 0))
    callMod = lambda match: inserter(hand, match[0], Action(Action.Call, float(match[2])))
    betMod = lambda match: inserter(hand, match[0], Action(Action.Bet, float(match[2])))
    raiseMod = lambda match: inserter(hand, match[0], Action(Action.Raise, float(match[4])))
    uncalledMod = lambda match: inserter(hand, match[2], Action(Action.Uncalled, float(match[0])))
    collectedMod = lambda match: setattr(hand.players[match[0]], 'collected', float(match[2]))

    def matchAndReturnIndex(idx, hand, pattern, modifier):
        m = re.match(pattern, hand.lines[idx])
        if m != None:
            modifier(m.groups())
            return idx + 1
        return idx

    while True:
        oldIdx = idx
        idx = matchAndReturnIndex(idx, hand, foldRe, foldMod)
        idx = matchAndReturnIndex(idx, hand, checkRe, checkMod)
        idx = matchAndReturnIndex(idx, hand, callRe, callMod)
        idx = matchAndReturnIndex(idx, hand, betRe, betMod)
        idx = matchAndReturnIndex(idx, hand, raiseRe, raiseMod)
        idx = matchAndReturnIndex(idx, hand, uncalledRe, uncalledMod)
        idx = matchAndReturnIndex(idx, hand, collectedRe, collectedMod)
        if 'has timed out' in hand.lines[idx] or 'is disconnected' in hand.lines[idx]:
            idx += 1
        if oldIdx == idx:
            break
    return idx

def parsePreflopAction(hand, idx):
    if '*** HOLE CARDS ***' not in hand.lines[idx]:
        return idx
    idx += 1
    # Example:
    # Dealt to PLAYER_CO [Ah Ac]
    dealtRe = re.compile('Dealt to %s \[(.*)\]' % playerRe)
    m = re.match(dealtRe, hand.lines[idx])
    while m != None:
        hand.players[m.groups()[0]].holding = m.groups()[2]
        idx += 1
        m = re.match(dealtRe, hand.lines[idx])

    def insertAction(hand, player, action):
        hand.players[player].preflop.append(action)

    return parseAction(hand, idx, insertAction)

def parseFlopAction(hand, idx):
    flopRe = re.compile('\*\*\* FLOP \*\*\*\s+\[(.*)\]')
    m = re.match(flopRe, hand.lines[idx])
    if m == None:
        return idx
    hand.board.flop = m.groups()[0]

    def insertAction(hand, player, action):
        hand.players[player].flop.append(action)

    return parseAction(hand, idx + 1, insertAction)

def parseTurnAction(hand, idx):
    turnRe = re.compile('\*\*\* TURN \*\*\*\s+\[.*\]\s+\[(.*)\]')
    m = re.match(turnRe, hand.lines[idx])
    if m == None:
        return idx
    hand.board.turn = m.groups()[0]

    def insertAction(hand, player, action):
        hand.players[player].turn.append(action)

    return parseAction(hand, idx + 1, insertAction)

def parseRiverAction(hand, idx):
    riverRe = re.compile('\*\*\* RIVER \*\*\*\s+\[.*\]\s+\[(.*)\]')
    m = re.match(riverRe, hand.lines[idx])
    if m == None:
        return idx
    hand.board.river = m.groups()[0]

    def insertAction(hand, player, action):
        hand.players[player].river.append(action)

    return parseAction(hand, idx + 1, insertAction)

def parseSummary(hand, idx):
    for i in xrange(idx, len(hand.lines)):
        if '*** SUMMARY ***' in hand.lines[i]:
            potRe = re.compile('Total pot %s \| Rake %s' % (amtRe, amtRe))
            m = re.match(potRe, hand.lines[i+1])
            if m != None:
                hand.pot = float(m.groups()[0])
                hand.rake = float(m.groups()[2])
            break

def parseHand(hand):
    parseGameInfo(hand)
    parseTableInfo(hand)
    idx = parsePlayerInfo(hand)
    parseBlindPosts(hand, idx)
    parseBlindPosts(hand, idx+1)
    idx = parsePreflopAction(hand, idx+2)
    idx = parseFlopAction(hand, idx)
    idx = parseTurnAction(hand, idx)
    idx = parseRiverAction(hand, idx)
    parseSummary(hand, idx)

def parseHandsFromFile(filename):
    result = []

    with open(filename, 'r') as inputfile:
        lines = inputfile.readlines()

    handInProcess = False
    for line in lines:
        if line == '\r\n' or line == '\n':
            if handInProcess:
                parseHand(hand)
                if hand.pot != None:
                    result.append(hand)
                handInProcess = False
        else:
            if not handInProcess:
                hand = Hand()
                handInProcess = True

            hand.lines.append(line)

    return result

