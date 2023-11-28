import queue
import random

#generate random data
def generate_data(size):
    return [random.randint(1, 100) for _ in range(size)]

def top_k_PQ(list, k):
    pq = queue.PriorityQueue()
    #push the first k into the priority queue
    for _ in range(k):
        pq.put(list[_])
    #compare rest of elements and push if greater than the smallest element in the queue
    for element in list[k:]:
        cutoff_key = pq.queue[0]
        if(cutoff_key < element):
            pq.get()
            pq.put(element)
    return pq

#print elements of the queue
def print_pq(pq):
    print_list = []
    while (pq.empty() == False):
        print_list.append(pq.get())
    print(print_list)

#generate and print the list of keys
list = generate_data(50)
print('\nDataset:')
print(list)

#generate the topk with pq
k = 5
pq = top_k_PQ(list, k)
print('\nTop-'+str(k)+' Elements:')
print_pq(pq)