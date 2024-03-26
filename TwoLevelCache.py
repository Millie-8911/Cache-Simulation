from WriteBackCache import WriteBackCache
import math
import table_print

class CacheBlock:
    def __init__(self, tag=None, data=None):
        self.valid = False
        self.tag = tag
        self.data = data
        self.last_accessed = 0  # Record the latest visit time
        self.dirty = False 

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


class TwoLevelCache:
    def __init__(self, l1_instruction_cache, l1_data_cache,l2_cache, l1_size, l1_block_size, l1_associativity, l2_size, l2_block_size, l2_associativity):
        self.l1_instruction_cache = l1_instruction_cache
        self.l1_data_cache = l1_data_cache
        self.l2_cache = l2_cache
        

        self.total_instruction_accesses = 0
        self.total_data_accesses = 0
        self.total_l2_accesses = 0
        self.total_l1_instruction_misses = 0
        self.total_l1_data_misses = 0
        self.total_l2_misses = 0
        self.instruction_hits = 0
        self.data_hits = 0
        self.l2_hits = 0

    def access_cache(self, trace_file):
        with open(trace_file, 'r') as file:
            for line in file:
              action, address = [int(x, 16) for x in line.strip().split()]
              if action == 0: # data read
                  self.total_data_accesses += 1
                  result = self.l1_data_cache.read(action, address)
                  if result == "Cache miss":
                      self.total_l1_data_misses += 1 
                      L2_result = self.l2_cache.read(action, address)
                      self.total_l2_accesses += 1
                      if L2_result == "Cache miss":
                          self.total_l2_misses += 1
                      else:
                          self.l2_hits += 1
                  else:
                      self.data_hits += 1
              elif action == 2: # instruction read
                  self.total_instruction_accesses += 1
                  result = self.l1_instruction_cache.read(action, address)
                  if result == "Cache miss":
                      self.total_l1_instruction_misses += 1 
                      L2_result = self.l2_cache.read(action, address)
                      self.total_l2_accesses += 1
                      if L2_result == "Cache miss":
                          self.total_l2_misses += 1
                      else:
                          self.l2_hits += 1
                  else:
                      self.instruction_hits += 1
              else: # data write
                  self.total_data_accesses += 1
                  result = self.l1_data_cache.write(action, address)
                  if result == "Cache miss":
                      self.total_l1_data_misses += 1 
                      L2_result = self.l2_cache.write(action, address)
                      self.total_l2_accesses += 1
                      if L2_result == "Cache miss":
                          self.total_l2_misses += 1
                      else:
                          self.l2_hits += 1
                  else:
                      self.data_hits += 1   
        self.print()
    def calculate_AMAT(self):
        # 计算AMAT
        l1_instruction_miss_rate = self.total_l1_instruction_misses / self.total_instruction_accesses if self.total_instruction_accesses else 0
        l1_data_miss_rate = self.total_l1_data_misses / self.total_data_accesses if self.total_data_accesses else 0
        l2_miss_rate = self.total_l2_misses / (self.total_l2_accesses if self.total_l2_accesses else 0)
        
        l1h = 1  
        l2h = 10  
        l2m = 100  
        
        # 假设指令和数据缓存访问均分
        l1_miss_rate = (l1_instruction_miss_rate + l1_data_miss_rate) / 2
        amat = l1h + (l1_miss_rate * (l2h + (l2_miss_rate * l2m)))
        return amat
                
    def print(self):
            results = []
            # print('hits', self.l1_data_cache.data_hits, self.l1_instruction_cache.instruction_hits) # For testing
            print("L1 Instruction Accesses:", self.l1_instruction_cache.total_instruction_accesses)
            print("L1 Instruction Misses:", self.l1_instruction_cache.total_misses)
            instruction_hit_rate = self.l1_instruction_cache.instruction_hits / self.l1_instruction_cache.total_instruction_accesses * 100
            instruction_hit_rate = f"{instruction_hit_rate:.2f}%"
            print("Instruction hit rate:", instruction_hit_rate)
            print("L1 Data Accesses:", self.l1_data_cache.total_data_accesses)
            print("L1 Data Misses:", self.l1_data_cache.total_misses)
            data_hit_rate = self.l1_data_cache.data_hits / self.l1_data_cache.total_data_accesses * 100
            data_hit_rate = f"{data_hit_rate:.2f}%"
            print("Data hit rate:", data_hit_rate)
            print("L2 Accesses:", self.total_l2_accesses)
            print("L2 Missess:", self.total_l2_misses)
            L2_hit_rate = self.l2_hits/self.total_l2_accesses* 100
            L2_hit_rate = f"{L2_hit_rate:.2f}%"
            print("L2 hit rate:", L2_hit_rate)
            print("AMAT:", self.calculate_AMAT())    
            table_print.print_table_dict.L1I_accesses.append(self.l1_instruction_cache.total_instruction_accesses)
            table_print.print_table_dict.L1I_misses.append(self.l1_instruction_cache.total_misses)
            table_print.print_table_dict.L1D_accesses.append(self.l1_data_cache.total_data_accesses)
            table_print.print_table_dict.L1D_misses.append(self.l1_data_cache.total_misses)
            table_print.print_table_dict.L1I_hit_rate.append(instruction_hit_rate)
            table_print.print_table_dict.L1D_hit_rate.append(data_hit_rate)
            table_print.print_table_dict.AMAT.append(self.l1_instruction_cache.calculate_AMAT()) 
            table_print.print_table_dict.L2_accesses.append(self.total_l2_accesses)
            table_print.print_table_dict.L2_misses.append(self.total_l2_misses)
            table_print.print_table_dict.L2_hit_rate.append(L2_hit_rate)

def simulate_two_level_cache(l2_associativity):
    l1_instruction_cache = WriteBackCache(total_size=1024, block_size=32, set_associativity=16)
    l1_data_cache =  WriteBackCache(total_size=1024, block_size=32, set_associativity=16)
    l2_cache = WriteBackCache(total_size=16384, block_size=32, set_associativity=l2_associativity)

    two_caches = TwoLevelCache(l1_instruction_cache, l1_data_cache, l2_cache, l1_size = 1024,l1_block_size = 32, l1_associativity=16, l2_size = 16384, l2_block_size = 32, l2_associativity = l2_associativity)
    
    print("Set associativity:", l2_associativity)
    trace_file = 'cc.trace'
    two_caches.access_cache(trace_file)

    
for associativity in [1, 4, 16, 64,128]:
    simulate_two_level_cache(associativity)
table_print.print_table_dict.table2_print()