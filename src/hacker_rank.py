"""
Implementation for hacker rank
Black player wants maximum, and white wants minimum
"""


from copy import deepcopy
from time import time


POSDICT = {0: (0, 0), 1: (0, 3), 2: (0, 6), 3: (1, 1), 4: (1, 3), 5: (1, 5), 6: (2, 2), 7: (2, 3), 8: (2, 4),
		   9: (3, 0), 10: (3, 1), 11: (3, 2), 12: (3, 4), 13: (3, 5), 14: (3, 6), 15: (4, 2), 16: (4, 3), 17: (4, 4),
		   18: (5, 1), 19: (5, 3), 20: (5, 5), 21: (6, 0), 22: (6, 3), 23: (6, 6)}

ADJDICT = {0: (1, 9), 1: (0, 2, 4), 2: (1, 14), 3: (4, 10), 4: (1, 3, 5, 7), 5: (4, 13), 6: (7, 11),
		   7: (4, 6, 8), 8: (7, 12), 9: (0, 21, 10), 10: (3, 8, 11, 18), 11: (6, 10, 15), 12: (8, 13, 17),
		   13: (5, 12, 14, 20), 14: (2, 13, 23), 15: (11, 16), 16: (15, 17, 19), 17: (12, 16),
		   18: (10, 19), 19: (16, 18, 20, 22), 20: (13, 19), 21: (9, 22), 22: (19, 21, 23), 23: (14, 22)}

MILLS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
		 (0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7), (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23))

TREECONFIG = \
	((9, 0, 1, 2, 21), (9, 21, 22, 0, 23), (1, 2, 14, 0, 23), (22, 23, 14, 21, 2), (10, 3, 4, 5, 18), (4, 5, 13, 3, 20),
	 (10, 18, 19, 3, 20), (19, 20, 13, 18, 5), (11, 6, 7, 15, 8), (7, 8, 12, 6, 17), (11, 15, 16, 6, 17),
	 (16, 17, 12, 15, 8), (0, 1, 4, 7, 2), (2, 1, 4, 0, 7), (21, 22, 19, 16, 23), (23, 22, 19, 16, 21),
	 (0, 9, 10, 11, 21),
	 (21, 9, 10, 11, 0), (2, 13, 14, 12, 23), (13, 14, 23, 12, 2), (3, 4, 7, 5, 1), (3, 4, 1, 7, 5), (4, 5, 7, 3, 1),
	 (5, 4, 1, 7, 3), (22, 19, 18, 20, 16), (18, 19, 16, 22, 20), (20, 19, 22, 16, 18), (20, 19, 16, 18, 22),
	 (3, 10, 11, 9, 18), (3, 9, 10, 11, 18), (18, 10, 11, 9, 3), (18, 10, 9, 11, 3), (5, 12, 13, 14, 20),
	 (5, 13, 14, 12, 20),
	 (20, 13, 14, 12, 5), (20, 13, 12, 5, 14), (6, 7, 4, 1, 8), (8, 7, 4, 1, 6), (6, 11, 10, 9, 15), (15, 11, 10, 6, 9),
	 (15, 16, 19, 17, 22), (16, 17, 19, 15, 22), (17, 12, 13, 8, 14), (8, 12, 13, 14, 17))

MILLS2 = (
	(23, 22, 21, 9, 0), (21, 22, 23, 14, 2), (21, 9, 0, 1, 2), (0, 1, 2, 14, 23), (20, 19, 18, 10, 3),
	(18, 19, 20, 13, 5),
	(18, 10, 3, 4, 5), (20, 13, 5, 4, 3), (17, 16, 15, 11, 6), (15, 16, 17, 12, 8), (15, 11, 6, 7, 8),
	(6, 7, 8, 12, 17),
	(0, 1, 2, 4, 7), (21, 22, 23, 19, 16), (0, 9, 21, 10, 11), (2, 14, 23, 12, 13), (1, 4, 7, 3, 5), (3, 10, 18, 9, 11),
	(5, 13, 20, 12, 14), (16, 19, 22, 18, 20), (6, 7, 8, 4, 1), (6, 11, 15, 9, 10), (15, 16, 17, 19, 22),
	(8, 12, 17, 13, 14))

