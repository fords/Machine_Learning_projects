import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        else:
            det  = self.g[0][0] * self.g[1][1] - self.g[0][1] * self.g[1][0]
            
        return det

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")        
        else:
            trace = 0
            for i in range(self.h):
                trace += self.g[i][i]
        return trace
    
    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        inv = identity(self.h)
        if self.h == 1:
            inv[0][0] = 1/ self[0][0]
        elif self.h == 2:
            detA = self[0][0] * self[1][1] - self[0][1] * self[1][0]
            if detA == 0:
                raise(ValueError, "Matrix does not have an inverse.")
            else:
                inv[0][0] = (1 / detA) * self.g[1][1]
                inv[0][1] = (-1 / detA) * self.g[0][1]
                inv[1][0] = (-1 / detA) * self.g[1][0]
                inv[1][1] = (1 / detA) * self.g[0][0]
        return inv      

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        Transpose = []
        for i in range(self.w):
            Transpose_row = []
            for j in range(self.h):
                Transpose_row.append(self.g[j][i])
            Transpose.append(Transpose_row)
        return Matrix(Transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        add_result = []
        for i in range(self.h):
            add_result_row = []
            for j in range(self.w):
                add_result_row.append(self.g[i][j] + other.g[i][j])
            add_result.append(add_result_row)
            
        return Matrix(add_result)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        neg = []
        for i in range(self.h):
            neg_row = []
            for j in range(self.w):
                neg_row.append(-1 * self.g[i][j])
            neg.append(neg_row)
        return Matrix(neg)
        
    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        sub = []
        for i in range(self.h):
            sub_row = []
            for j in range(self.w):
                sub_row.append(self.g[i][j] - other.g[i][j])
            sub.append(sub_row)
        return Matrix(sub)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        mul = []
        
        def dotproducts( Mat1, Mat2):
            sum = 0
            for i in range(len(Mat1)):
                sum += Mat1[i] * Mat2[i]
            return sum
        
        def get_row( matrix, row_index):
            return matrix[row_index]
        
        def get_column( matrix, col_index):
            col = []
            for i in range(len(matrix)):
                col.append(matrix[i][col_index])
            return col
        
        MatA_row = self.h
        MatB_col = other.w
        
        for i in range(MatA_row):
            mul_row = []
            for j in range(MatB_col):
                mul_row.append( dotproducts( get_row(self.g,i), get_column(other.g,j)) )
            mul.append(mul_row)
            
        return Matrix(mul)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            rmul = []
            for i in range(self.h):
                rmul_row = []
                for j in range(self.w):
                    rmul_row.append(other * self.g[i][j])
                rmul.append(rmul_row)
            return Matrix(rmul)
            