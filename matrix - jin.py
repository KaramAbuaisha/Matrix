## TODO:
## - Revise matrix coordinate system so that they begin at 1, not 0
## - Figure out how to do Gauss-Jordan Elimination
## - Use algorithm to find rows and columns with most zeroes for cofactor expansion

def isMatrix(inp):				# checks if a list is a matrix
	nColumns = len(inp[0])
	for i in range(len(inp)):
		if len(inp[i]) != nColumns:
			return False
	return True

class matrix:
	"""Implements matrices and matrix operations in Python."""
	version = "0.1"
	
	## -- SETUP AND INFORMATION FUNCTIONS --
	def __init__(self, input = None, nRows = 1, nColumns = 1):
		self.contents = [[None for i in range(nColumns)] for n in range(nRows)]
		if input != None:
			if isMatrix(input):
				self.nRows = len(input)
				self.nColumns = len(input[0])
				self.populate(input)
			else:
				raise Exception("Input is not matrix.")
		else:
			self.nRows = nRows
			self.nColumns = nColumns
	def __str__(self):
		out = "~ "
		for row in self.contents:
			out += "[ "
			for element in row:
				if element == None:
					out += "_ "
				elif isinstance(element, int) or isinstance(element, float):
					out += str(element) + " "
				else:
					out += "\"" + str(element) + "\" "
			out += "]\n  "
		return out
	def access(self, row = None, col = None):			# Access a matrix value.	
		"""To access an entire row or column, use keywords `row` or `col`."""
		try:
			if row != None and col != None:
				return self.contents[row][col]
			elif row != None and col == None:	# Access row
				return self.contents[row]
			elif col != None and row == None:	# Access column
				out = []
				for viewedRow in self.contents:
					out.append(viewedRow[col])
				return out
			else:
				return self.contents[0][0]
		except IndexError:
			print("Out of bounds.")
	def assign(self, row, column, value):	# Assign or change a value
		try:
			self.contents[row][column] = value
		except IndexError:
			print("Out of bounds.")
		return
	def populate(self, inp):				# Populate entire matrix at once
		# if matrix
		if isinstance(inp, matrix):
			if inp.nRows == self.nRows and inp.nColumns == self.nColumns:
				self.contents = inp.contents
			else:
				print("Dimension mismatch.")
				return
		# if list
		elif isinstance(inp, list):
			if isMatrix(inp):
				if len(inp) == self.nRows:
					for row in inp:
						if len(row) != self.nColumns:
							print("Dimension mismatch.")
							return
					self.contents = inp
				else:
					print("Out of bounds.")
				return
			else:
				print("List is not a matrix.")
		return
			
	## -- MATRIX OPERATIONS --
	def minor(self, deletedRow, deletedColumn):
		if self.nRows == 1 and self.nColumns == 1:
			return self.contents
		minor = self.contents[:]
		del minor[deletedRow]
		for row in minor:
			del row[deletedColumn]
		return minor
	def determinant(self):
		# Check if square matrix
		if self.nRows != self.nColumns:
			return None
		# If 1x1 matrix
		elif self.nRows == 1 and self.nColumns == 1:
			return self.access(0, 0)
		# 2x2 base case
		elif len(self.contents) == 2:
			return self.access(0, 0) * self.access(1, 1) - self.access(1, 0) * self.access(0, 1)
		# recursive case
		else:
			# cofactor expansion on first column:
			det = 0
			for row in range(self.nRows):
				det += self.minor(row, 0).determinant() * (-1)**(row + 1 + 1)
			return det
			
	## -- <UNTESTED> --
	# matrix multiplication?
	# self * other
	def __mul__(self, other):
		if isinstance(other, matrix) and self.xDim == other.yDim:
			result = Matrix(self.yDim, other.xDim)
			for n in range(self.xDim):
				pass
				# continue
				
	## -- GAUSS-JORDAN ELIMINATION --
	# R1 <-> R2
	def rowSwap(self, row1, row2, verbose = False):
		self.contents[row1], self.contents[row2] = self.contents[row2], self.contents[row1]
		if verbose:
			print(self, end = "")
			print("R" + str(row1) + " <-> R" + str(row2))
			print()
	# R1 -> k*R1
	def rowMult(self, row, k, verbose = False):
		for n in range(0, len(self.contents[row])):
			self.contents[row][n] *= k
		if verbose:
			print(self, end = "")
			print("R" + str(row) + " -> " + str(k) + "R" + str(row))
			print()
	# R1 -> R1 + k*R2
	def rowAdd(self, rowAdded, rowTarget, k = 1, verbose = False):
		for n in range(0, len(self.contents[rowTarget])):
			self.contents[rowTarget][n] += self.contents[rowAdded][n] * k
		if verbose:
			print(self, end = "")
			if k == 1:
				print("R" + str(rowTarget) + " -> " + "R" + str(rowTarget) + " + R" + str(rowAdded))
				print()
			elif k > 0:
				print("R" + str(rowTarget) + " -> " + "R" + str(rowTarget) + " + " + str(k) + "R" + str(rowAdded))
				print()
			elif k < 0:
				print("R" + str(rowTarget) + " -> " + "R" + str(rowTarget) + " - " + str(-k) + "R" + str(rowAdded))
				print()
				
## -- TEST CODE --
if __name__ == "__main__":
	a = matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
	print(a)
	print(a.minor(0, 0))