PEACEINMILL = {0: [(1, 2), (9, 21)], 1: [(0, 2), (4, 7)], 2: [(0, 1), (14, 23)], 3: [(4, 5), (10, 18)],
			   4: [(3, 5), (1, 7)],
			   5: [(13, 20), (3, 4)], 6: [(7, 8), (11, 15)], 7: [(1, 4), (6, 8)], 8: [(6, 7), (12, 17)],
			   9: [(0, 21), (10, 11)],
			   10: [(9, 11), (3, 18)], 11: [(15, 6), (9, 10)], 12: [(8, 17), (13, 14)], 13: [(12, 14), (5, 20)],
			   14: [(2, 23), (12, 13)],
			   15: [(16, 17), (11, 6)], 16: [(15, 17), (19, 22)], 17: [(12, 8), (15, 16)], 18: [(3, 10), (19, 20)],
			   19: [(18, 20), (16, 22)],
			   20: [(13, 5), (18, 19)], 21: [(0, 9), (22, 23)], 22: [(21, 23), (16, 19)], 23: [(2, 14), (21, 22)]}

EMPTYCELL = 'O'
PHASE = ''
MAXIMUM = 10e9
WALL = ['-', '|', '*']

IsPlayerBlack = True


def getNumberOf2PeacesConfig(state, player):
	number = 0
	for trio in MILLS:
		if state.board[trio[0]] == state.board[trio[1]] == player and state.board[trio[2]] == EMPTYCELL:
			number += 1
		if state.board[trio[1]] == state.board[trio[2]] == player and state.board[trio[0]] == EMPTYCELL:
			number += 1
	return number


def getNumberOf3PeaceConfig(state, player):
	number = 0
	for var in TREECONFIG:
		if state.board[var[0]] == state.board[var[1]] == state.board[var[2]] == player and state.board[
			var[3]] == EMPTYCELL and state.board[var[4]] == EMPTYCELL:
			number += 1
	return number


def getNumberOfPlayerDoubleMills(state, player):
	number = 0
	for var in MILLS2:
		if state.board[var[0]] == state.board[var[1]] == state.board[var[2]] == state.board[var[3]] == state.board[
			var[4]] == player:
			number += 1
	return number


def getNumberOfPlayerMills(state, player):
	numberOfMills = 0
	for trio in MILLS:
		if state.board[trio[0]] == state.board[trio[1]] == state.board[trio[2]] == player:
			numberOfMills += 1
	return numberOfMills


def getNumberOfPlayerPieces(state, player):
	number = 0
	for position in state.board:
		if position == player:
			number += 1
	return number


def getNumberOfPlayerClosedPeaces(state, player):
	number = 0
	for key, value in ADJDICT.items():
		temp = 0
		if state.board[key] == player:
			for adj in value:
				if state.board[adj] == EMPTYCELL:
					temp = 1
					break
			if temp == 0: number += 1
	return number


def allPlayerPiecesClosed(state, player):
	for key, value in ADJDICT.items():
		if state.board[key] == player:
			for adj in value:
				if state.board[adj] == EMPTYCELL:
					return False
	return True


def differenceIn3PeacesConfig(state):
	black = getNumberOf3PeaceConfig(state, 'B')
	white = getNumberOf3PeaceConfig(state, 'W')
	return black - white


def differenceInDoubleMorrises(state):
	black = getNumberOfPlayerDoubleMills(state, 'B')
	white = getNumberOfPlayerDoubleMills(state, 'W')
	return black - white


def differenceIn2PeacesConfig(state):
	black = getNumberOf2PeacesConfig(state, 'B')
	white = getNumberOf2PeacesConfig(state, 'W')
	return black - white


def differenceInClosedPeaces(state):
	black = getNumberOfPlayerClosedPeaces(state, 'B')
	white = getNumberOfPlayerClosedPeaces(state, 'W')
	return black - white


def differceInNumberOfMills(state):
	black = getNumberOfPlayerMills(state, 'B')
	white = getNumberOfPlayerMills(state, 'W')
	return black - white


def differceInPieces(state):
	black = getNumberOfPlayerPieces(state, 'B')
	white = getNumberOfPlayerPieces(state, 'W')
	return black - white


def winningConfiguration(state):
	if allPlayerPiecesClosed(state, 'W') or getNumberOfPlayerPieces(state, 'W') < 3:
		return 1
	if allPlayerPiecesClosed(state, 'B') or getNumberOfPlayerPieces(state, 'B') < 3:
		return -1
	return 0


def getListOfAllPlayerMills(state, player):
	list = []
	for trio in MILLS:
		if state.board[trio[0]] == state.board[trio[1]] == state.board[trio[2]] == player:
			list.append(trio)
	return list

