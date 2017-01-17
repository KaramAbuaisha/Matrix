import copy

#Matrix Operations
def dotprod(v1, v2):
  prod = 0
  for i in range(len(v1)):
    prod += v1[i] * v2[i]
  return prod

def multiply(m1, m2):
  if len(m1) != len(m2[0]) and len(m1[0]) != len(m2):
    return False
  else:
    multiplied = [[None for _ in range(len(m2[0]))] for _ in range(len(m1))]
    m2 = m2.transpose()
    for row in range(len(m1)):
      for col in range(len(m2[0])):
        multiplied[row][col] = dotprod(m1[row], m2[col])

#Matrix Object
class Matrix:
  def __init__(self, vals):
    self.vals = vals
    self.size = range(len(self.vals))
  
  #Equal Size Empty Matrix
  def _empty(self):
    size = len(self.vals)
    return [[0 for _ in range(size)] for _ in range(size)]
  
  #Transpose
  def transpose(self):
    matrix = copy.deepcopy(self.vals)
    transposed = self._empty()
    for i in self.size:
      for j in self.size:
        transposed[i][j] = matrix[j][i]
    return transposed
  
  #Row Echelon Form
  def ref(self):
    matrix = copy.deepcopy(self.vals)
    #Check for recursion stop, return self
    if len(matrix) == 1:
      return matrix[0][0]
    
    #Row reduce current column
    for row in matrix[1:]:
      
      #prevent division by zero
      if row[0] != 0:
        #create pivot to make first terms 0
        pivot = row[0] / matrix[0][0]
        for col in range(len(row)):
          row[col] = row[col] - pivot * matrix[0][col]
          if row[col] % 1 == 0:
            row[col] = int(row[col])

    #Create submatrix for recursion
    sub = Matrix([row[1:] for row in matrix[1:]])

    #Reapply function to submatrix
    sub = sub.ref()
  
    if type(sub) == float or type(sub) == int:
      matrix[1][1] = sub
      return matrix
    else:
      for i in range(len(sub)):
        sub[i] = [0] + sub[i]
  
    return [matrix[0]] + sub
  
  #Reduced Row Echelon Form
  def rref(self):
    matrix = Matrix(copy.deepcopy(self.vals))
    matrix = Matrix(matrix.ref())
    matrix = Matrix(matrix.transpose())
    matrix = Matrix(matrix.ref())
    return matrix.vals
  
  #Determinant
  def det(self):
    matrix = Matrix(copy.deepcopy(self.vals))
    if matrix.ind() == False:
      return 0
    matrix = matrix.ref()
    determinant = 1
    for i in range(len(matrix)):
      determinant = determinant * matrix[i][i]
    return determinant
  
  #Is Independent
  def ind(self):
    matrix = Matrix(copy.deepcopy(self.vals))
    matrix = matrix.ref()
    for i in range(len(matrix)):
      if matrix[i][i] == 0:
        return False
    return True
  
  #Single Cofactor
  def cof(self, row, col):
    sub = copy.deepcopy(self.vals)
    sub.pop(row)
    for i in sub:
      i.pop(col)
    sub = Matrix(sub)
    return sub.det()
  
  #Cofactor Matrix
  def cofmat(self):
    cofactors = self._empty()
    for row in self.size:
      for col in self.vals[row]:
        cofactors[row][col] = self.cof(row, col)
    return cofactors
  
  #Invert
  #Non-Functional
  def inverse(self):
    
    #Fron ref method
    matrix = copy.deepcopy(self.vals)
    inverted = Diag([1 for _ in range(len(matrix))])
    #Check for recursion stop, return self
    if len(matrix) == 1:
      return matrix[0][0]
    
    for col in self.size:
      matrix[0][col] = matrix[0][col] / matrix[0][0]
      inverted.vals[0][col] = inverted.vals[0][col] / matrix[0][0]
    
    #Row reduce current column
    for row in matrix[1:]:
      
      #prevent division by zero
      if row[0] != 0:
        #create pivot to make first terms 0
        for col in range(len(row)):
          row[col] = row[col] - row[0] * matrix[0][col]

    #Create submatrix for recursion
    sub = Matrix([row[1:] for row in matrix[1:]])

    #Reapply function to submatrix
    sub = sub.ref()
  
    if type(sub) == float:
      matrix[1][1] = sub
      return matrix
    else:
      for i in range(len(sub)):
        sub[i] = [0] + sub[i]
  
    return [matrix[0]] + sub
  
  #System Solve
  def solve(self, vector):
    return 0
  
  #Simple Solve for 1 Variable (Cramer's Rule)
  def cramsolve(self, vector, term):
    return 0
  
  #Rank
  def rank(self):
    numpivots = 0
    for i in range(len(self.vals)):
      if self.vals[i][i] != 0:
        numpivots += 1
    return numpivots
  
  #Formatted Printing
  def printmat(self):
    matrix = copy.deepcopy(self.vals)
    #BiggestNum
    big = 0
    printed = [''  for _ in self.size]
    for row in self.vals:
      for col in row:
        if len(str(col)) > big:
          big = col
    if big < 0:
      longest = len(str(big)) - 1
    else:
      longest = len(str(big))
    
    for row in self.size:
      for col in self.size:
        if matrix[row][col] < 0:
          num = str(matrix[row][col])
        else:
          num = ' ' + str(matrix[row][col])

        printed[row] += ' ' * (longest - len(num) + 1) + num + ' ' 
      printed[row] = printed[row][longest - len(str(matrix[row][0])):len(printed[row]) - 1] + ' ]'
    
    for row in printed:
      print('[' + row)
      
    return None

#Diagonal Matrix
class Diag(Matrix):
  def __init__(self, vals):
    self.vals = vals
    Matrix.__init__(self, self.__populate())
  
  def __populate(self):
    size = len(self.vals)
    diagmat = self._empty()
    for i in range(size):
      diagmat[i][i] = self.vals[i]
    return diagmat

#x = Matrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
x = Matrix([[1,2,3],[4,5,6],[7,8,9]])
x.printmat()
print('\n')
x = Matrix(x.ref())
x.printmat()
