import numpy as np

def pairwise_nw(seq1, seq2, match : int, mismatch : int, gap : int):
    n, m = len(seq1), len(seq2)
    score_matrix = np.zeros((n + 1, m + 1))

    for i in range(n + 1):
        score_matrix[i][0] = i * gap
    for j in range(m + 1):
        score_matrix[0][j] = j * gap

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_val = score_matrix[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = score_matrix[i-1][j] + gap
            insert = score_matrix[i][j-1] + gap
            score_matrix[i][j] = max(match_val, delete, insert)

    align1, align2 = "", ""
    i, j = n, m
    matches = 0

    while i > 0 or j > 0:
        current = score_matrix[i][j]

        if i > 0 and j > 0:
            score_diag = score_matrix[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            if current == score_diag:
                align1 = seq1[i-1] + align1
                align2 = seq2[j-1] + align2
                if seq1[i-1] == seq2[j-1]:
                    matches += 1
                i -= 1; j -= 1
                continue

        if i > 0 and current == score_matrix[i-1][j] + gap:
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

    length = len(align1)
    dist = 1.0 - (matches / length) if length > 0 else 1.0
    return score_matrix, align1, align2, dist

def pairwise_needleman_wunsch(s1 : str, s2 : str, match : int, mismatch : int, gap : int):
    size_s1 = len(s1)
    size_s2 = len(s2)
    matrix = np.zeros((size_s1 + 1, size_s2 + 1))
    
    matrix[:,0] = np.linspace(0, size_s1 * gap, size_s1 + 1) 
    matrix[0,:] = np.linspace(0, size_s2 * gap, size_s2 + 1)

    for line in range(1, size_s1+1):
        for column in range(1, size_s2+1):
            top = matrix[line, column-1] + gap
            left = matrix[line-1, column] + gap
            diagonal = matrix[line-1, column-1] + (match if s1[line-1] == s2[column-1] else mismatch)
            matrix[line, column] = max([top, left, diagonal])

    line_position = len(s1)
    column_position = len(s2)
    reversed_s1 = []
    reversed_s2 = []

    matches = 0
    while line_position > 0 or column_position > 0:
        actual = matrix[line_position, column_position]

        if column_position == 0:
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append("-")
            line_position -= 1

            continue
        
        if line_position == 0:
            reversed_s1.append("-")
            reversed_s2.append(s2[column_position-1])
            column_position -= 1

            continue

        if (actual == matrix[line_position-1][column_position-1] + (match if s1[line_position-1] == s2[column_position-1] else mismatch)
        ):        
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append(s2[column_position-1])
            line_position -= 1
            column_position -= 1
            if s1[line_position-1] == s2[column_position-1]:
                matches += 1

        elif (actual == matrix[line_position-1][column_position] + gap
        ):
            reversed_s1.append(s1[line_position-1])
            reversed_s2.append("-")
            line_position -= 1

        else:
            reversed_s1.append("-")
            reversed_s2.append(s2[column_position-1])
            column_position -= 1                        

    aligned_s1 = "".join(reversed_s1)[::-1]
    aligned_s2 = "".join(reversed_s2)[::-1]

    length = len(aligned_s1)
    dist = 1.0 - (matches / length) if length > 0 else 1.0

    return matrix, aligned_s1, aligned_s2, dist

if __name__ == "__main__":
    match = 1
    mismatch = -1
    gap = -2

    seq1 = "ACATTGGCACCCTTACTTCATTTTCGGAACTTGAGCCGGAATGGTGGGAACAGCACTTAGCCTCCTTATTCGGACAGAATTAAGCCAGCCCGGACCTCTATTAGGTGATGACCAAATTTATAACGTAATTGTCACCGCCCATGCCTTCATTATAATCTTTTTTATAGTAATACCAATTATAATTGGAGGGTTTGGAAACTGGCTATTACCCCTAATAATCGGAGCCCCAGACATGGCATTCCCCCGAATAAACAACATAAGTTTCTGATTACTCCCCCCATCTTTCACACTACTACTCTCCTCAGCCTGCATCGAAGCAGGTGCTGGAACAGGGTGAACCGTCTACCCTCCCCTAGCCGGAAACCTAGCCCACGCCGGGCCATCCGTAGATTTAACTATCTTCTCTCTACACTTAGCCGGAGTATCTTCCATCCTCGGAGCAATTAACTTTATTACAACAGCAATCAACATAAAACCCCCAGCAATATCCCAATACCAAACACCACTATTTGTGTGATCCGTCCTAATTACAGCTGTACTTCTCCTACTATCCCTACCAGTACTAGCTGCTGGAATTACAATACTACTCACAGACCGCAACTTAAACACAACCTTCTTTGACCCCGCAGGGGGAGGAGATCCCATCCTATACCAACACCTCTCTCATYT"
    seq2 = "CCGGTATAGTAGGCACTGCCTTGAGCCTCCTCATCCGAGCCGAACTAGGTCAGCCCGGTACTTTACTAGGTGACGATCAAATTTATAATGTCATCGTAACCGCCCATGCTTTCGTAATAATCTTCTTCATAGTCATGCCCATCATAATTGGGGGCTTTGGAAACTGACTAGTGCCGTTAATAATTGGTGCTCCGGACATGGCATTCCCCCGAATAAATAACATGAGCTTCTGACTCCTTCCTCCATCCTTTCTTCTACTATTAGCATCTTCTATGGTAGAAGCAGGTGCAGGAACGGGATGAACCGTATACCCCCCACTGGCTGGCAATCTGGCCCATGCAGGAGCATCCGTTGACCTTACAATTTTCTCCTTACACTTAGCCGGAGTCTCTTCTATTTTAGGGGCAATTAATTTCATCACTACTATTATCAACATAAAACCCCCTGCAATATCCCAGTATCAAACTCCCCTGTTTGTATGATCAGTACTAATTACAGCAGTTCTACTCTTACTATCCCTGCCTGTACTGGCTGCTGGAATTACAATACTTTTAACAGACCGGAATCTTAATACAACATTTTTTGATCCCGCTGGAGGAGGAGACCCTATCCTATATCAACACCTATTCTGATTCTTCGGGCATCCTG"
    # seq1 = "ATTGCCATT"
    # seq2 = "ATGGCCATT"

    pw_matrix, pw_new_s1, pw_new_s2, pw_dist = pairwise_nw(seq1, seq2, match, mismatch, gap) 
    gb_matrix, gb_new_s1, gb_new_s2, gb_dist = pairwise_needleman_wunsch(seq1, seq2, match, mismatch, gap)
    # print(pw_matrix, pw_new_s1, pw_new_s2, pw_dist)
    # print("\n\n")
    # print(gb_matrix, gb_new_s1, gb_new_s2, gb_dist)
    
    print(pw_dist)
    print(gb_dist)