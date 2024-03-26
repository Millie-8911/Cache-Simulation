import math
import table_print

class CacheBlock:
    def __init__(self, tag=None, data=None):
        self.valid = False
        self.tag = tag
        self.data = data
        self.last_accessed = 0  # Record the latest visit time

class Set:
    def __init__(self, associativity):
        self.entries = [CacheBlock() for _ in range(associativity)]

    def find_entry(self, tag):
        for entry in self.entries:
            if entry.valid and entry.tag == tag:
                return entry
        return None

    def update_LRU(self, accessed_entry):
        accessed_entry.last_accessed = max(entry.last_accessed for entry in self.entries) + 1 # Plus one to the address we just visited

    def evict_entry(self): # Call this function when cache is full
        lru_entry = min(self.entries, key=lambda x: x.last_accessed) # Find the least recent used address
        self.entries.remove(lru_entry) # Remove the address


class WriteThroughCache:
    def __init__(self, total_size, block_size, set_associativity, hit_time=1, miss_penalty=100):
        self.total_size = total_size
        self.block_size = block_size
        self.num_sets = total_size // (block_size * set_associativity)
        self.set_associativity = set_associativity
        self.sets = [Set(set_associativity) for _ in range(self.num_sets)]

        self.hit_time = hit_time
        self.miss_penalty = miss_penalty
        self.instruction_hits = 0
        self.data_hits = 0
        self.instruction_misses = 0
        self.total_data_accesses = 0
        self.total_instruction_accesses = 0
        self.total_misses = 0
        self.total_accesses = 0

    def get_tag(self, address):
        return address >> int(math.log2(self.num_sets) + math.log2(self.block_size))

    def is_cache_full(self):
        for cache_set in self.sets:
            if len(cache_set.entries) < self.set_associativity:
                return False
        return True

    def read(self, action, address):
        set_index = address // self.block_size % self.num_sets
        tag = self.get_tag(address) # Calculate tag
        cache_set = self.sets[set_index]
        entry = cache_set.find_entry(tag)

        # Update total access counts for both instruction and data caches
        self.total_instruction_accesses += 1 if action == 2 else 0
        self.total_data_accesses += 1 if action == 0 else 0

        if entry and entry.valid:
            cache_set.update_LRU(entry) # Update LRU
            if action == 2: # Instruction read
                self.instruction_hits += 1
            elif action == 0: # Data read
                self.data_hits += 1
            return "Cache hit"
        else:
            self.total_misses += 1
            if not self.is_cache_full():
                new_entry = CacheBlock(tag) # Create a new CacheBlock
                new_entry.valid = True
                cache_set.entries.append(new_entry) # Append the CacheBlock to cache
                cache_set.update_LRU(new_entry) # Update LRU
            else:
                cache_set.evict_entry() # if the cache is full remove one least used address
                new_entry = CacheBlock(tag)
                new_entry.valid = True
                cache_set.entries.append(new_entry)
                cache_set.update_LRU(new_entry)
            return "Cache miss"

    def write(self, action, address):
        set_index = address // self.block_size % self.num_sets
        tag = self.get_tag(address)
        cache_set = self.sets[set_index]
        entry = cache_set.find_entry(tag)
        self.total_misses += 1 # Each write regards as miss
        self.total_data_accesses += 1 # Data write
        
        if not self.is_cache_full():
            new_entry = CacheBlock(tag, None)
            new_entry.valid = True
            cache_set.entries.append(new_entry)
            cache_set.update_LRU(new_entry)
        else:
            cache_set.evict_entry()
            new_entry = CacheBlock(tag, None)
            new_entry.valid = True
            cache_set.entries.append(new_entry)
            cache_set.update_LRU(new_entry)
        return "Cache miss"

    def calculate_AMAT(self):
        self.total_accesses = self.total_instruction_accesses + self.total_data_accesses
        if self.total_accesses == 0:
            return 0
        miss_rate = self.total_misses / self.total_accesses
        amat = self.hit_time + miss_rate * self.miss_penalty
        rounded_amat = round(amat, 2)
        return rounded_amat

def simulate_cache(trace_file, l1_associativity):
    class TestWriteThrough(WriteThroughCache):
        def __init__(self, l1_instruction_cache, l1_data_cache):
            super().__init__(1024, 32, 1)  # Assuming default values for WriteThroughCache
            self.l1_instruction_cache = l1_instruction_cache
            self.l1_data_cache = l1_data_cache

        def read(self, action, address):
            if action == 2:
                result = self.l1_instruction_cache.read(action, address)
                return result
            elif action == 0:
                result = self.l1_data_cache.read(action, address)
                return result

        def write(self, action, address):
            if action == 1:
                result = self.l1_data_cache.write(action, address)
                return result

        def print(self):
            results = []
            print("L1 Data hits: ", self.l1_data_cache.data_hits)
            print("L1 Instruction hits: ", self.l1_instruction_cache.instruction_hits)
            print("L1 Instruction Accesses:", self.l1_instruction_cache.total_instruction_accesses)
            print("L1 Instruction Misses:", self.l1_instruction_cache.total_misses)
            print("L1 Data Accesses:", self.l1_data_cache.total_data_accesses)
            print("L1 Data Misses:", self.l1_data_cache.total_misses)
            instruction_hit_rate = self.l1_instruction_cache.instruction_hits / self.l1_instruction_cache.total_instruction_accesses * 100
            instruction_hit_rate = f"{instruction_hit_rate:.2f}%"
            print("Instruction hit rate:", instruction_hit_rate)
            data_hit_rate = self.l1_data_cache.data_hits / self.l1_data_cache.total_data_accesses * 100
            data_hit_rate = f"{data_hit_rate:.2f}%"
            print("Data hit rate:", data_hit_rate)
            print("AMAT:", self.l1_instruction_cache.calculate_AMAT())
            table_print.print_table_dict.L1I_accesses.append(self.l1_instruction_cache.total_instruction_accesses)
            table_print.print_table_dict.L1I_misses.append(self.l1_instruction_cache.total_misses)
            table_print.print_table_dict.L1D_accesses.append(self.l1_data_cache.total_data_accesses)
            table_print.print_table_dict.L1D_misses.append(self.l1_data_cache.total_misses)
            table_print.print_table_dict.L1I_hit_rate.append(instruction_hit_rate)
            table_print.print_table_dict.L1D_hit_rate.append(data_hit_rate)
            table_print.print_table_dict.AMAT.append(self.l1_instruction_cache.calculate_AMAT())

    l1_instruction_through = WriteThroughCache(total_size=1024, block_size=32, set_associativity=l1_associativity)
    l1_data_through = WriteThroughCache(total_size=1024, block_size=32, set_associativity=l1_associativity)

    test_write_through = TestWriteThrough(l1_instruction_through, l1_data_through)

    with open(trace_file, 'r') as file:
        for line in file:
            action, address = [int(x, 16) for x in line.strip().split()]
            if action == 0 or action == 2: # For read 
                test_write_through.read(action, address)
            else: # For write
                test_write_through.write(action, address) 

    print("Set associativity:", l1_associativity)
    test_write_through.print()


# trace_file = 'cc.trace'
# for l1_associativity in ([1, 2, 4, 8, 16, 32]):
#     simulate_cache(trace_file, l1_associativity)
# table_print.print_table_dict.table1_print()
