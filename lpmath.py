from  math import pi, cos, tan, sin, acos
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])

def matriz(matriz: list):
    if not validMatrix(matriz):
        return
    return matriz
    
def identidad(dimension :int):
    if dimension<=0:
        raise Exception(f"Dimension invalida para matriz: {dimension}")
    return [[1 if (j==i) else 0 for j in range(dimension)] for i in range(dimension)]  

def validMatrix(matriz):
    if  type(matriz)!=list:
        return False
    for fila in matriz:
        if type(fila)!=list:
            print(f"Tipo invalido para fila {matriz.index(fila)+1} (debe ser una lista)")  
            return False  
        if matriz.index(fila)==0:
            size_fila = len(fila)
            continue
        if size_fila!=len(fila):
            print(f"Fila {matriz.index(fila)+1} tiene tamaño invalido\nEsperado: {size_fila}\nObtenido: {len(fila)}")
            return False
    return True

def allowMult(matriz1, matriz2):
    if not (validMatrix(matriz1) and validMatrix(matriz2)):
        return False
    return len(matriz1[0])==len(matriz2)

def multTwoMatrixes(matriz1, matriz2):
    resultado = [[0 for r in range(len(matriz1))] for a in range(len(matriz2[0]))]
    if allowMult(matriz1, matriz2):
        if len(matriz2[0])==1:
            return matriz_por_vector(matriz1, matriz2)

        for i in range(len(matriz1)):
            multiplo1 = []
            for a in matriz1[i]:
                multiplo1.append(a)
            for j in range(len(matriz2[0])):
                multiplo2 = []
                for b in range(len(matriz2)):
                    multiplo2.append(matriz2[b][j])
                res = 0
                for ind in range(len(multiplo1)):
                    res += (multiplo1[ind] * multiplo2[ind])
                resultado[i][j] = res
        return resultado
    return

def matriz_por_vector(matriz, vector):
    resultado = []
    for fila in matriz:
        res = 0
        for elemnt in range(len(fila)):
            res += (fila[elemnt]*vector[elemnt])
        resultado.append(res)
    return resultado

def multMatrixes(*matrices):
    cantidad_matrices = len(matrices)
    if cantidad_matrices<0:
        print("No ingreso matrices a multiplicar")
        return 
    if cantidad_matrices==1:
        return matrices[0]
    indice_matriz_2 = 1
    matriz_1 = matrices[0]
    while indice_matriz_2<cantidad_matrices:
        matriz_2 = matrices[indice_matriz_2]
        matriz_resultado = multTwoMatrixes(matriz_1, matriz_2)
        if not matriz_resultado:
            return
        matriz_1 = matriz_resultado
        indice_matriz_2 += 1
    return matriz_resultado

def grades_to_radians(grados):
        return pi * grados /180

def radians_to_grades(radianes):
    return 180*radianes / pi

def productoPunto(vector_1, vector_2):
        if len(vector_1)!=len(vector_2):
            raise Exception ("No match on vector dimensions")
        total = 0
        for componente_i in range(len(vector_1)):
            total += vector_1[componente_i]*vector_2[componente_i]
        return total

def magnitud_vector(vector: list):
    sum = 0
    for comp in vector:
        sum += comp**2
    return sum**0.5

def anguloVectores(vector_1, vector_2):
    return radians_to_grades( acos( productoPunto(vector_1, vector_2)/(magnitud_vector(vector_1)*magnitud_vector(vector_2)) ) )

def multProductoCruz(*vectores):
    if len(vectores)<1:
        raise Exception("No se recibio vectores que multiplicar en el producto cruz")
    vector_1 = vectores[0]
    for i in range(len(vectores)):
        if not i==0:
            vector_1 = productoCruz(vector_1, vectores[i])
            if vector_1 == -1:
                return
    return vector_1

def productoCruz(vector_1, vector_2):
    if len(vector_1)>3 or len(vector_2)>3:
        print("Dimensiones de vectores no coinciden")
        return -1
    
    while len(vector_1)<3:
        vector_1.append(0)
    while len(vector_2)<3:
        vector_2.append(0)
    
    cont = 0
    vector_res = []
    signo = 1
    while cont<len(vector_2):
        matriz_det = []
        #fila 1
        matriz_det.append([vector_1[i] for i in range(len(vector_1)) if not i==cont])
        #fila 2
        matriz_det.append([vector_2[i] for i in range(len(vector_2)) if not i==cont])
        vector_res.append(signo*((matriz_det[0][0]*matriz_det[1][1])-(matriz_det[0][1]*matriz_det[1][0])))
        signo = -signo
        cont += 1
    return vector_res

def suma_o_resta_vectores(vector_1: list, vector_2: list, is_resta: bool = False):
    factor = -1 if is_resta else 1
    if not len(vector_2)==len(vector_1):
        print("Dimensiones de vectores no coiniciden")
        return
    vector_res = []
    for i in range(len(vector_1)):
        vector_res.append(vector_1[i]+factor*vector_2[i])
    return vector_res