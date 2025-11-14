# Idea: acting as a common interface for all algorithms
from memory_management.page import Page
from typing import List

class SimulationResult: 
    # data container to store the stats from simulation runs
    def __init__(self): 
        self.page_faults = 0        # total page faults (page not in RAM)
        self.hits=0                 # page hits (found in memory)
        self.misses = 0             # page requested not found in current frames
        self.timeline = []          # keeps track of memory state frames at each access
        self.total_accesses = 0     # total # of memory references processed.

# Converts the list of Page objects currently loaded in memory into a list of their IDs
def framesToIds(frames : List[Page]): 
    return [p.id if p is not None else None for p in frames]

