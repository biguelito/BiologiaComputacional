from needleman_wunsch import execute_global_alignment
import check_needleman_wunsch as check_nw

def align_sequences(s1 : str, s2 : str, print_path=False):
    match_value = 1
    mismatch_value = -1
    gap_value = -2

    print(s1)
    print(s2)
    matrix, new_s1, new_s2 = execute_global_alignment(s1, s2, match_value, mismatch_value, gap_value, print_path=print_path)
    check_nw.print_matrix(matrix, s1, s2)
    print(new_s1)
    print(new_s2)
    better_score = matrix[len(s1)][len(s2)]
    check_nw.validate(better_score, new_s1, new_s2, match_value, mismatch_value, gap_value)

    return

if __name__ == "__main__":
    align_sequences("GGCGCA", "AGCCCCTG", True)