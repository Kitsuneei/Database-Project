import heapq
import random


# generate random data set each time to test the correctness
def generate_data(size):
    return [random.randint(1, 100) for _ in range(size)]


def top_k_with_histogram(data, k, bucket_size=1):
    # print the orginal randomly generated numbers
    print("Array of Numbers:", data)

    # for storing the buckets
    histogram_queue = []
    total_elements_processed = 0

    # the threshold, initliazed to negeative infinity and will be refined later on
    cutoff_key = float('-inf')

    for value in data:
        # bucket: a tuple consisting of a value and a count
        bucket = (value, 1)

        # insert bucket into the histogram queue
        heapq.heappush(histogram_queue, bucket)
        total_elements_processed += 1

        # the while loop find a threshold that separates the top-k elements from the rest of the dataset
        # check if the sum of bucket sizes in the queue is greater than or equal to k
        while sum(bucket[1] for bucket in histogram_queue) > k:
            # pop the bucket with the smallest value
            popped_bucket = heapq.heappop(histogram_queue)

            # update the thereshold
            cutoff_key = popped_bucket[0]

            # refine the thereshold based on the next smaller key
            if histogram_queue:
                next_smaller_key = heapq.heappop(histogram_queue)[0]
                heapq.heappush(histogram_queue, (next_smaller_key, 1))
                cutoff_key = next_smaller_key

    # calculation of the remaining data after the seperation based on the threshold
    # initialize input model with the remaining histogram data
    input_model_histograms = histogram_queue

    # refine the threshold key while writing runs
    for _ in range(k):
        run_data = generate_data(10)
        run_histogram = [(value, 1) for value in run_data]

        # combine the histogram of the current run with the input model
        input_model_histograms.extend(run_histogram)

        # update threshold
        input_model_histograms.sort(reverse=True)
        cutoff_key = min(input_model_histograms[k - 1][0], cutoff_key)

    top_k_elements = sorted(
        [value for value in data if value >= cutoff_key], reverse=True)[:k]

    return top_k_elements


# show result
data = generate_data(50)
k = 5

result = top_k_with_histogram(data, k)
print("Top", k, "elements:", result)
