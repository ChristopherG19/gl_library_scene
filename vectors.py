'''
    Universidad del Valle de Guatemala
    Gráficas por computadora
    Christopher García 20541
    2do. ciclo 2022
'''

class V2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        
    def __add__(self, other):
        return V2(
            self.x + other.x,
            self.y + other.y
        )
        
    def __sub__(self, other):
        return V2(
            self.x - other.x,
            self.y - other.y
        )
        
    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return V2(
                self.x * other,
                self.y * other
            )
        '''
        return V2(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )'''
        
    def __matmul__(self, other):
        if (type(other) == V2):
            return (self.x * other.x + self.y * other.y)    
        
    def length(self):
        return (self.x**2 + self.y**2)**0.5    
    
    def norm(self):
        return self * (1/self.length())
            
    def __repr__(self):
        return "V2(%s, %s)" % (self.x, self.y)

class V3(object):
    def __init__(self, x, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)
        
    def __add__(self, other):
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other):
        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
        
    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return V3(
                self.x * other,
                self.y * other,
                self.z * other
            )
        
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
        
    def __matmul__(self, other):
        if (type(other) == V3):
            return (self.x * other.x + self.y * other.y + self.z * other.z)    
        
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5    
    
    def norm(self):
        return self * (1/self.length())
            
    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)
    
def cross(v1,v2):
    return (
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )

    
    
    
    