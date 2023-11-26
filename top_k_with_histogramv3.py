import heapq
import random
import heapq
from heapq import _heapify_max, _heappop_max, _siftdown_max
import pandas as pd
import numpy as np

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
    

def top_k_with_histogram(inputs, k, bucket_size=100, memory_size = 1000):

    histogram_queue = []   #Priority Queue
    _heapify_max(histogram_queue) #Max Heap Construction
    cutoff_key = float('inf')
    histogram_data_total = 0
    run_cnt = 0
    run_gen = []  
    Tracker = []
    secondary_cnt, secondary_memory = 0, []
    
    
    while inputs: 
        # Reading item one by one; until the list is empty
        
        if len(run_gen) < memory_size:

            new_item = inputs.pop(0)
            run_gen.append(new_item)
            
            
        if len(run_gen) == memory_size:
            # If the run generation is full, sort the run generation and split the list by bucket
            run_gen.sort()
            bucket_list = [run_gen[i:i + bucket_size] for i in range(0, len(run_gen), bucket_size)]
            bucket_key = [(bucket[-1], len(bucket))for bucket in bucket_list]
            bucket_quartile = [i[0] for i in bucket_key]
            
            for i in bucket_key:
                # Add the boundary key from each bucket into the max heap
                if histogram_data_total < k:
                    heappush_max(histogram_queue, i)
                    
                elif histogram_data_total >= k and i[0] < cutoff_key:
                    discard_bucket = _heappop_max(histogram_queue)
                    histogram_data_total -= discard_bucket[1]
                    heappush_max(histogram_queue, i)
                    
                histogram_data_total += i[1]
                cutoff_key = histogram_queue[0][0]
                
            inputs = remove_below_cutoff(cutoff_key, inputs)
            run_cnt += 1
            secondary_cnt += len(run_gen)
            secondary_memory.append(run_gen)
            Tracker.append([run_cnt, len(inputs), cutoff_key, secondary_cnt] + bucket_quartile)
            run_gen = []
            
    if len(run_gen) > 0:
        # Add the last run generations into the secondary memory
        run_gen.sort()
        bucket_list = [run_gen[i:i + bucket_size] for i in range(0, len(run_gen), bucket_size)]
        bucket_key = [(bucket[-1], len(bucket))for bucket in bucket_list]
        bucket_quartile = [i[0] for i in bucket_key]
        secondary_memory.append(run_gen)
        secondary_cnt += len(run_gen)
        run_cnt += 1
        Tracker.append([run_cnt, len(inputs), cutoff_key, secondary_cnt]+bucket_quartile)
        
    Secondary_to_Main = sum(secondary_memory,[])
    topk = sorted(Secondary_to_Main)[:k]          
            
    return histogram_queue, Tracker, topk
    
    
   
            
    


input_size = 10000000
k = 5000
memory_size = 1000
bucket_size = 100

inputs = generate_data(input_size)
Result = top_k_with_histogram(inputs, k, bucket_size, memory_size)
print(Result[2])
df_result = pd.DataFrame(Result[1], columns = ['RunNum', 'Remaining_Inputs', 'CutOff', 'Secondary_Cnt', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
df_result.to_csv("Exp1.csv")
