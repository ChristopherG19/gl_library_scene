'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''

from gl import *
from colors import *
from vectors import *
from matrix import *
from objects3d import Obj

#SR2
def house(r):
    #Base
    r.glLine(-0.5, 0.49, 0, 0.49, RED)
    r.glLine(-0.5, -0.5, -0.5, 0.49, RED)
    r.glLine(-0.3, -0.7, -0.5, -0.5, RED)
    r.glLine(0.19, -0.68, -0.305, -0.68, RED)
    r.glLine(-0.5, -0.5, 0, -0.5, RED)
    #Techo
    r.glLine(0.2, -0.7, 0, -0.5, BLUE)
    r.glLine(0, 0.499, 0, -0.5, BLUE)
    r.glLine(0.001, 0.499, 0.5, -0.001, BLUE)
    r.glLine(0, -0.5, 0.5, 0, BLUE)
    r.glLine(0.61, -0.2, 0.19, -0.68, BLUE)
    r.glLine(0.61, -0.2, 0.5, 0, BLUE)
    #Puerta
    r.glLine(-0.5, -0.1, -0.5, 0.1, GREEN)
    r.glLine(-0.5, -0.1, -0.25, -0.1, GREEN)
    r.glLine(-0.5, 0.1, -0.25, 0.1, GREEN)
    r.glLine(-0.25, -0.1, -0.25, 0.1, GREEN)
    
#LAB_01: Rellenar polígonos
pol1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), 
        (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
pol2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
pol3 = [(377, 249), (411, 197), (436, 249)]
pol4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37),
        (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214),
        (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
pol5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

#Función para dibujar cualquier polígono
def DrawPoligons(r, puntos):
    #--> Forma extensa: 
    sizeP = len(puntos)
    count = 0
    while (count != sizeP):
        if (count == sizeP-1):
            x0 = puntos[sizeP-1][0]
            y0 = puntos[sizeP-1][1]
            x1 = puntos[0][0]
            y1 = puntos[0][1]
            A = V2(y0,x0)
            B = V2(y1,x1)
            r.line(A, B, r.background_Color) 
        elif (count < sizeP-1):
            x0 = puntos[count][0]
            y0 = puntos[count][1]
            x1 = puntos[count+1][0]
            y1 = puntos[count+1][1]
            A = V2(y0,x0)
            B = V2(y1,x1)
            r.line(A, B, r.background_Color) 
        count += 1
    
def Center(puntos):
    centro = (0,0)
    x = 0
    y = 0
    for punto in range(0, len(puntos)):
        x += puntos[punto][0]
        y += puntos[punto][1]
    x = round(x/len(puntos))
    y = round(y/len(puntos))
    centro = (x,y)
    return centro
    
def InsidePoligon(x, y, puntos, sizeP, PuntoInicial):
    PuntoDentro = False
    x0, y0 = PuntoInicial
    for i in range(sizeP+1):
        x1, y1 = puntos[i % sizeP]
        if (y > min(y0, y1)):
            if (y <= max(y0, y1)):
                if (x <= max(x0, x1)):
                    xDentro = (y-y0)*(x1-x0)/(y1-y0)+x0 if (y0 is not y1) else 0
                    PuntoDentro = not PuntoDentro \
                        if (x0 == x1 or x <= xDentro) else PuntoDentro
                    
        x0, y0 = x1, y1
    return PuntoDentro
    
def FillPoligons(r, puntos, colorp):
    sizeP = len(puntos)
    for x in range(r.width):
        for y in range(r.height):
            if(InsidePoligon(x,y,puntos,sizeP, puntos[0])):
                r.glpoint(x, y, colorp or WHITE)

def boundingB(*vertices):
    coords = [ (vertex.x, vertex.y) for vertex in vertices ]
    
    xmin = 999999
    xmax = -999999
    ymin = 999999
    ymax = -999999
    
    for (x,y) in coords:
        if (x < xmin):
            xmin = x
        if (x > xmax):
            xmax = x
        if (y < ymin):
            ymin = y
        if (y > ymax):
            ymax = y

    return V3(xmin, ymin), V3(xmax, ymax)

def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    if (abs(cz) <= 0):
        return (-1, -1, -1)
    
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)
    
    return (w, v, u)
    
