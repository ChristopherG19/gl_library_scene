'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''
from math import trunc

def colorT(r, g, b):
    if ((r >= 0 and r <= 1) and (g >= 0 and g <= 1) and (b >= 0 and b <= 1)):
        r = trunc(r * 255)
        g = trunc(g * 255)
        b = trunc(b * 255)
    else: 
        print("Ingreso invalido. Valores entre 0 y 1 estan permitidos")    
    
    return bytes([b, g, r])

def color(r, g, b):
    return bytes([b, g, r])

WHITE = colorT(1, 1, 1)
BLACK = colorT(0, 0, 0)
RED = colorT(1, 0, 0)
BLUE = colorT(0, 0, 1)
GREEN = colorT(0, 1, 0)
YELLOW = colorT(1,0.898,0.486)