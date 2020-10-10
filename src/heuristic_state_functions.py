import global_config as g


def getNumberOf2PeacesConfig(state, player):
	number = 0
	for trio in g.MILLS:
		if state.board[trio[0]] == state.board[trio[1]] == player and state.board[trio[2]] in g.EMPTYCELL.values():
			number += 1
		if state.board[trio[1]] == state.board[trio[2]] == player and state.board[trio[0]] in g.EMPTYCELL.values():
			number += 1
		if state.board[trio[0]] == state.board[trio[2]] == player and state.board[trio[1]] in g.EMPTYCELL.values():
			number += 1
	return number


def getNumberOf3PeaceConfig(state, player):
	number = 0
	for var in g.TREECONFIG:
		if state.board[var[0]] == state.board[var[1]] == state.board[var[2]] == player and state.board[
			var[3]] in g.EMPTYCELL.values() and state.board[var[4]] in g.EMPTYCELL.values():
			number += 1
	return number


def getNumberOfPlayerDoubleMills(state, player):
	number = 0
	for var in g.MILLS2:
		if state.board[var[0]] == state.board[var[1]] == state.board[var[2]] == state.board[var[3]] == state.board[
			var[4]] == player:
			number += 1
	return number


def getNumberOfPlayerMills(state, player):
	numberOfMills = 0
	for trio in g.MILLS:
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
	for key, value in g.ADJDICT.items():
		temp = 0
		if state.board[key] == player:
			for adj in value:
				if state.board[adj] in g.EMPTYCELL.values():
					temp = 1
					break
			if temp == 0: number += 1
	return number


def allPlayerPiecesClosed(state, player):
	for key, value in g.ADJDICT.items():
		if state.board[key] == player:
			for adj in value:
				if state.board[adj] in g.EMPTYCELL.values():
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
	for trio in g.MILLS:
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
	if state.parent is None:
		return 0
	if state.blackToMove:
		if millHasBeenMadeInLastTurn(state, 'W'):
			return -1
	else:
		if millHasBeenMadeInLastTurn(state, 'B'):
			return 1
	return 0


def pieceInMill(state, index_peace):
	for par in g.PEACEINMILL[index_peace]:
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
		if state.board[i] in g.EMPTYCELL.values():
			pos.append(i)
	return pos



"""
Final heuristics, you can change coefficients if you see that
computer is playing better with those new coefficients
"""

def evalute(state, phase):
	result = 0
	if phase == 'INIT':
		result =18 * closedMorris(state) + \
				26 * differceInNumberOfMills(state) + \
				1 * differenceInClosedPeaces(state) + \
				9 * differceInPieces(state) + \
				10 * differenceIn2PeacesConfig(state) + \
				7 * differenceIn3PeacesConfig(state)

	elif phase == 'MOVE':
		result =14 * closedMorris(state) + \
				43 * differceInNumberOfMills(state) + \
				10 * differenceInClosedPeaces(state) + \
				11 * differceInPieces(state) + \
				8 * differenceInDoubleMorrises(state) + \
				1086 * winningConfiguration(state)

	elif phase == 'FLY':
		result =16 * differenceIn2PeacesConfig(state) + \
				10 * differenceIn3PeacesConfig(state) +\
				1 * closedMorris(state) + \
				1190 * winningConfiguration(state)
	return result