def transformT(vertex, scale, translate):
    return V3(
        (vertex[0] * scale[0]) + translate[0],
        (vertex[1] * scale[1]) + translate[1],
        (vertex[2] * scale[2]) + translate[2]
    )
    
def transform(r, vertex):
    aumented_vertex = Matrix([
        vertex[0],
        vertex[1],
        vertex[2],
        1
    ])

    # temp_Transformed_vertex = matrix_multiplication4(r.Model, aumented_vertex)
    # temp_Transformed_vertex2 = matrix_multiplication4(r.View, temp_Transformed_vertex)
    # temp_Transformed_vertex3 = matrix_multiplication4(r.Projection, temp_Transformed_vertex2)
    # temp_Transformed_vertex4 = matrix_multiplication4(r.ViewPort, temp_Transformed_vertex3)

    transformed_vertex_temp = r.View @ r.Model @ aumented_vertex
    # transformed_vertex_temp = r.ViewPort @ r.Projection @ r.View @ r.Model @ aumented_vertex

    transformed_vertex = []
    for i in transformed_vertex_temp.matrix:
        transformed_vertex.append(i[0])

    # print(transformed_vertex)

    return V3(
        transformed_vertex[0] / transformed_vertex[3],
        transformed_vertex[1] / transformed_vertex[3],
        transformed_vertex[2] / transformed_vertex[3]    
    )
    
def load_modelR(r, t, filename, tf=(0, 0, 0), s=(1, 1, 1), rotate=(0, 0, 0)):
    r.loadModelMatrix(tf, s, rotate)
    cube = Obj(filename)
    for face in cube.caras:       
        if(len(face) == 4):
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            f4 = face[3][0] - 1
            
            v1 = transform(r, cube.vertices[f1])
            v2 = transform(r, cube.vertices[f2])
            v3 = transform(r, cube.vertices[f3])
            v4 = transform(r, cube.vertices[f4])
            
            if (r.active_texture):
                ft1 = face[0][1] - 1
                ft2 = face[1][1] - 1
                ft3 = face[2][1] - 1
                ft4 = face[3][1] - 1
                
                vt1 = V3(*cube.tvertices[ft1])
                vt2 = V3(*cube.tvertices[ft2])
                vt3 = V3(*cube.tvertices[ft3])
                vt4 = V3(*cube.tvertices[ft4])

                trianguleR(r,
                    (v1, v2, v3),
                    t,
                    (vt1, vt2, vt3)
                )

                trianguleR(r,
                    (v1, v3, v4),
                    t,
                    (vt1, vt3, vt4)
                )
            else:
                trianguleR(r, (v1, v2, v3))
                trianguleR(r, (v1, v3, v4))

        if (len(face) == 3):
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            
            v1 = transform(r, cube.vertices[f1])
            v2 = transform(r, cube.vertices[f2])
            v3 = transform(r, cube.vertices[f3])
            
            if (r.active_texture):
                ft1 = face[0][1] - 1
                ft2 = face[1][1] - 1
                ft3 = face[2][1] - 1
                
                vt1 = V3(*cube.tvertices[ft1])
                vt2 = V3(*cube.tvertices[ft2])
                vt3 = V3(*cube.tvertices[ft3])
        
                trianguleR(r,
                    (v1, v2, v3),
                    t,
                    (vt1, vt2, vt3)
                )
            else:
                trianguleR(r, (v1, v2, v3))
    
