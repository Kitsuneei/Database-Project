import external_merge_sort as tems
import pandas as pd
import os
import sys

if len(sys.argv) != 2:
    print("Usage: python external_merge_sort_drvier.py <numeric_dataset_name>")
    sys.exit(1)

# Get the filename from the command line argument
filename = sys.argv[1]

# Get the current working directory
cwd = os.getcwd()

# Construct the full path by joining the cwd and the filename
file_path = os.path.join(cwd, filename)

# Change the parameters as needed
M = 1000        # Main-memory size
B = 256        # Block size
K = 800         # K-value

# Initialize an empty list as the test case
test_case = []

# Read the values from the file and store them in the array
with open(file_path, "r") as file:
    for line in file:
        # Convert the line to a float and append it to the array
        value = float(line.strip())
        test_case.append(value)
        
# This will be the solution
solution = sorted(test_case)[:K]

print("Read Dataset")

tracker = None

# Copy the current test case into two new arrays
disk_trad = test_case.copy()
disk_opt = test_case.copy()

# Objects for traditional and optimized merge sort
trad = tems.ExternalMergeSort(M, B, disk_trad)
opt = tems.ExternalMergeSort(M, B, disk_opt)      

# Arrays with the top-k elements
trad_ans = trad.top_k_with_traditional_external_merge_sort(K)
opt_ans = opt.top_k_with_optimized_external_merge_sort(K)

tracker = opt.tracker

# Write the tracker/metrics to a CSV
# Only the optimized exteral merge sort implementation has its metrics tracked and written, because there is a cutoff filter
# The traditional implementation has trivial metrics that are not interesting to the problem
df = pd.DataFrame(tracker, columns = ['Run','Remaining Input Rows', 'Cutoff Key (before each run)', 'Number of I/O Ops'])
csv_file_path = "metrics_{}.csv".format(filename)
df.to_csv(csv_file_path, index=False)


if trad_ans == solution:
    print("Traditional External Merge Sort: Passed")
else:
    print("Traditional External Merge Sort: Failed")

if opt_ans == solution:
    print("Optimized External Merge Sort: Passed")
else:
    print("Optimized External Merge Sort: Failed")