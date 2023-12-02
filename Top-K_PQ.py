import heapq
import xml.etree.ElementTree as ET

def max_push(heap, val):
        heapq.heappush(heap, -val)

def max_pop(heap):
        return -heapq.heappop(heap)

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


def top_k_PQ(list, k):
    pq = []

    #push the first k into the priority queue
    for _ in range(k):
        max_push(pq,list[_])

    #set initial cutoff key (largest element in the queue)
    cutoff_key = -pq[0]

    #compare rest of elements and push if smaller than the cutoff key
    for element in list[k:]:
        if(cutoff_key > element):
            max_pop(pq)
            max_push(pq, element)

            #re-assign cutoff_key
            cutoff_key = -pq[0]

    return pq, cutoff_key

dataset = [] 

#aggregate datasets into one
for i in range(1,6):
    dataset_path = '1_Mil_Dataset_{}/basic_database.xml'.format(i)
    dataset_partition = load(dataset_path)
    dataset.extend(dataset_partition)

k_options = [1000,5000]
data_sizes = [500000,1000000,5000000]
#generate the topk with pq
for k in k_options:
    for s in data_sizes:
        print('\nK size: ' + str(k) + ', Data Size: ' + str(s))
        pq,cutoff_key = top_k_PQ(dataset[:s],k)
        print('kth Element: '+str(-pq[0]))
        print('Cutoff Key: '+ str(cutoff_key))
        
