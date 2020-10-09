from copy import deepcopy
import heuristic_state_functions as h
import global_config as g
import pretty_print as pp
from state import State
import main


def human_play_mill(state):
	old_state_board = deepcopy(state.board)
	print()
	pp.print_table(state.board)

	br = 0
	possibilities = []
	for i in range(24):
		if not h.pieceInMill(state, i):
			if state.board[i] == 'B':
				possibilities.append(i)
				br += 1
	if br == 0:
		for i in range(24):
			if state.board[i] == 'B':
				possibilities.append(i)

	while True:
		place = input("You just made the mill! Input the field from which you want to remove opponent\'s piece >> ")
		try:
			place = int(place)
		except:
			continue
		if place not in possibilities:
			print("You can\'t remove the piece from this field.")
		else:
			break

	g.TABLE[place] = g.EMPTYCELL[place]
	g.BLACKREMOVED += 1
	state.board = old_state_board
	new_state = State(g.TABLE, True, [place], state)
	main.play(new_state)


def human_play_init(state):
	old_state_board = deepcopy(state.board)
	possibilities = []
	for i in range(24):
		if state.board[i] in g.EMPTYCELL.values():
			possibilities.append(i)

	while True:
		place = input("Input the field on which you want to place the piece >> ")
		try:
			place = int(place)
		except:
			continue
		if place not in possibilities:
			print("You can't place the piece on this field.")
		else:
			break

	g.TABLE[place] = 'W'
	state.board = old_state_board
	new_state = State(g.TABLE, True, [place], state)
	main.play(new_state)


def human_play_move(state):
	old_state_board = deepcopy(state.board)
	possibilities1 = []
	for i in range(24):
		if state.board[i] == 'W':
			possibilities1.append(i)

	while True:
		first = input("Input the field from which you want to move the piece >> ")
		try:
			first = int(first)
		except:
			continue
		if first not in possibilities1:
			print("You can't move the piece from this field.")
		else:
			br = 0
			for index in g.ADJDICT[first]:
				if state.board[index] in g.EMPTYCELL.values():
					br = 1
					break
			if br == 1:
				break
			print("This field doesn't have adjacent free fields.")



	possibilities2 = []
	for index in g.ADJDICT[first]:
		if state.board[index] in g.EMPTYCELL.values():
			possibilities2.append(index)

	while True:
		second = input("Input the adjacent field on which you want to move the piece >> ")
		try:
			second = int(second)
		except:
			continue
		if second not in possibilities2:
			print("This field is not adjacent or it's already taken.")
		else:
			break

	g.TABLE[second] = 'W'
	g.TABLE[first] = g.EMPTYCELL[first]
	state.board = old_state_board
	new_state = State(g.TABLE, True, [first, second], state)
	main.play(new_state)


def human_play_fly(state):
	old_state_board = deepcopy(state.board)
	possibilities1 = []
	possibilities_free = []
	for i in range(24):
		if state.board[i] == 'W':
			possibilities1.append(i)
		if state.board[i] in g.EMPTYCELL.values():
			possibilities_free.append(i)

	while True:
		first = input("Input the field from which you want to move the piece (it's FLY phase time!): ")
		try:
			first = int(first)
		except:
			continue
		if first not in possibilities1:
			print("You can't move the piece from this field.")
		else:
			break

	while True:
		second = input("Input ANY free field on the table on which you want to move the piece >> ")
		try:
			second = int(second)
		except:
			continue
		if second not in possibilities_free:
			print("This field is not free.")
		else:
			break

	g.TABLE[second] = 'W'
	g.TABLE[first] = g.EMPTYCELL[first]
	state.board = old_state_board
	new_state = State(g.TABLE, True, [first, second], state)
	main.play(new_state)


def human_play(state, mill):
	if h.getNumberOfPlayerPieces(state, 'W') + g.WHITEREMOVED == 9:
		g.PHASE = 'MOVE'
	else:
		g.PHASE = 'INIT'

	if h.getNumberOfPlayerPieces(state, 'W') == 3 and g.PHASE != 'INIT':
		g.PHASE = 'FLY'

	if mill:
		human_play_mill(state)
	elif g.PHASE == 'INIT':
		human_play_init(state)
	elif g.PHASE == 'MOVE':
		human_play_move(state)
	elif g.PHASE == 'FLY':
		human_play_fly(state)
