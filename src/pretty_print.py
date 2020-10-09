def ch(char):
	if len(char) == 1:
		return char + ' '
	return char



def print_table(board):
	print('                                                                                                              <<Empty table with fields>>\n'
	      '                     {}--------------{}---------------{}                                                  0 --------------1 ---------------2\n'
		  '                     |               |                |                                                   |               |                |\n'
		  '                     |    {}---------{}----------{}   |                                                   |    3 ---------4 ----------5    |\n'
		  '                     |    |          |           |    |                                                   |    |          |           |    |\n'
		  '                     |    |    {}----{}-----{}   |    |                                                   |    |    6 ----7 -----8    |    |\n'
		  '                     |    |    |            |    |    |                                                   |    |    |            |    |    |\n'
		  '                     {}---{}---{}           {}---{}---{}                                                  9 ---10---11           12---13---14\n'
		  '                     |    |    |            |    |    |                                                   |    |    |            |    |    |\n'
		  '                     |    |    {}----{}-----{}   |    |                                                   |    |    15----16----17    |    |\n'
		  '                     |    |          |           |    |                                                   |    |          |           |    |\n'
		  '                     |    {}---------{}----------{}   |                                                   |    18---------19---------20    |\n'
		  '                     |               |                |                                                   |               |                |\n'
		  '                     {}--------------{}---------------{}                                                  21--------------22---------------23\n'.format(
		ch(board[0]),ch(board[1]),ch(board[2]),ch(board[3]),ch(board[4]),ch(board[5]),ch(board[6]),ch(board[7]),
		ch(board[8]),ch(board[9]),ch(board[10]),ch(board[11]),ch(board[12]),ch(board[13]),ch(board[14]),ch(board[15]),
		ch(board[16]),ch(board[17]),ch(board[18]),ch(board[19]),ch(board[20]),ch(board[21]),ch(board[22]),ch(board[23])))
	print()

def welcome_prompt():
	print('+===================================================================+====================================================+\n'
	      '|                     NINE MAN\'S MORRIS                             |               INITIAL TABLE LAYOUT                 |\n'     
	      '+===================================================================+====================================================+\n'
	      '| RULES OF THE GAME :                                               |         0 --------------1 ---------------2         |\n'
	      '| At the beginning, every playes has 9 pieces. The goal of the game |         |               |                |         |\n'
	      '| is to leave your opponent with only two pieces or leave him       |         |    3 ---------4 ----------5    |         |\n'
	      '| without any possible moves. Table has 24 fields and it is possible|         |    |          |           |    |         |\n'
	      '| to move only to adjacent fields, if they are free. If one of the  |         |    |    6 ----7 -----8    |    |         |\n'
	      '| players make mill (three pieces in a row) then he can remove one  |         |    |    |            |    |    |         |\n'
	      '| opponent\'s piece by choosing one of the fields where opponent     |         9 ---10---11           12---13---14        |\n'
	      '| placed his piece. NOTE: it\'s not allowed to remove opponent piece |         |    |    |            |    |    |         |\n'
	      '| if it\'s already in a MILL, unless his all pieces are in MILLS,    |         |    |    15----16----17    |    |         |\n'
	      '| then you can remove any piece you want. You can remove piece in   |         |    |          |           |    |         |\n'
	      '| any phase of the game.                                            |         |    18---------19---------20    |         |\n'
	      '|                                                                   |         |               |                |         |\n'
	      '| PHASES OF THE GAME:                                               |         21--------------22---------------23        |\n'
	      '| 1. PHASE (INIT) -> in this phase both playes are intermittently   |                                                    |\n'
	      '| placing pieces on free fields ( 0 - 23 on the table). When player +----------------------------------------------------+\n'
	      '| run out of pieces to place, then we are moving to the next stage  |\n'
	      '| of the game.                                                      |\n'
	      '| 2. PHASE (MOVE) -> in this phase players can move their pieces to |\n'
	      '| adjacent free fields. First, they input the piece they want to    |\n'
	      '| move, and then the field where they want to move that piece.      |\n'
	      '| 3. PHASE (FLY) -> if the player remained with only 3 pieces,      |\n'
	      '| then he has additional opportunity to move his pieces to ANY free |\n'
	      '| field on the table, filed doesn\'t has to be adjecent and jumping  |\n'
	      '| over pieces is allowed.                                           |\n'
	      '|                                                                   |\n'
	      '| When one of the players remained with only 2 pieces, or the player|\n'
	      '| can\'t perform any move because every adjacent field is taken, the |\n'
	      '| game is over. Right now, your enemy is computer, can you beat him?|\n'
	      '| You can choose if you want to play first. Yours pieces are marked |\n'
	      '| as W (white) and computers pieces are marked as B (black).        |\n'
	      '|                         GOOD LUCK!                                |\n'
	      '+-------------------------------------------------------------------+\n')
