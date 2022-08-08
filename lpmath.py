
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
