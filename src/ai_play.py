from copy import deepcopy
from time import time
import heuristic_state_functions as h
import global_config as g
import pretty_print as pp
from state import State
import main


def minValue(state, alpha, beta, depth, phase, fly_previous=False):
	val = g.MAXIMUM
	state.makeChildren(phase)
	for successor in state.nextStates:
		val = min(val, alphaBeta(successor, alpha, beta, depth - 1, phase, fly_previous))
		if val <= alpha: return val
		beta = min(beta, val)
	return val


def maxValue(state, alpha, beta, depth, phase, fly_previous=False):
	val = -g.MAXIMUM
	state.makeChildren(phase)
	for successor in state.nextStates:
		val = max(val, alphaBeta(successor, alpha, beta, depth - 1, phase, fly_previous))
		if val >= beta: return val
		alpha = max(alpha, val)
	return val


def alphaBeta(state, alpha, beta, depth, phase, fly_previous=False):
	if phase == 'MILL':
		if fly_previous is False:
			phase = g.PHASECOPY
		else:
			phase = 'FLY'

	if phase == 'MOVE':
		if (state.blackToMove and h.getNumberOfPlayerPieces(state, 'B') == 3) or \
				((not state.blackToMove) and h.getNumberOfPlayerPieces(state, 'W')) == 3:
			phase = 'FLY'

	if state.isTerminalState() and phase != 'INIT':
		return state.getTerminal()
	if depth <= 0 or (time() - g.STARTTIME) > g.TIMEALLOWED:
		return h.evalute(state, phase)

	if state.parent is not None:
		if state.blackToMove:
			if h.millHasBeenMadeInLastTurn(state, 'W'):
				state.blackToMove = False
				if phase == 'FLY':
					#state.blackToMove = False
					return minValue(state, alpha, beta, depth, 'MILL', True)
				else:
					return minValue(state, alpha, beta, depth, 'MILL')
		else:
			if h.millHasBeenMadeInLastTurn(state, 'B'):
				state.blackToMove = True
				if phase == 'FLY':
					#state.blackToMove = True
					return maxValue(state, alpha, beta, depth, 'MILL', True)
				else:
					return maxValue(state, alpha, beta, depth, 'MILL')

	if state.blackToMove:
		return maxValue(state, alpha, beta, depth, phase)
	else:
		return minValue(state, alpha, beta, depth, phase)


def next_move_AI(state, mill):
	g.STARTTIME = time()
	depth = 4

	if h.getNumberOfPlayerPieces(state, 'B') + g.BLACKREMOVED == 9:
		g.PHASE = 'MOVE'
	else:
		g.PHASE = 'INIT'

	if h.getNumberOfPlayerPieces(state, 'B') == 3 and g.PHASE != 'INIT':
		g.PHASE = 'FLY'
		depth = 2

	g.PHASECOPY = g.PHASE

	if mill:
		state.makeChildren('MILL')
	else:
		state.makeChildren(g.PHASECOPY)
	depth -= 1

	bestMove = None
	alpha = -g.MAXIMUM
	for successor in state.nextStates:
		if time() - g.STARTTIME > g.TIMEALLOWED: break
		score = alphaBeta(successor, -g.MAXIMUM, g.MAXIMUM, depth, g.PHASECOPY)
		if score >= alpha:
			alpha, bestMove = score, successor.move
		if alpha >= g.MAXIMUM:
			break
	return bestMove


def AI_play(state, mill):
	move = next_move_AI(state, mill)
	old_state_table = deepcopy(state.board)
	if mill:
		g.TABLE[move[0]] = g.EMPTYCELL[move[0]]
		pp.print_table(state.board)
		print("Computer just made the MILL and he removed your piece from {}. field.".format(move[0]))
		g.WHITEREMOVED += 1
	elif g.PHASE == 'INIT':
		g.TABLE[move[0]] = 'B'
		pp.print_table(state.board)
		print("Computer has placed his piece at {}. field.".format(move[0]))
	elif g.PHASE == 'MOVE' or g.PHASE == 'FLY':
		g.TABLE[move[1]] = 'B'
		g.TABLE[move[0]] = g.EMPTYCELL[move[0]]
		pp.print_table(state.board)
		print("Computer has moved his piece from {}. field to {}. field.".format(move[0], move[1]))
	state.board = old_state_table
	new_state = State(g.TABLE, False, move, state)
	main.play(new_state)
