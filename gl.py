'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''
from math import cos, sin
from colors import *
from vectors import *
from matrix import *
import struct
import random

def char(c):
    # 1 bytes
    return struct.pack('=c', c.encode('ascii'))
    
def word(w):
    # 2 bytes
    return struct.pack('=h', w)
    
def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.InX = 0
        self.InY = 0
        self.current_color = RED
        self.VP_Color = RED
        self.background_Color = BLACK
        self.Model = None
        self.View = None
        self.active_vertex_array = []
        self.active_shader = None
        self.active_texture = None
        self.light = V3(0, 0, 1)
        self.glViewPort(0,0, self.width, self.height)
        self.glClear()
        
    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)
        
        translation_matrix = Matrix([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0,           1]
        ])
        
        scale_matrix = Matrix([
            [scale.x,       0,       0, 0],
            [      0, scale.y,       0, 0],
            [      0,       0, scale.z, 0],
            [      0,       0,       0, 1]
        ])
        
        anx = rotate.x
        rotation_x = Matrix([
            [1,        0,         0, 0],
            [0, cos(anx), -sin(anx), 0],
            [0, sin(anx),  cos(anx), 0],
            [0,        0,         0, 1]
        ])
        
        anty = rotate.y
        rotation_y = Matrix([
            [ cos(anty), 0, sin(anty), 0],
            [        0,        1, 0, 0],
            [-sin(anty), 0, cos(anty), 0],
            [        0,        0, 0, 1]
        ])
        
        anz = rotate.z
        rotation_z = Matrix([
            [cos(anz), -sin(anz), 0, 0],
            [sin(anz),  cos(anz), 0, 0],
            [       0,         0, 1, 0],
            [       0,         0, 0, 1]
        ])
            
        rotation_matrix = rotation_x @ rotation_y @ rotation_z

        self.Model = translation_matrix @ rotation_matrix @ scale_matrix
    
    def loadViewMatrix(self, x, y, z, center):
        Mi = Matrix([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [  0,   0,   0, 1]
        ])
        
        Op = Matrix([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0,         1]
        ])
        
        self.View = Mi @ Op
        
    def loadProjectionMatrix(self, eye, center):
        coeff = -1/(eye.length()-center.length())
        self.Projection = Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ])
        
    def loadViewportMatrix(self):
        x = 0
        y = 0
        w = self.width/2
        h = self.height/2
        
        self.ViewPort = Matrix([
            [w, 0, 0, x + w],
            [0, h, 0, y + h],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]) 
    
    def lookAt(self, eye, center, up):
        z = (eye - center).norm() 
        x = (up * z).norm()
        y = (z * x).norm()
        
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(eye, center)
        self.loadViewportMatrix()

    def write(self, filename):
        f = open(filename, 'bw')
    
        #pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))
        
        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        #pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
                
        f.close()
        
    def glpoint(self, x, y, colorp=None):
        xComp = (x > 0 & x < self.width)
        yComp = (y > 0 & y < self.height)
        
        if(xComp & yComp):
            self.framebuffer[y][x] = colorp or self.current_color
        
    #Funciones

    #Inicializar framebuffer con un tamaño
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    #Area de la imagen sobre la que se dibujara
    def glViewPort(self, x, y, width, height):
        self.InX = x
        self.InY = y
        self.ViewPW = width
        self.ViewPH = height

    #Llenar mapa de bits de un color
    def glClear(self):
        self.framebuffer = [
            [self.background_Color for x in range(self.width)]
            for y in range(self.height)
        ]
        
        self.zBuffer = [
            [-9999 for x in range(self.width)]
            for y in range(self.height)
        ]
        
    def glViewPortFM(self, colorp = None):
        ExtremoA = self.InX + self.ViewPW
        ExtremoB = self.InY + self.ViewPH
        
        for a in range(self.InX, ExtremoA):
            for b in range(self.InY, ExtremoB):
                self.glpoint(a,b,colorp or WHITE)

    #Cambiar color glClear
    def glClearColor(self, r, g, b):
        NewColor = colorT(r, g, b)
        self.background_Color = NewColor
        self.glClear()
        
    #Cambiar color punto en la pantalla
    def glVertex(self, x, y, colorp=None):
        xComp = (x > 1 or x < -1)
        yComp = (y > 1 or y < -1)
         
        if (xComp or yComp):
            print('Fuera de rango')
        else:
            if (x == 1):
                x -= 0.0001
            elif (x == -1):
                x += 0.0001   
            elif (y == 1):
                y -= 0.0001
            elif (y == -1):
                y += 0.0001 
            
            x2 = (x + 1) * round(self.ViewPW/2) + self.InX
            y2 = (y + 1) *round(self.ViewPH/2) + self.InY

            self.glpoint(round(x2), round(y2), colorp or self.VP_Color)

    #Cambiar color glVertex
    def glColor(self, r, g, b):
        self.VP_Color = colorT(r, g, b)
        
    def glLine(self, x0, y0, x1, y1, colorp=None):
        
        xComp = (x0 > 1 or x0 < -1 or x1 > 1 or x1 < -1)
        yComp = (y0 > 1 or y0 < -1 or y1 > 1 or y1 < -1)
        
        if (xComp or yComp):
            print('Fuera de rango')
            
        else:
            x0 = (x0 + 1) * round(self.ViewPW/2) + self.InX
            y0 = (y0 + 1) *round(self.ViewPH/2) + self.InY
            x1 = (x1 + 1) * round(self.ViewPW/2) + self.InX
            y1 = (y1 + 1) *round(self.ViewPH/2) + self.InY
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        limEm = dy > dx
        
        if (limEm):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
            
        count = 0
        lim = round(dx)
        y = round(y0)
        
        for x in range (round(x0), round(x1)+1):
            
            if limEm:
                self.glpoint(round(y),round(x), colorp)
            else: 
                self.glpoint(round(x),round(y), colorp) 
            
            count += dy * 2
            if (count >= lim): 
                if (y0 < y1):
                    y += 1
                else:
                    y -= 1
                lim += dx * 2   
                
    def line(self, A, B, colorp=None):
        
        x0 = round(A.x)
        y0 = round(A.y)
        x1 = round(B.x)
        y1 = round(B.y)
        
        if ((x0 == x1) and (y0 == y1)):
            self.glpoint(x0, y0,colorp)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        limEm = dy > dx
        
        if (limEm):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
            
        count = 0
        lim = dx
        y = y0
        
        for x in range (x0, x1+1):
            if limEm:
                self.glpoint(x, y, colorp)
            else: 
                self.glpoint(y, x, colorp) 
            
            count += dy * 2
            if (count >= lim): 
                if (y0 < y1):
                    y += 1
                else:
                    y -= 1
                lim += dx * 2 
                
    def shader(self, **kwargs):
        w, u, v = kwargs['bar']
        Li = kwargs['light']
        A, B, C = kwargs['vertices']
        tA, tB, tC = kwargs['texture_coords']
        nA, nB, nC = kwargs['normals']
        
        iA = nA.norm() @ Li.norm()
        iB = nB.norm() @ Li.norm()
        iC = nC.norm() @ Li.norm()
        
        i = (iA * w) + (iB * u) + (iC * v)
        
        if self.active_texture:
            
            tx = tA.x * w + tB.x * u * tC.x * v
            ty = tA.y * w + tB.y * u * tC.y * v
            
            return self.active_texture.get_color_with_intensity(tx, ty, i)
        
    #Escribir imagen 
    def glFinish(self):
        self.write('a.bmp')
        
