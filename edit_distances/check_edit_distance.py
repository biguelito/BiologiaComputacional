def print_matrix(matrix : list, s1 : str, s2 : str):
    matrix_s1 = "  " + s2
    matrix_s2 = " " + s1 
    print(" |".join(f" {l} " for l in matrix_s1))
    pos = 0
    for line in matrix:
        l = "|".join(f"{column:4.0f}" for column in line)
        print(f"{matrix_s2[pos]}   |{l}")
        pos += 1 