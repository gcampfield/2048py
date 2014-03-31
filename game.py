import random

try:
	from colorama import init, Fore, Style
	init(autoreset=True)
	COLORAMA = True
	COLORS = {
		   0: Fore.WHITE,
           2: Fore.GREEN,
           4: Fore.BLUE + Style.BRIGHT,
           8: Fore.CYAN,
          16: Fore.RED,
          32: Fore.MAGENTA,
          64: Fore.CYAN,
         128: Fore.BLUE + Style.BRIGHT,
         256: Fore.MAGENTA,
         512: Fore.GREEN,
        1024: Fore.RED,
        2048: Fore.YELLOW,
        4096: Fore.MAGENTA,
        8192: Fore.CYAN,
    }
except:
	COLORAMA = False
	print "\033[93mNOTE: in order for text to be colored, you must install 'termred' from PyPI\033[0m\n"

class InvalidMoveError(Exception) :
	'''
	Raised by game.shiftLeft or game.shiftRight if the move
	did not change anything
	'''
	pass

class game(object):
	def __init__(self, size=4, prob=.9, goal=2048, numStartTiles=2):
		'''
		Initializes the game with a board size x size big with numStartTiles
		tiles to begin

		w - width of the board
		h - height of the board
		prob - probability of spawning a 2 over a 4
		goal - the number used check if the game is won
		numStartTiles - the number of tiles to begin with
		'''
		self.size = size
		self.board = [[0 for a in range(size)] for b in range(size)]
		self.score = 0
		self.prob = prob
		self.goal = goal
		for i in range(numStartTiles) :
			self.addTile()


	def isWon(self):
		'''
		Sees if self.goal is on the board

		returns: True if the game is won, else False
		'''
		for row in self.board:
			if self.goal in row:
				return True
		return False

	def getScore(self):
		'''
		returns: the current score of the game
		'''
		return self.score

	def printBoard(self):
		'''
		Prints the current board in a pretty array fashion
		'''
		for row in self.board:
			for val in row:
				if COLORAMA :
					print '{0}{1:<6}'.format(COLORS[val], val),
				else :
					print '{:<6}'.format(val),
			print

	def getEmptyTiles(self):
		'''
		returns: a list of all of the coordinates of empty tiles
		on the board
		'''
		emptyTiles = []
		for rowNum in range(len(self.board)):
			for colNum in range(len(self.board[rowNum])):
				if not self.board[rowNum][colNum]:
					emptyTiles.append((rowNum, colNum))
		return emptyTiles

	def addTile(self, loc=None):
		'''
		Places a tile at loc if loc given, or else it places one
		in a random empty tile

		loc - tuple formatted (row, col)
		'''
		try:
			row, col = random.choice(self.getEmptyTiles())
			self.board[row][col] = 2 if random.random() < self.prob else 4
			return True
		except:
			return False

	@staticmethod
	def shiftLeft(board, test=False):
		'''
		Moves every element in the board all the way to the LEFT

		returns: new board with elements shifted LEFT
		'''
		newBoard = [row for row in board]
		newBoard = [filter(lambda x: x!=0, row) for row in newBoard]
		for row in newBoard :
			while len(row) != len(newBoard) :
				changed = True
				row.append(0)
		if not test or newBoard != board:
			return newBoard
		else :
			raise InvalidMoveError

	@staticmethod
	def shiftRight(board):
		'''
		Moves every element in the board all the way to the RIGHT

		returns: new board with elements shifted RIGHT
		'''
		newBoard = [row for row in board]
		newBoard = [filter(lambda x: x!=0, row) for row in newBoard]
		for row in newBoard :
			while len(row) != len(newBoard) :
				row.insert(0, 0)
		return newBoard

	@staticmethod
	def mergeLeft(board, currentScore):
		'''
		Merges identical values favoring the LEFT

		returns: the new board, new score
		'''
		for row in board:
			for i in range(len(row)-1):
				if row[i] == row[i+1] :
					currentScore += row[i]*2
					row[i] = row[i]*2
					row[i+1] = 0
		return board, currentScore


	@staticmethod
	def mergeRight(board, currentScore):
		'''
		Merges identical values favoring the RIGHT

		returns: the new board, new score
		'''
		for row in board:
			for i in range(len(row)-1)[::-1]:
				if row[i] == row[i+1] :
					currentScore += row[i]*2
					row[i+1] = row[i+1]*2
					row[i] = 0
		return board, currentScore

	@staticmethod
	def invert(board):
		newBoard = []
		for i in range(len(board)):
			newBoard.append([row[i] for row in board])
		return newBoard

	def slide(self, direction, addTile=True):
		'''
		Makes a move in the game and adds a tile if addTile is
		True

		returns: True if a move was made, else False
		'''
		compareBoard = [row for row in self.board]
		if direction == 'left' or direction == 'l':
			self.board = self.shiftLeft(self.board)
			self.board, self.score = self.mergeLeft(self.board, self.score)
			self.board = self.shiftLeft(self.board)
		elif direction == 'right' or direction == 'r':
			self.board = self.shiftRight(self.board)
			self.board, self.score = self.mergeRight(self.board, self.score)
			self.board = self.shiftRight(self.board)
			if compareBoard != self.board and addTile:
				self.addTile()
		elif direction == 'up' or direction == 'u':
			invertedBoard = self.invert(self.board)
			invertedBoard = self.shiftLeft(invertedBoard)
			invertedBoard, self.score = self.mergeLeft(invertedBoard, self.score)
			invertedBoard = self.shiftLeft(invertedBoard)
			self.board = self.invert(invertedBoard)
			if compareBoard != self.board and addTile:
				self.addTile()
		elif direction == 'down' or direction == 'd':
			invertedBoard = self.invert(self.board)
			invertedBoard = self.shiftRight(invertedBoard)
			invertedBoard, self.score = self.mergeRight(invertedBoard, self.score)
			invertedBoard = self.shiftRight(invertedBoard)
			self.board = self.invert(invertedBoard)
			if compareBoard != self.board and addTile:
				self.addTile()
		if compareBoard != self.board and addTile:
			self.addTile()
		else:
			raise InvalidMoveError

