'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''

from gl import *
from colors import *
from objects3d import *

from shapes import *
#Clase 11/08/2022
class Texture:
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        with open(self.path, "rb") as image:
            image.seek(2 + 4 + 2 + 2)
            header_size = struct.unpack("=l", image.read(4))[0]    
            image.seek(2 + 4 + 2 + 2 + 4 + 4)
            self.width = struct.unpack("=l", image.read(4))[0]    
            self.height = struct.unpack("=l", image.read(4))[0]    
            
            image.seek(header_size)
            
            self.pixels = []
            for x in range(self.width):
                self.pixels.append([])
                for y in range(self.height):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[x].append(
                        color2(r, g, b)
                    )
    
    def get_color(self, tx, ty):
        x = round(tx * self.width)
        y = round(ty * self.height)
        
        return self.pixels[y][x]
    
    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)
        
        #Revisar estos colores (progra defensiva ante valores mayores 255 o menores 0)
        b = round(self.pixels[y][x][0] * intensity)
        g = round(self.pixels[y][x][1] * intensity)
        r = round(self.pixels[y][x][2] * intensity)
        
        return color2(
            max(min(r, 255), 0), 
            max(min(g, 255), 0), 
            max(min(b, 255), 0)
        )
    
'''
r = Render(1024, 1024)
t = Texture('./Models/helmet.bmp')
r.framebuffer = t.pixels
r.write("Vista.bmp")
  
r = Render(1024, 1024)
t = Texture('./model.bmp')
#print(t.get_color_with_intensity(0, 0, 1))

r.framebuffer = t.pixels

cube = Obj('./model.obj')
r.current_color = WHITE

for face in cube.caras:
                
    if (len(face) == 4):
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1
        f4 = face[3][1] - 1
        
        vt1 = V3(
            cube.tvertices[f1][0] * t.width,
            cube.tvertices[f1][1] * t.height
        )
        vt2 = V3(
            cube.tvertices[f2][0] * t.width,
            cube.tvertices[f2][1] * t.height
        )
        vt3 = V3(
            cube.tvertices[f3][0] * t.width,
            cube.tvertices[f3][1] * t.height
        )
        vt4 = V3(
            cube.tvertices[f4][0] * t.width,
            cube.tvertices[f4][1] * t.height
        )

        triangule(vt1, vt2, vt3)
        triangule(vt1, vt3, vt4)

    if (len(face) == 3):
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1
        
        vt1 = V3(
            cube.tvertices[f1][0] * t.width,
            cube.tvertices[f1][1] * t.height
        )
        vt2 = V3(
            cube.tvertices[f2][0] * t.width,
            cube.tvertices[f2][1] * t.height
        )
        vt3 = V3(
            cube.tvertices[f3][0] * t.width,
            cube.tvertices[f3][1] * t.height
        )
    
        triangule(vt1, vt2, vt3)
        
r.write("t.bmp")
'''