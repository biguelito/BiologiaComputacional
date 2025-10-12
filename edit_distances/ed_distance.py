from edit_distance import execute_edit_distance
import check_edit_distance as check_ed

def distances(s1 : str, s2 : str):
    match_value = 0
    mismatch_value = 1
    gap_value = 1

    print(s1)
    print(s2)
    matrix = execute_edit_distance(s1, s2, match_value, mismatch_value, gap_value)
    check_ed.print_matrix(matrix, s1, s2)

    return

if __name__ == "__main__":
    distances("GGCGCA", "AGCCCCTG")