from re import L
import struct 
from collections import namedtuple
from obj import Obj
import random
import lpmath as lpm
from  math import pi, cos, tan, sin 
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def NewColor(r, g, b):
    return bytes([
        int(b*255),
        int(g*255),
        int(r*255)
    ])

class Renderer(object):

    def __init__(self, width, height):#Constructor
        self.width = width
        self.height = height
        self.secondary_color = NewColor(1, 1, 1)

        self.glViewPort(0, 0, self.width, self.height)

        self.clearColor = NewColor(0,0,0)

    def glViewPort(self, posX, posY, width, height):
        self.vPx = posX
        self.vPy = posY
        self.vpWidth = width
        self.vpHeight = height
    
    def glClearViewPort(self, clr = None):
        for x in range(self.vPx, self.vPx + self.vpWidth):
            for y in range(self.vPy, self.vPy + self.vpHeight):
                self.glCreatePoint(x, y, clr)

    def glVpPoint(self, ndcX, ndcY, clr = None): # View port coordinates (NDC)
        """ De coordenadas normalizadas a  coordenadas de ventana"""
        x = (ndcX+1)*(self.vpWidth/2) +self.vPx
        y = (ndcY+1)*(self.vpHeight/2) +self.vPy

        self.glCreatePoint(int(x), int(y), clr)
    def grades_to_radians(self, grados):
        return pi * grados /180
    
    def glCreateObjectMatrix(self, translate = V3(0, 0, 0), rotate  = V3(0, 0, 0), scale = V3(1, 1, 1)):
        
        translation = lpm.matriz([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
            ])

        pitch = self.grades_to_radians(rotate.x)
        yaw = self.grades_to_radians(rotate.y)
        roll = self.grades_to_radians(rotate.z)
        
        R_x = lpm.matriz([
            [1, 0, 0, 0],
            [0, cos(pitch), - sin(pitch), 0],
            [0, sin(pitch), cos(pitch), 0],
            [0, 0, 0, 1]
        ])
        R_y = lpm.matriz([
            [cos(yaw), 0, sin(yaw), 0],
            [0, 1, 0, 0],
            [-sin(yaw), 0, cos(yaw), 0],
            [0, 0, 0, 1]
        ])
        R_z = lpm.matriz([
            [cos(roll), -sin(roll), 0, 0],
            [sin(roll), cos(roll), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        rotation = lpm.multMatrixes(R_x, R_y, R_z)
        scaleMat = lpm.matriz([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
            ])
        return lpm.multMatrixes(translation, rotation, scaleMat)

    def glTransform(self, vertex, matrix):
        v = V4(vertex[0], vertex[1], vertex[2], 1)

        #vt = matrix @ v
        vt = lpm.matriz_por_vector(matrix, v)
        #vt = vt.tolist()[0]
        vf = V3( vt[0]/vt[3],  vt[1]/vt[3], vt[2]/vt[3])
        
        return vf

    def glLoadModel(self, filename, translate = V3(0, 0, 0), rotate  = V3(0, 0, 0), scale = V3(1, 1, 1)):
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)
        for face in model.faces:
            vertCount = len(face)
            #Relleno con triangulos de colores
            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]

            v0 = self.glTransform(v0, modelMatrix)
            v1 = self.glTransform(v1, modelMatrix)
            v2 = self.glTransform(v2, modelMatrix)



            self.glTriangle_std(v0, v1, v2, NewColor(random.random(),
                                                  random.random(),
                                                  random.random()))

            #Wire model
            '''
            for vert in range(len(face)):
                v0 = model.vertices[face[vert][0]-1]
                v1 = model.vertices[face[(vert+1) % vertCount][0]-1]

                v0 = self.glTransform(v0, modelMatrix) #V2(v0[0], v0[1])
                v1 = self.glTransform(v1, modelMatrix)#V2(v1[0], v1[1])

                self.glLine(V2(v0.x, v0.y), V2(v1.x, v1.y))
            '''

    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x0 == x1 and y0 == y1:
            self.glCreatePoint(x0,y0,clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de 
        # izquierda a derecha       
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                self.glCreatePoint(y, x, clr)
            else:
                # Dibujar de manera horizontal
                self.glCreatePoint(x, y, clr)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1
    
    def glTriangle_std(self, A, B, C, clr = None):
        """     
        #Forma alternativa de ordenar puntos que no termine de concretar con todos los casos    
        mx = A if A.y==max(A.y, B.y, C.y) else B if B.y==max(A.y, B.y, C.y) else C 
        mn = C if C.y==min(A.y, B.y, C.y) else B if B.y==min(A.y, B.y, C.y) else A 
        md = B if (B.y!=mn.y) and (B.y!=mx.y)  else C if (C.y!=mn.y) and (C.y!=mx.y)else A 
        A = mx
        B = md
        C = mn
         """
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        self.glLine(A,B, clr)
        self.glLine(B,C, clr)
        self.glLine(C,A, clr)

        def flatBottom(vA,vB,vC):
            try:
                mBA = (vB.x - vA.x) / (vB.y - vA.y)
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
            except:
                pass
            else:
                x0 = vB.x
                x1 = vC.x
                for y in range(int(vB.y), int(vA.y)):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA,vB,vC):
            try:
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
                mCB = (vC.x - vB.x) / (vC.y - vB.y)
            except:
                pass
            else:
                x0 = vA.x
                x1 = vB.x
                for y in range(int(vA.y), int(vC.y), -1):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 -= mCA
                    x1 -= mCB

        if B.y == C.y:
            # Parte plana abajo
            flatBottom(A,B,C)
        elif A.y == B.y:
            # Parte plana arriba
            flatTop(A,B,C)
        else:
            # Dibujo ambos tipos de triangulos
            # Teorema de intercepto
            D = V2( A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottom(A,B,D)
            flatTop(B,D,C)     
        
    def glSecondaryColor(self, r, g, b):
        self.secondary_color  = NewColor(r, g, b)
    
    def glCreatePoint(self, x, y, clr = None):# Window coordinates
        if (0<=x<self.width) and (0<=y<self.height):
            self.pixels[x][y] = clr or self.secondary_color


    def glClearColor(self, r, g, b): #setter del color de fondo
        self.clearColor = NewColor(r, g, b)
    
    def glClear(self):#Crea el fondo
        self.pixels = [[ self.clearColor for i in range(self.height)]
         for x in range (self.width)]
    
    def glFinish(self, filename):
        #http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm
        with open (filename, 'wb') as file:
            #Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + ((self.width+self.height)) ))
            file.write(dword(0))
            file.write(dword( 14 + 40 ))
            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
    #Intento de relleno pt 1
    def polygon(self, vertices, clr = None):
        for i in range(len(vertices)):
            self.glLine(vertices[i], vertices[(i+1)%len(vertices)], clr)
    #Intento de relleno pt 2
    def filled_polygon(self, vertices, clr_borde = None, clr_relleno = None, insidePolygons = []):         
        self.polygon(vertices, clr = clr_borde)
        max_y = -1
        max_x = -1
        min_y = self.height
        min_x = self.width
        #Encontrando el cuadro donde esta la figura
        for vertice in vertices: 
            #-------Para x-------
            #Minimo
            min_x = vertice[0] if(vertice[0]<min_x) else min_x
            #Maximo
            max_x  = vertice[0] if(vertice[0]>max_x) else max_x
            #-------Para Y-------
            #Minimo
            min_y  =  vertice[1] if(vertice[1]<min_y) else min_y
            #Maximo
            max_y = vertice[1] if (vertice[1]>max_y) else max_y
        min_y += 1
        max_y += 1
        for polygon in insidePolygons:
            self.polygon(polygon, clr_borde)
        #Escaneo horizontal
        border_scan = {}
        for y in range(min_y, max_y):
            last_pixel_is_border = False
            bordes = []
            for x in range(min_x, max_x):
                if self.pixels[x][y] == clr_borde:
                    if not last_pixel_is_border:
                        bordes.append([x])
                    else:
                        brd = list(bordes[-1])
                        brd.append(x)
                        bordes[-1] = brd
                    last_pixel_is_border = True
                else:
                    last_pixel_is_border = False
            border_scan[y] = bordes
        #Rellenado a partir de escaneo
        for y in border_scan:
            x_borders  = border_scan.get(y)
            if(len(x_borders)>1):#Asegurarse que haya por lo menos 1
                bordes_tratados = 0
                paint = True
                while True:
                    borde_inicial  = x_borders[bordes_tratados]
                    try:
                        borde_final  = x_borders[bordes_tratados+1]
                    except:
                        break
                    bordes_tratados += 1
                    if paint:
                        self.glLine(V2(borde_inicial[-1], y), V2(borde_final[0], y), NewColor(0, 0, 1))
                    paint = not paint                

        self.polygon(vertices, clr_borde)
        #self.polygon([V2(min_x, min_y), V2(max_x, min_y), V2(max_x, max_y), V2(min_x, max_y)], NewColor(0, 1, 0))    
         

