import heapq

class ExternalMergeSort:

    # The list that represents the main memory of the system.
    # Throughout the execution of the program, the size of the list will never exceed the value of M
    main_memory = []

    # The list that represents the disk in main memory
    disk = []

    # Output buffer (size of one block B)
    output_buffer = []

    # The size of main memory (number of objects that can fit in main memory)
    M = 0

    # Block size (number of objects that can fit in one block)
    B = 0

    # M // B (number of blocks that can fit into main memory, rounded down)
    m = 0

    # Number of I/O operations will be the metric to track time complexity
    num_IO_operations = 0

    tracker = []

    # Initialize the variables and system components
    def __init__ (self, main_memory_size, block_size, disk):
        self.M = main_memory_size
        self.B = block_size
        self.m = self.M // self.B
        self.disk = disk
        self.tracker = []
        
    
    # The simluation of traditional external merge sort
    def traditional_external_merge_sort(self):

        # If the block-size to main-memory-size ratio is not conducive of a sort, alert the user and terminate
        if (self.M // self.B) <= 1:
            print("Set a reasonable ratio for block-size to main-memory-size (must be able to fit more than one block in main memory).")
            exit(1)

        # Variable to keep track of the number of runs generated
        num_runs = 0
        
        while not self.all_elements_are_arrays():

            # Bring form disk a section of elements that are the size of main memory
            self.main_memory = self.disk[num_runs:num_runs+self.M]

            # Sort them in main memory using a classic sort
            self.main_memory = sorted(self.main_memory)

            # Write the sorted run back to disk
            del self.disk[num_runs:num_runs+self.M]
            self.disk.insert(num_runs, self.main_memory)

            num_runs+=1
            self.num_IO_operations += 2
        

        self.merge_step(num_runs)
        return self.disk
    
    def optimized_external_merge_sort(self, k):
        
        # Optimized merge sort makes use of a sharpening filter 
        sharpening_filter = None

        # Ths optimized version focuses on problem instances where k is less than the size of main memory
        if k < self.M:

            # If the block-size to main-memory-size ratio is not conducive of a sort, alert the user and terminate
            if (self.M // self.B) <= 1:
                print("Set a reasonable ratio for block-size to main-memory-size (must be able to fit more than one block in main memory).")
                exit(1)
        
            # Variable to keep track of the number of runs generated
            num_runs = 0

            # A disk pointer to keep track of the location in the disk
            disk_pointer = 0
            rows_left = len(self.disk)
            
            while not self.all_elements_are_arrays():

                self.tracker.append([num_runs+1,rows_left,sharpening_filter, self.num_IO_operations])
                # Bring from disk a section of elements that are the size of main memory
                self.main_memory = self.disk[num_runs:num_runs+self.M]
                rows_left -= self.M
                
                # Move the disk pointer
                disk_pointer = num_runs + self.M

                if sharpening_filter != None:

                    # Use sharpening filter to filter out input as it arrives
                    self.main_memory = [value for value in self.main_memory if value <= sharpening_filter]
                    
                    # The filter is refinable in this case
                    refinable = True

                    # After filtering, we want to load more elements into main memory, but only do so if we have less than k elements loaded
                    while (len(self.main_memory) < k):

                        # Refill main memory will new additional items
                        additional_items = self.disk[disk_pointer:disk_pointer+self.M-len(self.main_memory)]
                        disk_pointer += self.M-len(self.main_memory)
                        rows_left -= self.M-len(self.main_memory)

                        # If there are no more items to process, there is no more need to refine the filter and we can halt the reading process
                        if additional_items == []:
                            refinable = False
                            break

                        # Add the additional items to main memory
                        self.main_memory.extend(additional_items)
                        
                        # We had to do an I/O to read from disk
                        self.num_IO_operations +=1

                        # Filter from main memory again using the sharpening filter, and repeat
                        self.main_memory = [value for value in self.main_memory if value <= sharpening_filter]
                        
                    # Sort the main memory
                    self.main_memory = sorted(self.main_memory)
                    

                    if refinable:

                        # Refine the sharpening filter based on the current run
                        sharpening_filter = self.main_memory[k-1]
                        
                        # Use the new sharpening filter to refine the current run one last time before writing it to disk
                        self.main_memory = self.main_memory[0:k]

                # Else block executes if we do not have a sharpening filter yet
                else:

                    # Sort them in main memory using a classic sort
                    self.main_memory = sorted(self.main_memory)
                    
                    # Derive a sharpening filter based on the first run
                    sharpening_filter = self.main_memory[k-1]
                    
                    # Filter the first run
                    self.main_memory = self.main_memory[0:k]
        

                # Write the sorted run back to disk
                del self.disk[num_runs:disk_pointer]
                self.disk.insert(num_runs, self.main_memory)
                num_runs+=1

                # Writing costs one I/O
                self.num_IO_operations +=1
            
            # Once all the pre-processing and run generation are done, perform the merge step
            self.merge_step(num_runs)
            

            return self.disk
        
        # K >= M, so warn and terminate
        print("Failed Optimized Sort. Set a k that is smaller than the main memory size. For larger k, see histogram approach.")


    def top_k_with_traditional_external_merge_sort(self, k):

        # Invoke the traditional external merge sort
        self.traditional_external_merge_sort()

        # Perform the top-k and return results
        return self.perform_top_k(k)
    
    def top_k_with_optimized_external_merge_sort(self, k):

        # Invoke the optimized external merge sort
        self.optimized_external_merge_sort(k)

        # Perform the top-k and return results
        return self.perform_top_k(k)

        
    def perform_top_k(self, k):

        # The output list that will have the top-k elements. 
        # Each read from disk could have been read to main memory, then moved the the output list, but the extra steps can be assumed
        # and are overall unimportant to the evaluation metrics and understanding of the algorithm
        top_k = []

        # Disk pointer to keep track of location in disk
        disk_pointer = 0

        while k > 0:
            if k < self.M:
                top_k.extend(self.disk[disk_pointer:disk_pointer+k])
                k -= k
                disk_pointer += k
            else:
                top_k.extend(self.disk[disk_pointer:disk_pointer+self.M])
                k -= self.M
                disk_pointer += self.M

            # Each read from disk costs one I/O
            self.num_IO_operations+=1

        return top_k

    # Writes the output block to disk and flushes the output block
    def write_output_block_to_disk(self):
        self.disk[0] += self.output_buffer
        self.output_buffer = []

        # Increment the number of I/O performed
        self.num_IO_operations+=1
                        
    # Loads at most one block from disk into main memory from the specified run
    def load_block_from_disk(self, run_index):

        max_load = min(self.B, len(self.disk[run_index]))
        tuples = [(value, run_index, False) for value in self.disk[run_index][0:max_load-1]]
        tuples.append((self.disk[run_index][max_load-1], run_index, True))
        self.main_memory.extend(tuples)
        heapq.heapify(self.main_memory)
        del self.disk[run_index][0:max_load]

        # Increment the number of I/O performed
        self.num_IO_operations+=1

    # Remove all sublists in the disk so it is one connected list
    def collapse_disk(self):
        self.disk = [item for sublist in self.disk for item in sublist]

    # Helper function that will check if all elements in a list are themselves lists. Aids with run-generation
    def all_elements_are_arrays(self):
            for elem in self.disk:
                if not isinstance(elem, list):
                    return False
            return True
        
    def merge_step(self, num_runs):
        # Keep track of the current run in processing
        current_run = 0

        # Keep track of the number of runs generated (that will become the input to the next phase of merges)
        next_phase_num_runs = 0

        # Flush main memory
        self.main_memory = []

        # Insert a new partition into main memory to receive the blocks from the output buffer
        self.disk.insert(0, [])

        self.output_buffer = []
        
        # Terminate when there is a single run left, namely the sorted list of elements
        while num_runs != 1:
            while current_run < num_runs:
                
                # Load one block from each of m runs, thereby filling main memory
                for i in range(current_run, current_run + self.m):
                    
                    if self.disk[i+1]:
                        self.load_block_from_disk(i+1)
                    
                    if i == num_runs-1:
                        break
                    
                while self.main_memory:
                    # Pop from main memory the smallest value, the run it came from, and whether it is the last of its run
                    key, run_index, is_last_flag = heapq.heappop(self.main_memory)

                    # Append this element to the output buffer
                    self.output_buffer.append(key)

                    # If the output buffer is full, write it back to disk
                    if (len(self.output_buffer) % self.B == 0):
                        self.write_output_block_to_disk()
        
                    # If the element is last in its run, load another block from that run from the disk into main memory
                    if is_last_flag:
                        if self.disk[run_index]:
                            self.load_block_from_disk(run_index)
                
                # Write the remainder of what is in the output block to the disk
                self.write_output_block_to_disk()

                # Consider the following two actions as atomic: move the sorted run from the disk accumulator to the run section 
                self.disk[(current_run // self.m) + 1] = self.disk[0]
                self.disk[0] = []
                
                # Increment the number of runs to process in the next phase
                next_phase_num_runs +=1

                # The program finishes with m runs, so increment current_run by m
                current_run += self.m

            # Set the new number of runs to be the runs calculated for the next phase
            num_runs = next_phase_num_runs

            # Reset the tracking variables
            current_run = 0
            next_phase_num_runs = 0
            
        
        # Collapse the disk into a single output array
        self.collapse_disk()
        