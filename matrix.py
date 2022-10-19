'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''
class Matrix(object):
    def __init__(self, matrix = []):
        self.matrix = matrix
        
    def __matmul__(self, matrix_B):
        res = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]

        # multiply matrix
        for i in range(len(self.matrix)):
            for j in range(matrix_B.len()):
                for k in range(matrix_B.len()):
                    if isinstance(matrix_B.matrix[0], int) or isinstance(matrix_B.matrix[0], float):
                        res[i][j] += self.matrix[i][k] * matrix_B.matrix[k]
                    elif isinstance(self.matrix[0], int) or isinstance(self.matrix[0], float):
                        res[i][j] += self.matrix[k] * matrix_B.matrix[k][j]
                    else:
                        res[i][j] += self.matrix[i][k] * matrix_B.matrix[k][j]
                        
        return Matrix(res)
    
    def len(self):
        return len(self.matrix)