from WriteBackCache import WriteBackCache
import math

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
        return lru_entry

    def add_victim(self):
        self.victim_cache.add(evict_entry()) #Add the address to victim cache


class ThreeLevelCache:
    def __init__(self, l1_size, l1_block_size, l1_associativity, l2_size, l2_block_size, l2_associativity, victim_size, victim_block, victim_associativity):
        self.l1_instruction_cache = WriteBackCache(l1_size, l1_block_size, l1_associativity)
        self.l1_data_cache = WriteBackCache(l1_size, l1_block_size, l1_associativity)
        self.l2_cache = WriteBackCache(l2_size, l2_block_size, l2_associativity)
        self.victim_cache = WriteBackCache(victim_size, victim_block, victim_associativity)
        
        self.total_instruction_accesses = 0
        self.total_data_accesses = 0
        self.total_l2_accesses = 0
        self.total_victim_accesses = 0
        self.total_l1_instruction_misses = 0
        self.total_l1_data_misses = 0
        self.total_l2_misses = 0
        self.total_victim_misses = 0
        self.instruction_hits = 0
        self.data_hits = 0
        self.l2_hits = 0
        self.victim_hits = 0

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

        # # Update total access counts for both instruction and data caches
        self.total_instruction_accesses += 1 if action == 2 else 0
        self.total_data_accesses += 1 if action == 0 else 0

        if entry and entry.valid:
          if entry.dirty: # when dirty bit = 1, the block has been revised -> write to memory
              self.write(action, address)
              entry.dirty = False
            #   cache_set.update_LRU(entry) # Update LRU
          else: # Read
              cache_set.update_LRU(entry) # Update LRU
              entry.dirty = False
              if action == 2: # Instruction read
                  self.instruction_hits += 1
              elif action == 0: # Data read
                  self.data_hits += 1
              return "Cache hit"
        else: # Read from memory
            self.total_misses += 1 
            if not self.is_cache_full(): # Need to store in victim cache
                new_entry = CacheBlock(tag) # Create a new CacheBlock
                new_entry.valid = True
                new_entry.dirty = True
                cache_set.entries.append(new_entry) # Append the CacheBlock to cache
                cache_set.update_LRU(new_entry) # Update LRU
            else:
              if victim_cache.is_cache_full():
                cache_set.evict_entry()
              else:
                cache_set.add_victim(evict_entry()) # if the cache is full remove one least used address
              new_entry = CacheBlock(tag)
              new_entry.valid = True
              new_entry.dirty = False
              cache_set.entries.append(new_entry)
              cache_set.update_LRU(new_entry)
            return "Cache miss"

    def write(self, action, address):
        set_index = address // self.block_size % self.num_sets
        tag = self.get_tag(address)
        cache_set = self.sets[set_index]
        entry = cache_set.find_entry(tag)
        self.total_data_accesses += 1 # Data write

        if entry:
            entry.valid = True
            entry.dirty = True
            cache_set.update_LRU(entry)
            return "Cache hit"
        else:
            if not self.is_cache_full():
                new_entry = CacheBlock(tag, None)
                new_entry.valid = True
                # new_entry.dirty = True
                cache_set.entries.append(new_entry)
                cache_set.update_LRU(new_entry)
            else:
              if victim_cache.is_cache_full():
                  cache_set.evict_entry()
              else:
                cache_set.add_victim(evict_entry())
              new_entry = CacheBlock(tag, None)
              new_entry.valid = True
              # new_entry.dirty = True
              cache_set.entries.append(new_entry)
              cache_set.update_LRU(new_entry)
            return "Cache miss"

    def access_cache(self):
        with open(trace_file, 'r') as file:
            for line in file:
              action, address = [int(x, 16) for x in line.strip().split()]
              if action == 0: # data read
                  self.total_data_accesses += 1
                  result = self.l1_data_cache.read(action, address)
                  if result == "Cache miss":
                      self.total_l1_data_misses += 1
                      victim_result = self.victim_cache.read
                      (action, address)
                      self.total_victim_accesses += 1
                      if victim_result == "Cache miss":
                          self.total_victim_misses += 1
                          L2_result = self.l2_cache.read(action, address)
                          self.total_victim_misses += 1
                          self.total_l2_accesses += 1
                          if L2_result == "Cache miss":
                              self.total_l2_misses += 1
                          else:
                              self.l2_hits += 1
                      else:
                        self.victim_hits += 1
                  else:
                      self.data_hits += 1
              elif action == 2: # instruction read
                  self.total_instruction_accesses += 1
                  result = self.l1_instruction_cache.read(action, address)
                  if result == "Cache miss":
                      self.total_l1_instruction_misses += 1 
                      victim_result = self.victim_cache.read
                      (action, address)
                      self.total_victim_accesses += 1
                      if victim_result == "Cache miss":
                          self.total_victim_misses += 1
                          L2_result = self.l2_cache.read(action, address)
                          self.total_l2_accesses += 1
                          if L2_result == "Cache miss":
                              self.total_l2_misses += 1
                          else:
                              self.l2_hits += 1
                      else:
                          self.victim_hits += 1
                  else:
                      self.instruction_hits += 1
              else: # data write
                  self.total_data_accesses += 1
                  result = self.l1_data_cache.write(action, address)
                  if result == "Cache miss":
                      self.total_l1_data_misses += 1 
                      victim_result = self.victim_cache.write
                      (action, address)
                      self.total_victim_accesses += 1
                      if victim_result == "Cache miss":
                          self.total_victim_misses += 1
                          L2_result = self.l2_cache.write(action, address)
                          self.total_l2_accesses += 1
                          if L2_result == "Cache miss":
                              self.total_l2_misses += 1
                          else:
                              self.l2_hits += 1
                      else:
                          self.victim_hits += 1
                  else:
                      self.data_hits += 1   
        self.print()
    def calculate_AMAT(self):
        # 计算AMAT
        l1_instruction_miss_rate = self.total_l1_instruction_misses / self.total_instruction_accesses if self.total_instruction_accesses else 0
        l1_data_miss_rate = self.total_l1_data_misses / self.total_data_accesses if self.total_data_accesses else 0
        if self.total_l2_accesses == 0:
          l2_miss_rate = 0
        else:
          l2_miss_rate = self.total_l2_misses / (self.total_l2_accesses)
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
            if self.total_l2_accesses == 0: 
              L2_hit_rate = 0
            else:
              L2_hit_rate = self.l2_hits/self.total_l2_accesses* 100
            L2_hit_rate = f"{L2_hit_rate:.2f}%"
            print("L2 hit rate:", L2_hit_rate)
            print("Victim Accesses:", self.total_victim_accesses)
            print("Victim Misses:", self.total_victim_misses)
            victim_hit_rate = self.victim_hits/self.total_victim_accesses*100
            victim_hit_rate = f"{victim_hit_rate:.2f}%"
            if self.total_l2_accesses == 0: 
              L2_hit_rate = 0
            else:
              L2_hit_rate = self.l2_hits/self.total_l2_accesses* 100
            L2_hit_rate = f"{L2_hit_rate:.2f}%"
            print("Victim_hit_rate:", victim_hit_rate)
            print("AMAT:", self.calculate_AMAT())         