def load_model(r, filename, tf=(0, 0, 0), s=(1, 1, 1), rotate=(0, 0, 0)):
    r.loadModelMatrix(tf, s, rotate)
    cube = Obj(filename)
    
    vertex_buffer_object = []
    
    for face in cube.caras:       
        if(len(face) == 4):
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            f4 = face[3][0] - 1
            
            v1 = transform(r, cube.vertices[f1])
            v2 = transform(r, cube.vertices[f2])
            v3 = transform(r, cube.vertices[f3])
            v4 = transform(r, cube.vertices[f4])
            
            vertex_buffer_object.append(v1)
            vertex_buffer_object.append(v2)
            vertex_buffer_object.append(v3)
            
            if (r.active_texture):
                ft1 = face[0][1] - 1
                ft2 = face[1][1] - 1
                ft3 = face[2][1] - 1
                
                vt1 = V3(*cube.tvertices[ft1])
                vt2 = V3(*cube.tvertices[ft2])
                vt3 = V3(*cube.tvertices[ft3])
                
                vertex_buffer_object.append(vt1)
                vertex_buffer_object.append(vt2)
                vertex_buffer_object.append(vt3)

            try:
                fn1 = face[0][2] - 1
                fn2 = face[1][2] - 1
                fn3 = face[2][2] - 1
                
                vn1 = V3(*cube.nvertices[fn1])
                vn2 = V3(*cube.nvertices[fn2])
                vn3 = V3(*cube.nvertices[fn3])
                
                vertex_buffer_object.append(vn1)
                vertex_buffer_object.append(vn2)
                vertex_buffer_object.append(vn3)
                
            except:
                pass
            
            vertex_buffer_object.append(v1)
            vertex_buffer_object.append(v3)
            vertex_buffer_object.append(v4)
                
            if r.active_texture:
                
                ft1 = face[0][1] - 1
                ft3 = face[2][1] - 1
                try:
                    ft4 = face[3][1] - 1
                except:
                    ft4 = 1
                
                vt1 = V3(*cube.tvertices[ft1])
                vt3 = V3(*cube.tvertices[ft3])
                vt4 = V3(*cube.tvertices[ft4])
                
                vertex_buffer_object.append(vt1)
                vertex_buffer_object.append(vt3)
                vertex_buffer_object.append(vt4)
            
            try:
                fn1 = face[0][2] - 1
                fn3 = face[2][2] - 1
                fn4 = face[3][2] - 1
            
                vn1 = V3(*cube.nvertices[fn1])
                vn3 = V3(*cube.nvertices[fn3])
                vn4 = V3(*cube.nvertices[fn4])
            
                vertex_buffer_object.append(vn1)
                vertex_buffer_object.append(vn3)
                vertex_buffer_object.append(vn4)
            except:
                pass
            
        if (len(face) == 3):
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            
            v1 = transform(r, cube.vertices[f1])
            v2 = transform(r, cube.vertices[f2])
            v3 = transform(r, cube.vertices[f3])
            
            vertex_buffer_object.append(v1)
            vertex_buffer_object.append(v2)
            vertex_buffer_object.append(v3)
            
            if (r.active_texture):
                ft1 = face[0][1] - 1
                ft2 = face[1][1] - 1
                ft3 = face[2][1] - 1
                
                vt1 = V3(*cube.tvertices[ft1])
                vt2 = V3(*cube.tvertices[ft2])
                vt3 = V3(*cube.tvertices[ft3])
        
                vertex_buffer_object.append(vt1)
                vertex_buffer_object.append(vt2)
                vertex_buffer_object.append(vt3)

            try:
                fn1 = face[0][2] - 1
                fn2 = face[1][2] - 1
                fn3 = face[2][2] - 1
                
                vn1 = V3(*cube.nvertices[fn1])
                vn2 = V3(*cube.nvertices[fn2])
                vn3 = V3(*cube.nvertices[fn3])
                
                vertex_buffer_object.append(vn1)
                vertex_buffer_object.append(vn2)
                vertex_buffer_object.append(vn3)
            except:
                pass
        
    r.active_vertex_array = iter(vertex_buffer_object)
        
def load_model_FS(r, filename, s=(1, 1, 1), tf=(0, 0, 0)):
    cube = Obj(filename)
    for face in cube.caras:        
        if (len(face) == 4):
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            f4 = face[3][0] - 1
            
            v1 = transformT(cube.vertices[f1], s, tf)
            v2 = transformT(cube.vertices[f2], s, tf)
            v3 = transformT(cube.vertices[f3], s, tf)
            v4 = transformT(cube.vertices[f4], s, tf)

            triangule2(r, (v1, v2, v3))
            triangule2(r, (v1, v3, v4))
    
        if (len(face) == 3):
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            
            v1 = transformT(cube.vertices[f1], s, tf)
            v2 = transformT(cube.vertices[f2], s, tf)
            v3 = transformT(cube.vertices[f3], s, tf)
        
            triangule2(r, (v1, v2, v3))

