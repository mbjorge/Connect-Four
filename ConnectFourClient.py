#Connect4 Client

import os,socket,time,sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = raw_input("Host IP: ")

port = 6667

client.connect((host,port))

def clearScreen():
	for i in range(100):
		print "\n"

clearScreen()
print "\nConnected!\n"


message = client.recv(1024)
print message

playerName = message[8:16] #Either 'player X' or 'player O'

def check_board(board):
	"""Return a list of valid columns to play in"""
	validColumns = []

	counter = 0
	for i in range(4,25,3): 
		if board[i] == ' ': #Check if the top of the column is empty
			validColumns.append("{0}".format(counter))
		counter += 1

	return validColumns


def play():
	while True:

		board = client.recv(1024)
		clearScreen()
		print board

		if board[-1] == '!': #Somebody has won
			break

		col = raw_input("\nYour turn {0}.\nWhich column?\n>> ".format(playerName),)

		#Check if the input is a number and if it is a valid column to play in
		while not col.isdigit() or col not in check_board(board):
			col = raw_input("\nYour turn.\nWhich column?\n>> ",)
		
		client.send(str(col))
		
		board = client.recv(1024)			
		clearScreen()
		print board

		if board[-1] == '!':
			break
		else:
			print "Waiting for other player..."

play()

while True:
	playAgain = client.recv(1024)
	print playAgain
	answer = raw_input(">> ")

	while answer != 'y' and answer != 'n':
		print playAgain
		answer = raw_input(">> ")
	
	client.send(answer)
	playAgain = client.recv(1024)

	print "\n"
	clearScreen()
	
	if playAgain == "Let's play!": #Start a new game
		print "\nWaiting for other person to play..."
		if playerName == "player X":
			playerName = "player O"
		else:
			playerName = "player X"
		play()
	else:
		print "Someone didn't want to play again."
		print "Or someone is not smart enough to type y"
		break

client.close()
		
	