#Iniciar objeto interno
def glinit():
    return Render(1024, 1024)

def neptuno(**kwargs):
    x, y = kwargs['coors']
    w, u, v = kwargs['bar']
    Li = kwargs['light']
    nA, nB, nC = kwargs['normals']
        
    iA = nA.norm() @ Li.norm()
    iB = nB.norm() @ Li.norm()
    iC = nC.norm() @ Li.norm()
    
    i = (iA * w) + (iB * u) + (iC * v)
    
    #772 tope superior
    #252 tope inferior
    
    #239 tope izquierdo
    #761 tope derecho

    if 700 + random.randint(0, 20) <= y <= 772: 
        if 290 - random.randint(0, 30) <= x <= 761 - random.randint(5, 15):
            return color(99, 87, 64)  
                
    elif 630 + random.randint(0, 20) <= y <= random.randint(710, 750):
        if 290 - random.randint(0, 50) <= x <= 761 - random.randint(0, 80):
            return color(110, 97, 69)  
        
    elif 550 + random.randint(0, 20) <= y <= 700 - random.randint(0, 15):
        if 239 + random.randint(0, 30) <= x <= 250 + random.randint(250, 450):
            return color(110, 97, 69)  
        
        elif 239 <= x <= 550 + random.randint(200, 300):
            r = random.randint(127, 135)
            g = random.randint(115, 126)
            b = random.randint(83, 85)
            return color(r, g, b)  
        
    elif 470 + random.randint(0, 20) <= y <= random.randint(600, 620):
        if 239 <= x <= 250 + random.randint(250, 450):
            r = random.randint(89, 95)
            g = random.randint(74, 78)
            b = random.randint(55, 59)
            return color(r, g, b)  
    
        elif 440 + random.randint(0, 20) <= y <= random.randint(530, 570):
            if 239 + random.randint(20, 40) <= x <= 550 + random.randint(100, 260):
                r = random.randint(67, 73)
                g = random.randint(57, 62)
                b = random.randint(39, 44)
                return color(r, g, b)  
         
    elif 400 + random.randint(0, 20) <= y <= random.randint(480, 570):
        if 239 <= x <= 250 + random.randint(250, 450):
            r = random.randint(127, 135)
            g = random.randint(115, 126)
            b = random.randint(83, 85)
            return color(r, g, b) 
        
        elif 239 + random.randint(0, 40) <= x <= 350 + random.randint(300, 560):
            r = random.randint(89, 95)
            g = random.randint(74, 78)
            b = random.randint(55, 59)
            return color(r, g, b) 
        
    elif 330 - random.randint(0, 20) <= y <= random.randint(410, 560):
        
        if 239 <= x <= random.randint(250, 260):
            return color(99, 87, 64) 
        
        elif 239 + random.randint(0, 20) <= x <= 250 + random.randint(300, 560):
            return color(110, 97, 69) 
        
    elif 320 - random.randint(0, 5) < y < 325 + random.randint(0, 5):
        r = random.randint(127, 135)
        g = random.randint(115, 126)
        b = random.randint(83, 85)
        return color(r, g, b)  
        
    elif 252 <= y <= 320 + random.randint(0, 20): 
        if 290 - random.randint(0, 30) <= x <= 761 - random.randint(5, 15):
            return color(99, 87, 64)   
            
    r = random.randint(140, 150)
    g = random.randint(130, 145)
    b = random.randint(100, 122)

    return color(r, 136, b) 