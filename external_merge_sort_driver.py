import top_k_with_external_merge_sort as ems
import pandas as pd
import random

# Change the parameters as needed
M = 1000        # Main-memory size
B = 128         # Block size
K = 500        # K-value
N = 1000000     # Size of test-case

# Initialize an empty list as the test case
test_case = []
solution = []

# Initialize N random numbers between 0 and 1
test_case = [round(random.random(), 8) for _ in range(N)]
        
# This will be the solution
solution = sorted(test_case)[:K]

print("Generated test case with parms: [M={},B={},K={},N={}]".format(M,B,K,N))

tracker = None

# Copy the current test case into two new arrays
disk_trad = test_case.copy()
disk_opt = test_case.copy()

# Objects for traditional and optimized merge sort
trad = ems.ExternalMergeSort(M, B, disk_trad)
opt = ems.ExternalMergeSort(M, B, disk_opt)      

# Arrays with the top-k elements
trad_ans = trad.top_k_with_traditional_external_merge_sort(K)
opt_ans = opt.top_k_with_optimized_external_merge_sort(K)

tracker = opt.tracker

# Write the tracker/metrics to a CSV
df = pd.DataFrame(tracker, columns = ['Run','Remaining Input Rows', 'Cutoff Key (before each run)', 'Number of I/O Ops'])
csv_file_path = "table_metrics.csv"
df.to_csv(csv_file_path, index=False)

if trad_ans == opt_ans and opt_ans == solution:
    print(opt_ans)
    print("Traditional External Merge Sort: Passed\nOptimized External Merge Sort: Passed")
    exit(0)

if trad_ans != solution:
    print("Traditional External Merge Sort: Failed")

if opt_ans != solution:
    print("Optimized External Merge Sort: Failed")