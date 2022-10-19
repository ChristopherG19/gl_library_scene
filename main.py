'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''

from gl import *
from colors import *
from shapes import *
from textures import Texture

r = Render(1024, 1024) 

t = Texture('./Models_And_Textures/Books2.bmp')
r.framebuffer = t.pixels

# Dragon ---------------------------------------------------------
t = Texture('./Models_And_Textures/Dragon.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (3, 3, 3)
tf = (510, 440, 0)
rot = (0, 0, 0)

load_model(r, './Models_And_Textures/Dragon.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

# Cyborg ---------------------------------------------------------
t = Texture('./Models_And_Textures/helmet.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (7,7,7)
tf = (512, 740, 0)
rot = (0, 0, 0)

load_model(r, './Models_And_Textures/helmet_clean.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

# Steam Deck ---------------------------------------------------------
t = Texture('./Models_And_Textures/Steam.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (19, 19, 19)
tf = (275, 410, 0)
rot = (-1, 0, 0)

load_model(r, './Models_And_Textures/Steam.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

# Bus ---------------------------------------------------------
t = Texture('./Models_And_Textures/Bus.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (135, 135, 135)
tf = (510, 185, 0)
rot = (0.5, 20, 0)

load_model(r, './Models_And_Textures/Bus.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

t = Texture('./Models_And_Textures/Bus.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (60, 60, 60)
tf = (465, 145, 0)
rot = (0.6, -20, 0)

load_model(r, './Models_And_Textures/Bus.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

# Tenis ---------------------------------------------------------
t = Texture('./Models_And_Textures/nb574.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0.6, -12, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (25, 25, 25)
tf = (770, 250, 0)
rot = (0, 0, 5)

load_model(r, './Models_And_Textures/nb574.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

# Velero ---------------------------------------------------------
t = Texture('./Models_And_Textures/veliero.bmp')
r.active_texture = t
r.active_shader = r.shader

r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0))

s = (20, 20, 20)
tf = (650, 632, 0)
rot = (5, 0, 0)

load_model(r, './Models_And_Textures/veliero.obj', tf, s, rot)
draw(r, 'TRIANGLEST')

# Fin ---------------------------------------------------------
r.write("Scene.bmp")
print("Escena creada con éxito")