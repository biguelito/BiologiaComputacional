def print_matrix(matrix : list, s1 : str, s2 : str):
    matrix_s1 = "  " + s2
    matrix_s2 = " " + s1 
    print(" |".join(f" {l} " for l in matrix_s1))
    pos = 0
    for line in matrix:
        l = "|".join(f"{column:4.0f}" for column in line)
        print(f"{matrix_s2[pos]}   |{l}")
        pos += 1

def validate(better_score : int, s1 : str, s2 : str, match_value : int, mismatch_value : int, gap_value : int):
    total_score = 0

    if (len(s1) != len(s2)):
        print("error: strings with different lengths")
        return

    for i in range(len(s1)):
        char_s1 = s1[i]
        char_s2 = s2[i]
        if (char_s1 == char_s2):
            total_score += match_value
        elif (char_s1 == "-" or char_s2 == "-"):
            total_score += gap_value
        else:
            total_score += mismatch_value

    print(f"better score: {better_score}\ntotal score: {total_score}")
    return total_score == better_score