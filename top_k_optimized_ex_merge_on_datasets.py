import xml.etree.ElementTree as ET
import top_k_with_external_merge_sort as ems
import pandas as pd

# Function to load a dataset from XML format into an array
def load(dataset_path):

    # Parse the XML file
    tree = ET.parse(dataset_path)
    root = tree.getroot()

    order_key_arr = []

    # Access elements and attributes
    for child in root:

        # Access element data
        for index, sub_element in enumerate(child):
            if index == 0:
                order_key_arr.append(int(sub_element.text))

    return order_key_arr

# Main dataset of 5 million elements
main_dataset = []

# Combine all datasets
for i in range(1,6):
    dataset_path = '1_Mil_Dataset_{}/basic_database.xml'.format(i)
    dataset_partition = load(dataset_path)
    main_dataset.extend(dataset_partition)

# All the K-N combos of interest for our experiments
K_N_combos = [
    [1000,500000],
    [1000,1000000],
    [1000,5000000],
    [5000,500000],
    [5000,1000000],
    [5000,5000000]
]

k_th_element_arr = []

# Fix Main memory size
M = 1000
B = 64

# For each test-case
for combo in K_N_combos:

    # Extract K and N
    K = combo[0]
    N = combo[1]

    # Init the thest case
    test_case = main_dataset[:N]
            
    # This will be the solution
    solution = sorted(test_case)[:K]

    # Verbose
    print("Test case with parms: [M={},B={},K={},N={}]".format(M,B,K,N))

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
    csv_file_path = 'dataset_metrics_{}_{}.csv'.format(K,N)
    df.to_csv(csv_file_path, index=False)

    if trad_ans == opt_ans and opt_ans == solution:
        print(opt_ans)
        print("Traditional External Merge Sort: Passed\nOptimized External Merge Sort: Passed")
        k_th_element_arr.append(opt_ans[-1])

    if trad_ans != solution:
        print("Traditional External Merge Sort: Failed")
        exit(1)

    if opt_ans != solution:
        print("Optimized External Merge Sort: Failed")
        exit(1)

# Print out the k_th_element in the top-k of each test for validation purposes
print(k_th_element_arr)


    