def millHasBeenMadeInLastTurn(state, player):
	parent_mills = getListOfAllPlayerMills(state.parent, player)
	current_mills = getListOfAllPlayerMills(state, player)
	for mill in current_mills:
		if mill not in parent_mills:
			return True
	return False

def closedMorris(state):
	if state.parent == None:
		return 0
	if state.blackToMove:
		if millHasBeenMadeInLastTurn(state, 'W'):
			return -1
	else:
		if millHasBeenMadeInLastTurn(state, 'B'):
			return 1
	return 0


def pieceInMill(state, index_peace):
	for par in PEACEINMILL[index_peace]:
		if state.board[par[0]] == state.board[par[1]] == state.board[index_peace]:
			return True
	return False


def getAllPositionsOfPlayer(state, player):
	positions = []
	for i in range(24):
		if state.board[i] == player:
			positions.append(i)
	return positions


def getAllEmptyPositionsOnBoard(state):
	pos = []
	for i in range(24):
		if state.board[i] == EMPTYCELL:
			pos.append(i)
	return pos


class State(object):
	def __init__(self, board, blackToMove, move, parent=None, nextStates=None):
		if nextStates == None:
			nextStates = []
		self.board = board
		self.blackToMove = blackToMove
		self.move = move
		self.parent = parent
		self.nextStates = nextStates

	def isTerminalState(self):
		loserIsBlack, loserIsWhite = False, False
		if allPlayerPiecesClosed(self, 'B') or getNumberOfPlayerPieces(self, 'B') < 3:
			loserIsBlack = True
		if allPlayerPiecesClosed(self, 'W') or getNumberOfPlayerPieces(self, 'W') < 3:
			loserIsWhite = True
		if loserIsBlack is False and loserIsWhite is False:
			return False
		if loserIsWhite: self.isLoserBlack = False
		else: self.isLoserBlack = True
		return True

	def getTerminal(self):
		if self.isLoserBlack:
			return -MAXIMUM
		else:
			return MAXIMUM

	def nextStatesInit(self):
		for i in range(24):
			if self.board[i] == EMPTYCELL:
				boardCopy = deepcopy(self.board)
				if self.blackToMove:
					boardCopy[i] = 'B'
				else:
					boardCopy[i] = 'W'
				self.nextStates.append(State(boardCopy, not self.blackToMove, [i], self))

	def nextStatesMove(self):
		if self.blackToMove:
			player = 'B'
		else:
			player = 'W'
		for key, value in ADJDICT.items():
			if self.board[key] == player:
				for index in value:
					if self.board[index] == EMPTYCELL:
						boardCopy = deepcopy(self.board)
						boardCopy[index] = player
						boardCopy[key] = EMPTYCELL
						self.nextStates.append(State(boardCopy, not self.blackToMove, [key, index], self))

	def nextStatesFly(self):
		if self.blackToMove:
			player = 'B'
		else:
			player = 'W'
		player_pieces = getAllPositionsOfPlayer(self, player)
		empty_pos = getAllEmptyPositionsOnBoard(self)
		for piece in player_pieces:
			for cell in empty_pos:
				boardCopy = deepcopy(self.board)
				boardCopy[cell] = player
				boardCopy[piece] = EMPTYCELL
				self.nextStates.append(State(boardCopy, not self.blackToMove, [piece, cell], self))

	def nextStatesMill(self):
		br = 0
		for i in range(24):
			if not pieceInMill(self, i):
				if (self.blackToMove and self.board[i] == 'W') or ((not self.blackToMove) and self.board[i] == 'B'):
					boardCopy = deepcopy(self.board)
					boardCopy[i] = EMPTYCELL
					self.nextStates.append(State(boardCopy, not self.blackToMove, [i], self))
					br += 1
		if br == 0:
			for i in range(24):
				if (self.blackToMove and self.board[i] == 'W') or ((not self.blackToMove) and self.board[i] == 'B'):
					boardCopy = deepcopy(self.board)
					boardCopy[i] = EMPTYCELL
					self.nextStates.append(State(boardCopy, not self.blackToMove, [i], self))

	def makeChildren(self, phase):
		if phase == 'INIT':
			self.nextStatesInit()
		if phase == 'MILL':
			self.nextStatesMill()
		if phase == 'MOVE':
			self.nextStatesMove()
		if phase == 'FLY':
			self.nextStatesFly()


