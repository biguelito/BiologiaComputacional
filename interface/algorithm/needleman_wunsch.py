import numpy as np

def needleman_wunsch(s1 : str, s2 : str, match_value : int, mismatch_value : int, gap_value : int):
    size_s1 = len(s1)
    size_s2 = len(s2)
    matrix = np.zeros((size_s1 + 1, size_s2 + 1))
    
    matrix[:,0] = np.linspace(0, size_s1 * gap_value, size_s1 + 1) 
    matrix[0,:] = np.linspace(0, size_s2 * gap_value, size_s2 + 1)

    for line in range(1, size_s1+1):
        for column in range(1, size_s2+1):
            top = matrix[line, column-1] + gap_value
            left = matrix[line-1, column] + gap_value
            diagonal = matrix[line-1, column-1] + (match_value if s1[line-1] == s2[column-1] else mismatch_value)
            matrix[line, column] = max([top, left, diagonal])

    return matrix

def log(line_position : int, column_position : int, actual : int, actual_pos : int, path : str, back_score : int, print_path=False):
    next_pos = (line_position, column_position)
    print(f"From {actual} {actual_pos} moves {path} to {back_score} {next_pos}") if print_path else None
    return

def backtracking(s1 : str, s2 : str, matrix : list, match_value : int, mismatch_value : int, gap_value : int, print_path=False):
    line_position = len(s1)
    column_position = len(s2)
    reversed_s1 = []
    reversed_s2 = []

    while line_position > 0 or column_position > 0:
        actual = matrix[line_position, column_position]
        actual_pos = (line_position, column_position)
        back_score = 0
        path = ""

        if column_position == 0:
            path = "up"
            back_score = matrix[line_position-1][column_position]
            
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append("-")
            line_position -= 1

            log(line_position, column_position, actual, actual_pos, path, back_score, print_path)
            continue

        if line_position == 0:
            path = "left"
            back_score = matrix[line_position][column_position-1]
            
            reversed_s1.append("-")
            reversed_s2.append(s2[column_position-1])
            column_position -= 1

            log(line_position, column_position, actual, actual_pos, path, back_score, print_path)
            continue

        if (actual == matrix[line_position-1][column_position-1] + (match_value if s1[line_position-1] == s2[column_position-1] else mismatch_value)
        ):        
            path = "diagonal"
            back_score = matrix[line_position-1][column_position-1]
            
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append(s2[column_position-1])
            line_position -= 1
            column_position -= 1

        elif (actual == matrix[line_position-1][column_position] + gap_value
        ):
            path = "up"
            back_score = matrix[line_position-1][column_position]

            reversed_s1.append(s1[line_position-1])
            reversed_s2.append("-")
            line_position -= 1

        else:
            path = "left"
            back_score = matrix[line_position][column_position-1]

            reversed_s1.append("-")
            reversed_s2.append(s2[column_position-1])
            column_position -= 1                        

        log(line_position, column_position, actual, actual_pos, path, back_score, print_path)
    
    aligned_s1 = "".join(reversed_s1)[::-1]
    aligned_s2 = "".join(reversed_s2)[::-1]

    return aligned_s1, aligned_s2