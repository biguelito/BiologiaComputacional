import numpy as np

def edit_distance(s1 : str, s2 : str, match_value : int, mismatch_value : int, gap_value : int):
    # cria uma matriz de 0s de tamamho S1+1 por S2+1 
    size_s1 = len(s1)
    size_s2 = len(s2)
    matrix = np.zeros((size_s1 + 1, size_s2 + 1))
    
    # Adiciona o valor nos gaps nos eixos (0,y) e (x,0), sendo 
    # Nas posições (x, 0) adicionado o valor x
    # Nas posições (0, y) adicionado o valor y
    matrix[:,0] = [i for i in range(size_s1+1)] 
    matrix[0,:] = [i for i in range(size_s2+1)]

    # Inicia a populacao da matriz, calculando o valor de cima, esquerda e diagonal e escolhendo o menor valor
    # Esquerda: Valor da esquerda anterior + gap_value
    # Cima: Valor de cima anterior + gap_value
    # Diagonal: Valor anterior de cima e esquerda + 
    #   (match_value se os caracteres que represetam essa casa anterior forem iguais
    #   mismatch_value se os caracteres que represetam essa casa anterior forem diferentes)
    for line in range(1, size_s1+1):
        for column in range(1, size_s2+1):
            top = matrix[line, column-1] + gap_value
            left = matrix[line-1, column] + gap_value
            diagonal = matrix[line-1, column-1] + (match_value if s1[line-1] == s2[column-1] else mismatch_value)
            matrix[line, column] = min([top, left, diagonal])

    return matrix


def execute_edit_distance(s1 : str, s2 : str, match_value : int, mismatch_value, gap_value : int):
    matrix = edit_distance(s1, s2, match_value, mismatch_value, gap_value)
    
    return matrix