def maxValue(state, alpha, beta, depth, phase, fly_previous=False):
	state.makeChildren(phase)
	for successor in state.nextStates:
		score = alphaBeta(successor, alpha, beta, depth - 1, phase, fly_previous)
		alpha = max(alpha, score)
		if alpha >= beta:
			return beta
	return alpha


def minValue(state, alpha, beta, depth, phase, fly_previous=False):
	state.makeChildren(phase)
	for successor in state.nextStates:
		score = alphaBeta(successor, alpha, beta, depth - 1, phase, fly_previous)
		beta = min(beta, score)
		if alpha >= beta:
			return alpha
	return beta


def alphaBeta(state, alpha, beta, depth, phase, fly_previous=False):
	global PHASE
	if phase == 'MILL' and fly_previous:
		phase = 'FLY'
	else: phase = PHASE


	if phase == 'MOVE':
		if (state.blackToMove and getNumberOfPlayerPieces(state, 'B') == 3) or \
				((not state.blackToMove) and getNumberOfPlayerPieces(state, 'W')) == 3:
			phase = 'FLY'
			if depth > 2:
				depth = 2


	if state.isTerminalState() and PHASE != 'INIT':
		return state.getTerminal()
	if depth <= 0:
		return evalute(state, phase)



	if state.parent is not None:
		if state.blackToMove:
			if millHasBeenMadeInLastTurn(state, 'W'):
				state.blackToMove = False
				if phase == 'FLY':
					return minValue(state,alpha,beta,depth,'MILL', True)
				else:
					return minValue(state,alpha,beta,depth,'MILL')
		else:
			if millHasBeenMadeInLastTurn(state, 'B'):
				state.blackToMove = True
				if phase == 'FLY':
					return maxValue(state,alpha,beta,depth,'MILL', True)
				else:
					return maxValue(state,alpha,beta,depth,'MILL')


	if state.blackToMove:
		return maxValue(state, alpha, beta, depth, phase)
	else:
		return minValue(state, alpha, beta, depth, phase)


def next_move(state):
	global PHASE
	depth = 4
	if PHASE == 'MOVE':
		if (state.blackToMove and getNumberOfPlayerPieces(state, 'B') == 3) or \
				((not state.blackToMove) and getNumberOfPlayerPieces(state, 'W')) == 3:
			PHASE = 'FLY'
			depth = 2

	state.makeChildren(PHASE)
	depth -= 1

	if PHASE == 'MILL':
		PHASE = 'INIT'

	bestMove = None
	if state.blackToMove:
		val = -MAXIMUM
		for successor in state.nextStates:
			score = alphaBeta(successor, -MAXIMUM, MAXIMUM, depth, PHASE)
			if score >= val:
				val, bestMove = score, successor.move
		return bestMove
	else:
		val = MAXIMUM
		for successor in state.nextStates:
			score = alphaBeta(successor, -MAXIMUM, MAXIMUM, depth, PHASE)
			if score <= val:
				val, bestMove = score, successor.move
		return bestMove

def evalute(state, phase):
	result = 0
	if phase == 'INIT':
		result = 18 * closedMorris(state) + \
				 26 * differceInNumberOfMills(state) + \
				 1 * differenceInClosedPeaces(state) + \
				 6 * differceInPieces(state) + \
				 21 * differenceIn2PeacesConfig(state) + \
				 7 * differenceIn3PeacesConfig(state)

	elif phase == 'MOVE':
		result = 42 * closedMorris(state) + \
				 28 * differceInNumberOfMills(state) + \
				 16 * differenceInClosedPeaces(state) + \
				 8 * differceInPieces(state) + \
				 25 * differenceInDoubleMorrises(state) + \
				 949 * winningConfiguration(state)

	elif phase == 'FLY':
		result = 23 * differenceIn2PeacesConfig(state) + \
				 21 * differenceIn3PeacesConfig(state) + \
				 5 * closedMorris(state) + \
				 1120 * winningConfiguration(state)
	return result

if __name__ == '__main__':
	player = input().strip()
	PHASE = input().strip()
	board = []
	for i in range(7):
		row = list(input())
		for cell in row:
			if cell not in WALL:
				board.append(cell)

	if player == 'B':
		IsPlayerBlack = True
	else:
		IsPlayerBlack = False

	state = State(board, IsPlayerBlack, [])

	move = next_move(state)

	if len(move) == 1:
		cordinates = POSDICT[move[0]]
		print(cordinates[0], cordinates[1])
	else:
		start = POSDICT[move[0]]
		stop = POSDICT[move[1]]
		print(start[0], start[1], stop[0], stop[1])

