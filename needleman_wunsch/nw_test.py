from needleman_wunsch_alg import execute_global_alignment
import check_needleman_wunsch as check_nw
import numpy as np

def run_test(min_size : int, max_size : int, print_path=False):
    s1_len = np.random.choice(range(min_size, max_size))
    s2_len = np.random.choice(range(min_size, max_size))
    letters = ['A', 'T', 'G', 'C']
    s1 = "".join(np.random.choice(letters, s1_len))
    s2 = "".join(np.random.choice(letters, s2_len))        

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

if __name__ == "__main__":
    min_size = 10
    max_size = 20
    run_test(min_size, max_size, True)