def simulate_three_level_cache(trace_file, l2_associativity, victim_associativity):

    # two_level_cache_system = TwoLevelCache(1024, 32, 2, 16384, 128, 4)  # 示例参数
    l1_instruction_cache = WriteBackCache(total_size=1024, block_size=32, set_associativity=2)
    l1_data_cache =  WriteBackCache(total_size=1024, block_size=32, set_associativity=2)
    l2_cache = WriteBackCache(total_size=16384, block_size=128, set_associativity=l2_associativity)
    victim_cache = WriteBackCache(total_size=32, block_size=32, set_associativity=victim_associativity)


    three_caches = ThreeLevelCache(l1_size = 1024,l1_block_size = 32, l1_associativity=2, l2_size = 16384, l2_block_size = 128, l2_associativity = l2_associativity, victim_size = 16384, victim_block = 128, victim_associativity=victim_associativity)
    
    print("Set L2 associativity:", l2_associativity,"/ Set Victim associativity:", victim_associativity )
    three_caches.access_cache()

trace_file = 'cc.trace'
for l2_associativity, victim_associativity in [(a, b) for a in [1, 2, 4, 8, 16, 32] for b in [1, 2, 4, 32, 64, 128]]:
    simulate_three_level_cache(trace_file, l2_associativity, victim_associativity)



