#Connect4 Server

import socket, sys, os, thread, time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 6667
server.bind(('',port))

server.listen(2) #Listen for players 1 and 2

#Player 1 is the first player to connect
player1, addr1 = server.accept()
player1.send("You are player X.\nWaiting for player O to connect...")
print "Player 1 connected from", addr1

#Player 2 is the second player to connect
player2, addr2 = server.accept()
player2.send("You are player O.\nWaiting for Player X to start the game...\n")
print "Player 2 connected from", addr2

#-------------------------------------------------
#Initialize a board
board = {} #key: (column, row); value: 0=empty, 1=P1, 2=P2
height, width = 6, 7 #6x7 is the standard Connect Four dimensions

for row in range (0,height):
	for col in range (0,width):
		board[(col, row)] = 0 #All squares are empty
#------------------------------------------------


#*************************
#Functions for the game
#*************************

def put_piece(board, p1_turn, col):
	"""Place the piece in the board with the appropriate value based on the player."""
	
	if True == p1_turn:
		piece = 1
	else:
		piece = 2

	#Piece gets added to the first empty slot in the column
	#If the column is full, no piece is added
	for row in range(0, height):
		if board[(col, row)] == 0:
			board[(col, row)] = piece
			break

def winner(board):
	"""Determine if someone has gotten four in a row.
	Return 1 if P1 wins, 2 if P2 wins, 0 if no winner yet, or -1 if a tie.
	"""

	#Check horizontal
	for row in range(0, height):
		for col in range(0, width-3):
			if board[(col,row)] != 0 and board[(col,row)] == board[(col+1,row)] and board[(col+1,row)] == board[(col+2,row)]  and board[(col+2,row)] == board[(col+3,row)]:				
				return board[(col,row)]

	#Check vertical
	for col in range(0, width):
		for row in range(0,height-3):
			if board[(col,row)] != 0 and board[(col,row)] == board[(col,row+1)] and board[(col,row+1)] == board[(col,row+2)]  and board[(col,row+2)] == board[(col,row+3)]:
				return board[(col,row)]

	#Check diagonal, top left to bottom right
	for row in range(height-1, 2, -1):
		for col in range(0,width-3):
			if board[(col,row)] != 0 and board[(col,row)] == board[(col+1,row-1)] and board[(col+1,row-1)] == board[(col+2,row-2)] and board[(col+2,row-2)] == board[(col+3,row-3)]:
				return board[(col,row)]

	#Check diagonal, bottom left to top right
	for row in range(0, height-3):
		for col in range(0, width-3):
			if board[(col,row)] != 0 and board[(col,row)] == board[(col+1,row+1)] and board[(col+1,row+1)] == board[(col+2,row+2)] and board[(col+2,row+2)] == board[(col+3,row+3)]:
				return board[(col,row)]

	#The board is full; it's a tie.
	for col in range(0,width):
		if 0 == board[(col,height-1)]: #There is still an empty space
			break
		elif col == width -1:
			return -1 #A tie

	return 0 #No winner yet

def board_to_string(board, newPlay):
	"""Convert the board to a string
	board is the board to be converted.
	newPlay is the column most recently played in"""
	
	boardString = ''
	boardString += "\n\n"


	newPiece = 0 #Used to identify if the new piece has been added with the < > identifiers
	
	#Make the string
	for row in range(height-1, -1, -1): #Start at the top and go down
	
		boardString += "|"
		
		for col in range(0,width): #Start at the left and go right

			if row == height-1 and newPlay == col and board[(newPlay,height-1)] != 0:
				if 1 == board[(col, row)]: #Player 1
					boardString += "<X>"
				elif 2 == board[(col, row)]: #Player 2
					boardString += "<O>"
				else:	# Empty
					boardString += " ? 
				newPiece = -1
				newPlay = -1
			else:
				if newPiece != 1:
					if 1 == board[(col, row)]: #Player 1
						boardString += " X "
					elif 2 == board[(col, row)]: #Player 2
						boardString += " O "
					else:	# Empty
						boardString += "   "

				if newPiece == 1 and newPlay == col:
					if 1 == board[(col, row)]: #Player 1
						boardString += "<X>"
					elif 2 == board[(col, row)]: #Player 2
						boardString += "<O>"
					else:	# Empty
						boardString += "   "
					newPiece = -1
					newPlay = -1
				elif newPiece == 1:
					if 1 == board[(col, row)]: #Player 1
						boardString += " X "
					elif 2 == board[(col, row)]: #Player 2
						boardString += " O "
					else:	# Empty
						boardString += "   "

			if newPlay == col and newPiece == 0 and row > 0 and board[(col, row-1)] != 0:
				newPiece += 1				
				
		boardString += "|\n\n"

	#Add column labels on the bottom
	for col in range(0, width-1):
		boardString += "- - "
		
	boardString += "\n "
	for col in range(0, width):
		boardString += " {0} " .format(col)

	boardString += "\n"

	win = winner(board)

	if win:
		if -1 == win:
			boardString += "\n\nIt's a tie!"
		else:
			boardString += "\n\n!!!!!!!Player {0} wins!!!!!!!".format(win)

	return boardString

#********************************************************************


def play(player1, player2):
	"""Make a game of Connect 4"""

	col = -1
	while True:

		#Player 1 Turn
		player1.send(board_to_string(board, col))
		
		choice = player1.recv(10)
		col = int(choice)

		#If the column choice is not valid, the piece goes in the first empty slot
		if col >= width or col < 0 or 0 != board[(col,height-1)]:
			col = 0
			while 0 != board[(col,height-1)]:
				col += 1

		put_piece(board, True, col) ##the second argument indicates it is P1 turn
		
		player1.send(board_to_string(board, col))

		#See if player 1 has just played a winning move
		if winner(board):
			time.sleep(1)
			player2.send(board_to_string(board, col))
			print "Player {0} won".format(winner(board))
			break

		#Player 2 Turn
		player2.send(board_to_string(board, col))

		choice = player2.recv(10)
		col = int(choice)

		#If the column choice is not valid, the piece goes in the first empty slot
		if col >= width or col < 0 or 0 != board[(col,height-1)]:
			col = 0
			while 0 != board[(col,height-1)]:
				col += 1

		put_piece(board, False, col) ##the second argument indicates it is P2 turn
		player2.send(board_to_string(board, col))

		#See if player 2 has just played a winning move
		if winner(board):
			time.sleep(1)
			player1.send(board_to_string(board, col))
			print "Player {0} won".format(winner(board))
			break

play(player1, player2)

play_again = True

while play_again:

	print "Sent to 1"
	player1.send("Play again y/n?")


	p1Ans = player1.recv(1)
	print "Received from 1"

	print "Sent to 2"
	player2.send("Play again y/n?")
	
	time.sleep(1)
	p2Ans = player2.recv(1)
	print "Recieve from 2"

	print "{0}, {1}".format(p1Ans, p2Ans)
	
	if p1Ans == 'y' and p2Ans == 'y':
		for row in range (0,height):
			for col in range (0,width):
				board[(col, row)] = 0 #Reset the board
		player1.send("Let's play!")
		player2.send("Let's play!")
		
		player1, player2 = player2, player1 #Switch who gets to play first
		play(player1, player2)
		
	elif p1Ans != 'y':
		player2.send("Player 1 does not like fun or does not know how to type. He (or she) did not want to face you again")
		player1.send("You must not like fun.")
		play_again = False
	else:
		player1.send("Player 2 does not like fun or does not know how to type. He (or she) did not want to face you again")
		player2.send("You must not like fun.")
		play_again = False
		


player1.close()
player2.close()
server.close()


