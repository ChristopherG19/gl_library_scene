'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''

def matrix_multiplication(matrix_A, matrix_B):
    res = [[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]]

    # multiply matrix
    for i in range(len(matrix_A)):
        for j in range(len(matrix_B or matrix_B[0])):
            for k in range(len(matrix_B)):
                if isinstance(matrix_B[0], int):
                    res[i][j] += matrix_A[i][k] * matrix_B[k]
                else:
                    res[i][j] += matrix_A[i][k] * matrix_B[k][j]
    
    return res

def matrix_multiplication4(matrix_A, matrix_B):
    res = [[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]
    ]

    # multiply matrix
    for i in range(len(matrix_A)):
        for j in range(len(matrix_B)):
            for k in range(len(matrix_B)):
                if isinstance(matrix_B[0], int) or isinstance(matrix_B[0], float):
                    res[i][j] += matrix_A[i][k] * matrix_B[k]
                elif isinstance(matrix_A[0], int) or isinstance(matrix_A[0], float):
                    res[i][j] += matrix_A[k] * matrix_B[k][j]
                else:
                    res[i][j] += matrix_A[i][k] * matrix_B[k][j]

    return res