def draw(r, polygon):
    if polygon == 'TRIANGLESS':
        try:
            while True:
                trianguleS(r) 
        except StopIteration:
            print('Modelo creado.')
            
    if polygon == 'TRIANGLEST':
        try:
            while True:
                trianguleT(r) 
        except StopIteration:
            print('Modelo creado.')
            
    if polygon == 'WIREFRAME':
        try:
            while True:
                triangule_wireframe(r) 
        except StopIteration:
            print('Done.')
           
def trianguleB(r, A, B, C):
    
    # Acolor = (255, 0, 0)
    # Bcolor = (0, 255, 0)
    # Ccolor = (0, 0, 255)
    
    L = V3(0, 0, 1)
    N = (B - A) * (C - A)
    i = N.norm() @ L.norm()
    
    if (i < 0):
        return
    
    gris = round(255 * i)
    r.current_color = color(gris, gris, gris)
    
    Bmin, Bmax = boundingB(A,B,C)
    Bmin.round()
    Bmax.round()
    
    for x in range(Bmin.x, Bmax.x + 1):
        for y in range(Bmin.y, Bmax.y + 1):
            w, v, u = barycentric(A, B, C, V3(x, y))        
            if (w < 0 or v < 0 or u < 0):
                continue
            
            z = A.z * w + B.z * v + C.z * u
            if (r.zBuffer[x][y] < z): 
                print(r.zBuffer[x][y])
                r.zBuffer[x][y] = z
                r.glpoint(y, x)
                
def trianguleR(r, vertices, t=None, tvertices=()):
    
    A, B, C = vertices
    
    L = V3(0, 0, 1)
    N = (B - A) * (C - A)
    i = N.norm() @ L.norm()
    
    if (i < 0):
        return
    
    gris = round(255 * i)
    r.current_color = color(gris, gris, gris)
    
    Bmin, Bmax = boundingB(A,B,C)
    Bmin.round()
    Bmax.round()
    
    if (t):
        tA, tB, tC = tvertices
        
    for x in range(Bmin.x, Bmax.x + 1):
        for y in range(Bmin.y, Bmax.y + 1):
            w, v, u = barycentric(A, B, C, V3(x, y))        
            if (w < 0 or v < 0 or u < 0):
                continue
            
            #A:w, B:u, C:v
            z = A.z * w + B.z * u + C.z * v

            if (x >= 0 and
                y >= 0 and
                x < len(r.zBuffer) and 
                y < len(r.zBuffer) and 
                r.zBuffer[x][y] < z): 
                r.zBuffer[x][y] = z
                
                if (r.active_texture):
                    tx = tA.x * w + tB.x * u + tC.x * v
                    ty = tA.y * w + tB.y * u + tC.y * v
                    
                    r.current_color = t.get_color_with_intensity(tx, ty, i)
                
                r.glpoint(x, y) 

def trianguleS(r):
    
    A = next(r.active_vertex_array)
    B = next(r.active_vertex_array)
    C = next(r.active_vertex_array)
    
    if r.active_texture:
        tA = next(r.active_vertex_array)
        tB = next(r.active_vertex_array)
        tC = next(r.active_vertex_array)
    
    if r.active_shader:
        nA = next(r.active_vertex_array)
        nB = next(r.active_vertex_array)
        nC = next(r.active_vertex_array)

    Bmin, Bmax = boundingB(A,B,C)
    Bmin.round()
    Bmax.round()

    for x in range(Bmin.x, Bmax.x + 1):
        for y in range(Bmin.y, Bmax.y + 1):
            #print(Bmin.x, Bmin.y, Bmax.x, Bmax.y, x, y)
            w, v, u = barycentric(A, B, C, V2(x, y))   
            if (w < 0 or v < 0 or u < 0):
                continue
            
            #A:w, B:u, C:v
            z = A.z * w + B.z * u + C.z * v

            if (x >= 0 and
                y >= 0 and
                x < len(r.zBuffer) and 
                y < len(r.zBuffer[x]) and 
                r.zBuffer[x][y] < z): 
                
                r.zBuffer[x][y] = z
                
                r.current_color = r.active_shader(
                    coors=(x,y),
                    bar=(w,u,v),
                    vertices=(A,B,C),
                    texture_coords=(tA,tB,tC),
                    normals=(nA,nB,nC),
                    light=r.light
                )
                    
                # if (r.texture):
                #     tx = tA.x * w + tB.x * u + tC.x * v
                #     ty = tA.y * w + tB.y * u + tC.y * v
                    
                #     r.current_color = t.get_color_with_intensity(tx, ty, i)
                
                r.glpoint(x, y, r.current_color) 

