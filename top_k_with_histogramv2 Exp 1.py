import heapq
import random
import heapq
from heapq import _heapify_max, _heappop_max, _siftdown_max
import pandas as pd

random.seed(10)

# generate random data set each time to test the correctness
def generate_data(size):
    return [random.random() for _ in range(size)]

def heappush_max(max_heap, item): 
    #Max Heap Helper function
    max_heap.append(item)
    _siftdown_max(max_heap, 0, len(max_heap)-1)
    
def remove_below_cutoff(cutoff_key, inputs):
    #Remove subsequent inputs after updating the cutoff key
    return [i for i in inputs if i <= cutoff_key]
    

def top_k_with_histogram(inputs, k, bucket_size=5, memory_size = 10):

    histogram_queue = []   #Priority Queue
    _heapify_max(histogram_queue) #Max Heap Construction
    cutoff_key = float('inf')
    secondary_memory = [] # Secondary Memory
    Tracker = []
    
    bucket = [] # We will keep feeding new item into the bucket
    run_gen = []  # Run generation; if the list grows large enough (size of secondary memory), the run generations will be transferred to the secondary memory
    run_cnt = 0
    secondary_cnt = 0
    
    while inputs: 
        # Reading item one by one; until the list is empty
        
        if len(bucket) < bucket_size:
            # Fill up the bucket until it is full;
            # Remove the first element from the inputs
            # Each data will be stored in the bucket list (to calculate the bucket key -> will be used in the max heap)
            # Each data will be stored in the run_gen list (it is a run generation and it will be moved to the secondary memory if needed)
            new_item = inputs.pop(0)
            bucket.append(new_item)
            run_gen.append(new_item)
            
            
        if len(bucket) == bucket_size:
            # If the bucket is full, obtain the boundary key
            bucket.sort()
            bucket_key = bucket[bucket_size-1]
            
            if len(histogram_queue) * bucket_size < k:
                # Initialization: if size of the max heap is smaller than K, we keep inserting new tuples to the max heap until it is full
                heappush_max(histogram_queue, (bucket_key, len(bucket)))
                
                
            elif len(histogram_queue) * bucket_size >= k and bucket_key < cutoff_key:
                # Maintenance: If the size of the max heap is larger than K and the boundary key is smaller than the cutoff key
                # We should pop the cut off key (currently the first element in the max heap) and insert the boundary key to the heap
                _heappop_max(histogram_queue)
                heappush_max(histogram_queue, (bucket_key, len(bucket)))
                    
            # Update the cutoff key
            cutoff_key = histogram_queue[0][0]
                
            # The bucket is either inserted to the max heap or do not need to be worried about. Initialize the list for next input element
            bucket=[]
            
            
        if len(run_gen) >= memory_size:
            # If length of run_gen is larger or equal to the secondary memory size, move the run generation to there
            secondary_memory.append(run_gen)
            inputs = remove_below_cutoff(cutoff_key, inputs)  # Remove the data elements in Inputs if it is smaller than cutoff key - It reduces the memory need
            secondary_cnt += len(run_gen)
            print("Run: ", run_cnt, "Input Remains: ", len(inputs), "Cut off Key: ", cutoff_key) 
            #quartiles_stat = np.quantile(run_gen, [0,0.25,0.5,0.75,1])
            run_cnt += 1
            Tracker.append([run_cnt, len(inputs), cutoff_key, secondary_cnt])
            run_gen = []

      
    if len(run_gen) > 0:
        # Add the last run generations into the secondary memory
        secondary_memory.append(run_gen)
        secondary_cnt += len(run_gen)
        run_cnt += 1
        Tracker.append([run_cnt, len(inputs), cutoff_key, secondary_cnt])
        
    
    Secondary_to_Main = sum(secondary_memory,[])
    topk = sorted(Secondary_to_Main)[:k]
    
    return histogram_queue, topk, cutoff_key, Tracker
    
    
   
            
    


input_size = 1000000
k = 5000
memory_size = 1000
bucket_size = 100

inputs = generate_data(input_size)
#print(inputs)
Result = top_k_with_histogram(inputs, k, bucket_size, memory_size)
print("Final: ", Result[1])
df_result = pd.DataFrame(Result[3], columns = ['RunNum', 'Remaining_Inputs', 'CutOff', 'SecondarySize'])
df_result.to_csv("Exp1.csv")
