class Token:
	def __init__(self, line, col, tok):
		self.token = tok
		self.line = line
		self.col = col