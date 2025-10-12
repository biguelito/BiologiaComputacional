from needleman_wunsch_semi_global import execute_semi_global_alignment, get_max_position
import check_needleman_wunsch_semi_global as check_nw_semi

def semi_align_sequences(s1 : str, s2 : str, print_path=False):
    match_value = 1
    mismatch_value = -1
    gap_value = -2

    print(s1)
    print(s2)
    matrix, new_s1, new_s2 = execute_semi_global_alignment(s1, s2, match_value, mismatch_value, gap_value, print_path=print_path)
    check_nw_semi.print_matrix(matrix, s1, s2)
    print(new_s1)
    print(new_s2)
    
    line_position, column_position = get_max_position(matrix, s1, s2)
    better_score = matrix[line_position][column_position]

    # check_nw_semi.validate(better_score, new_s1, new_s2, match_value, mismatch_value, gap_value)

    return

if __name__ == "__main__":
    semi_align_sequences("GGCGCA", "AGCCCCTG", True)