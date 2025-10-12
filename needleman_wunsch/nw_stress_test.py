from needleman_wunsch_alg import execute_global_alignment
import numpy as np
import time
import check_needleman_wunsch as check_nw

def generate_test_data(data_size, min_size, max_size):
    test_data = []
    for i in range(data_size):
        s1_len = np.random.choice(range(min_size, max_size))
        s2_len = np.random.choice(range(min_size, max_size))
        s1 = np.random.choice(['A', 'T', 'G', 'C'], s1_len)
        s2 = np.random.choice(['A', 'T', 'G', 'C'], s2_len)
        test_data.append([s1, s2])

    return test_data

def execute_test(data_size : int, min_size : int, max_size : int):
    match_value = 1
    mismatch_value = -1
    gap_value = -2
    test_data = generate_test_data(data_size, min_size, max_size)

    executions_time = []
    for i, data in enumerate(test_data):
        start = time.time()
        matrix, new_s1, new_s2 = execute_global_alignment(data[0], data[1], match_value, mismatch_value, gap_value)
        total_time = time.time()-start
        executions_time.append(total_time)

        better_score = matrix[len(data[0])][len(data[1])]
        print(f"Test {i+1}")
        is_ok = check_nw.validate(better_score, new_s1, new_s2, match_value, mismatch_value, gap_value)
        if not is_ok:
            print("NOK")
            return
    print("OK")
    print(np.mean(executions_time))
    
    return

if __name__ == "__main__":
    data_size = 10000
    min_size = 10
    max_size = 60
    execute_test(data_size, min_size, max_size)