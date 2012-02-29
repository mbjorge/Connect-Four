#c:\Python27

import random
import sys
import math
import time
import os

board = {} #(columb, row) : 0(empty), 1(P1), 10(P2)
height, width = 6, 7 #6x7 is standard Connect Four

#Initialize board
for row in range (0,height):
	for col in range (0,width):
		board[(col, row)] = 0



def print_board(board, newPlay):
	"""Print a graphical representation of the board.
	Human is X. Computer is 0.
	@newPlay - the column most recently played in"""
	
	clearScreen()
	
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
				elif 10 == board[(col, row)]: #Computer
					boardString += "<O>"
				else:	# Empty
					boardString += "   "
				newPiece = -1
				newPlay = -1
			else:
				if newPiece != 1:
					if 1 == board[(col, row)]: #Player 1
						boardString += " X "
					elif 10 == board[(col, row)]: #Computer
						boardString += " O "
					else:	# Empty
						boardString += "   "

				if newPiece == 1 and newPlay == col:
					if 1 == board[(col, row)]: #Player 1
						boardString += "<X>"
					elif 10 == board[(col, row)]: #Computer
						boardString += "<O>"
					else:	# Empty
						boardString += "   "
					newPiece = -1
					newPlay = -1
				elif newPiece == 1:
					if 1 == board[(col, row)]: #Player 1
						boardString += " X "
					elif 10 == board[(col, row)]: #Computer
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
		boardString += " {} " .format(col)

	boardString += "\n"

	win = winner(board)

	if win:
		if -1 == win:
			boardString += "\n\nIt's a tie!"

	print boardString


def clearScreen():
	for i in range(100):
		print "\n"

def play_computer(board, difficulty):
	"""Play a one player game on board until someone wins"""
	p1_turn = True
	col = -1

	while True:
	
		print_board(board, col)
		print col
		
		if p1_turn:
			if col != -1:
				print "\nComputer played in column:", col
			#score, col = minimax(board,p1_turn,difficulty, board)
			tmp, col = put_piece(board,p1_turn,-1)
			p1_turn = False
		else: #Computer turn
			print "\nThinking..."
			score, col = minimax(board,p1_turn,difficulty, board)
			put_piece(board,p1_turn,col)
			p1_turn = True

		if winner(board):
			print_board(board, col)
			if 1 == winner(board):
				sys.exit("Human player wins!")
			else:
				sys.exit("Computer player wins!")
			
	
	
	

def put_piece(board, p1, computerColumn=-1):
	"""Ask a player for the next move. Place the piece in the board."""
	if True == p1:
		piece = 1
	else:
		piece = 10

	#Human turn
	if -1 == computerColumn: 
		message = "\nPlayer {}'s turn.\nWhich column?\n>> " .format('X')

	
		choice = raw_input(message)	
		col = int(choice)

		while col >= width or col < 0:
			print "Not a valid input. Choose again."
			choice = raw_input(message)
			col = int(choice)
	
		while 0 != board[(col, height-1)]: #If the top slot isn't empty, it's not valid
			print "Not a valid input. Choose again."
			choice = raw_input(message)
			col = int(choice)

	#Computer Turn	
	else:
		col = computerColumn		

	#Piece gets added to the first empty slot in the column
	for row in range(0, height):
		if board[(col, row)] == 0:
			board[(col, row)] = piece
			return row, col
	return -1, -1
	

def winner(board):
	"""Determine if someone has gotten four in a row"""

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
		if 0 == board[(col,height-1)]:
			break
		elif col == width-1:
			sys.exit("The game is tie. Nobody is a winner")

	return 0 #No winner

def score_board(board):
	"""Return a value for the board. Positive for Comp, Negative for Human"""
	CompWins = 1000000
	HumanWins = -CompWins
	score = 0

	#Check horizontal
	for row in range(0, height):
		for col in range(0, width-3):
			 tmp = board[(col,row)] + board[(col+1,row)] + board[(col+2,row)] + board[(col+3,row)]
			 if tmp == 40:
			 	return CompWins
			 elif tmp == 4:
			 	return HumanWins
			 else:
			 	score += (int(tmp/10))**3 - (tmp%10)**3 ##Since Comp is represented by 10 and Human by 1, Comp is tens digit, Human is ones digit
				
	#Check vertical
	for col in range(0, width):
		for row in range(0,height-3):
			tmp = board[(col,row)] + board[(col,row+1)] + board[(col,row+2)] + board[(col,row+3)]
			if tmp == 40:
			 	return CompWins
			elif tmp == 4:
			 	return HumanWins
			else:
			 	score += (int(tmp/10))**3 - (tmp%10)**3 ##Since Comp is represented by 10 and Human by 1, Comp is tens digit, Human is ones digit

	#Check diagonal, top left to bottom right
	for row in range(height-1, 2, -1):
		for col in range(0,width-3):
			tmp = board[(col,row)] + board[(col+1,row-1)] + board[(col+2,row-2)] + board[(col+3,row-3)]
			if tmp == 40:
			 	return CompWins
			elif tmp == 4:
			 	return HumanWins
			else:
			 	score += (int(tmp/10))**3 - (tmp%10)**3 ##Since Comp is represented by 10 and Human by 1, Comp is tens digit, Human is ones digit

	#Check diagonal, bottom left to top right
	for row in range(0, height-3):
		for col in range(0, width-3):
			tmp = board[(col,row)] + board[(col+1,row+1)] + board[(col+2,row+2)] + board[(col+3,row+3)]
			if tmp == 40:
			 	return CompWins
			elif tmp == 4:
			 	return HumanWins
			else:
			 	score += (int(tmp/10))**3 - (tmp%10)**3 ##Since Comp is represented by 10 and Human by 1, Comp is tens digit, Human is ones digit

	return score
	
def minimax(maxOrmin, p1, depth, board):
	"""Determine the move the maximizes the minimum loss"""

	HumanWins = -1000000
	CompWins = 1000000
	
	if 0 == depth:
		move = -1
		score = score_board(board)
		return(score, move)
	else:
		if maxOrmin:
			bestScore = HumanWins
		else:
			bestScore = CompWins

		bestMove = -1

		for col in range(0,width):
			if board[(col, height-1)] != 0:
				continue

			rowFilled, tmp = put_piece(board, p1, col)
			if rowFilled == -1:
				continue			
			
			s = score_board(board)
			if (maxOrmin and s == 1000000) or (not maxOrmin and s == -1000000):
				bestMove = col
				bestScore = s
				board[(col,rowFilled)] = 0
				return (bestScore, bestMove)
				
			

			moveInner, scoreInner = 0, 0

			inner = minimax(not maxOrmin, not p1, depth-1, board)
			moveInner = inner[1]
			scoreInner = inner[0]
			board[(col,rowFilled)] = 0

			if maxOrmin:
				if scoreInner >= bestScore:
					bestScore = scoreInner
					bestMove = col
			else:
				if scoreInner <= bestScore:
					bestScore = scoreInner
					bestMove = col

		return (bestScore, bestMove)
				

play_computer(board,5)
	
			
		