def trianguleT(r):
    
    A = next(r.active_vertex_array)
    B = next(r.active_vertex_array)
    C = next(r.active_vertex_array)
    
    if r.active_texture:
        tA = next(r.active_vertex_array)
        tB = next(r.active_vertex_array)
        tC = next(r.active_vertex_array)
    
    if r.active_shader:
        nA = next(r.active_vertex_array)
        nB = next(r.active_vertex_array)
        nC = next(r.active_vertex_array)
        
    L = V3(0, 0, 1)
    N = (B - A) * (C - A)
    i = N.norm() @ L.norm()

    Bmin, Bmax = boundingB(A,B,C)
    Bmin.round()
    Bmax.round()

    for x in range(Bmin.x, Bmax.x + 1):
        for y in range(Bmin.y, Bmax.y + 1):
            #print(Bmin.x, Bmin.y, Bmax.x, Bmax.y, x, y)
            w, v, u = barycentric(A, B, C, V2(x, y))   
            if (w < 0 or v < 0 or u < 0):
                continue
            
            #A:w, B:u, C:v
            z = A.z * w + B.z * u + C.z * v

            if (x >= 0 and
                y >= 0 and
                x < len(r.zBuffer) and 
                y < len(r.zBuffer[x]) and 
                r.zBuffer[x][y] < z): 
                
                r.zBuffer[x][y] = z
                
                if (r.active_texture):
                    tx = tA.x * w + tB.x * u + tC.x * v
                    ty = tA.y * w + tB.y * u + tC.y * v
                    
                    r.current_color = r.active_texture.get_color_with_intensity(tx, ty, i)
                
                r.glpoint(x, y)                
              
def triangule_wireframe(r):
    
    A = next(r.active_vertex_array)
    B = next(r.active_vertex_array)
    C = next(r.active_vertex_array)
    
    if r.active_texture:
        tA = next(r.active_vertex_array)
        tB = next(r.active_vertex_array)
        tC = next(r.active_vertex_array)
    
    r.line(A, B)
    r.line(B, C)
    r.line(C, A)
    
def triangule2(r, vertices, t=None, tvertices=()):
    A, B, C = vertices
    L = V3(0, 0, 1)
    N = (B - A) * (C - A)

    i = N.norm() @ L.norm()
    
    if (i < 0):
        return
    
    gris = round(255 * i)
    r.current_color = color(gris, gris, gris)
    
    Bmin, Bmax = boundingB(A,B,C)
    Bmin.round()
    Bmax.round()
    
    if (t):
        tA, tB, tC = tvertices
        
    for x in range(Bmin.x, Bmax.x + 1):
        for y in range(Bmin.y, Bmax.y + 1):
            w, v, u = barycentric(A, B, C, V3(x, y))        
            if (w < 0 or v < 0 or u < 0):
                continue
            
            #A:w, B:u, C:v
            z = A.z * w + B.z * u + C.z * v

            if (x >= 0 and
                y >= 0 and
                x < len(r.zBuffer) and 
                y < len(r.zBuffer) and 
                r.zBuffer[x][y] < z): 
                r.zBuffer[x][y] = z
                
                if (r.active_texture):
                    tx = tA.x * w + tB.x * u + tC.x * v
                    ty = tA.y * w + tB.y * u + tC.y * v
                    
                    r.current_color = t.get_color_with_intensity(tx, ty, i)
                
                r.glpoint(y, x)                 

