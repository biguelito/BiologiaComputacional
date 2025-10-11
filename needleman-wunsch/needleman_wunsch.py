import numpy as np

def needleman_wunsch(s1 : str, s2 : str, match_value : int, mismatch_value : int, gap_value : int):
    # cria uma matriz de 0s de tamamho S1+1 por S2+1 
    size_s1 = len(s1)
    size_s2 = len(s2)
    matrix = np.zeros((size_s1 + 1, size_s2 + 1))
    
    # Adiciona o valor nos gaps nos eixos (0,y) e (x,0), sendo 
    # Nas posições (x, 0) adicionado o valor x * gap
    # Nas posições (0, y) adicionado o valor y * gap
    matrix[:,0] = np.linspace(0, size_s1 * gap_value, size_s1 + 1) 
    matrix[0,:] = np.linspace(0, size_s2 * gap_value, size_s2 + 1)

    # Inicia a populacao da matriz, calculando o valor de cima, esquerda e diagonal e escolhendo o melhor valor
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
            matrix[line, column] = max([top, left, diagonal])

    return matrix

def backtracking(s1 : str, s2 : str, matrix : list, match_value : int, mismatch_value : int, gap_value : int, print_path=False):
    # Obtem as informações necessárias
    line_position = len(s1)
    column_position = len(s2)
    reversed_s1 = []
    reversed_s2 = []

    # Percorre a matriz ate alcancar alguma borda da esquerda ou de cima da matriz
    # O ponto de partida é o ponto inferior direito da matriz
    # Essa posicao possui a melhor pontuacao do alinhamento dessas cadeias
    while line_position > 0 or column_position > 0:
        # Para saber de onde o valor daquela posição veio, é obtido o valor da posicao que estamos
        # e recalculado os valores das posicoes adjacentes
        # Ao encontrar que o valor veio da:
        # * Diagonal: Mantem as 2 letras, de S1 e S2
        # * Cima: Adiciona um gap a nova S2 e mantem a letra em S1
        # * Esquerda: Adiciona um gap a nova S1 e mantem a letra em S2
        
        actual = matrix[line_position, column_position]
        back_score = 0
        path = ""

        # Chegou na primeira coluna
        if column_position == 0:
            path = "up"
            back_score = matrix[line_position-1][column_position]
            
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append("-")
            line_position -= 1
            continue
        # Chegou na primeira linha
        if line_position == 0:
            path = "left"
            back_score = matrix[line_position][column_position-1]
            
            reversed_s1.append("-")
            reversed_s2.append(s2[column_position-1])
            column_position -= 1
            continue

        # Checa se veio da diagonal
        if (actual == matrix[line_position-1][column_position-1] + (match_value if s1[line_position-1] == s2[column_position-1] else mismatch_value)
        ):        
            path = "diagonal"
            back_score = matrix[line_position-1][column_position-1]
            
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append(s2[column_position-1])
            line_position -= 1
            column_position -= 1

        # Checa se veio de cima
        elif (actual == matrix[line_position-1][column_position] + gap_value
        ):
            path = "up"
            back_score = matrix[line_position-1][column_position]

            reversed_s1.append(s1[line_position-1])
            reversed_s2.append("-")
            line_position -= 1

        # Veio da esquerda
        else:
            path = "left"
            back_score = matrix[line_position][column_position-1]

            reversed_s1.append("-")
            reversed_s2.append(s2[column_position-1])
            column_position -= 1                        

        print(f"From {actual} moves {path} to {back_score}") if print_path else None
    
    # As string finais obtidas estão invertidas, aqui invertemos elas
    aligned_s1 = "".join(reversed_s1)[::-1]
    aligned_s2 = "".join(reversed_s2)[::-1]

    return aligned_s1, aligned_s2

def execute_global_alignment(s1 : str, s2 : str, match_value : int, mismatch_value, gap_value : int, print_path=False):
    matrix = needleman_wunsch(s1, s2, match_value, mismatch_value, gap_value)
    new_s1, new_s2 = backtracking(s1, s2, matrix, match_value, mismatch_value, gap_value, print_path)
    
    return matrix, new_s1, new_s2