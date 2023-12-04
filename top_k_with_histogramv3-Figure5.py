import heapq
import random
import heapq
from heapq import _heapify_max, _heappop_max, _siftdown_max
import pandas as pd
import numpy as np
from statistics import median

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
            prior_key = cutoff_key
            prior_input_size = len(inputs)
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
                
            if histogram_data_total >= k:
                inputs = remove_below_cutoff(cutoff_key, inputs)
            run_cnt += 1
            secondary_cnt += len(run_gen)
            secondary_memory.append(run_gen)
            Tracker.append([run_cnt, prior_input_size + len(run_gen), prior_key, secondary_cnt] )
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
        Tracker.append([run_cnt, len(run_gen), cutoff_key, secondary_cnt])
        
    Secondary_to_Main = sum(secondary_memory,[])
    topk = sorted(Secondary_to_Main)[:k]          
            
    return histogram_queue, Tracker, topk
    
    
   
          
   
            
    

Experiment = 3
input_size = 1000000
k = 5000
memory_size = 1000
bucket_size = 100
Result_list = []
for k in [1000,2000,5000,10000,20000,50000]:
    random.seed(10)
    inputs = generate_data(input_size)
    Result = top_k_with_histogram(inputs, k, bucket_size, memory_size)
    #print(Result[2])
    Result_list.append([k] + Result[1][-1])
                             
                             
                             
df_result = pd.DataFrame(Result_list, columns = ['k','RunNum', 'Remaining_Inputs', 'CutOff', 'Secondary_Cnt'])
df_result.to_csv("Table_"+str(Experiment)+"_Final.csv")

