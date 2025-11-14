# Idea: the oldest loaded page (first entered) is replaced first
from memory_management.page import Page
from algorithms.base import SimulationResult, framesToIds
from collections import deque
from typing import List, Optional, Dict, Deque, cast

def runFifo(reference: List[int], numFrames): 
    ''' 
    Arguments: 
        reference - list of page ids requested by the CPU
        numFrames - number of physical frames available in memory
    Returns:
        SimulationResult object w/ stats and timeline
    ''' 
    frames: List[Optional[Page]] = [None] * numFrames  
    queue: Deque[int] = deque() # stores the order of pages loaded into frames
    page_table: Dict[int, Page] = {} # maps page id to Page object
    time = 0 # simulation clock (+1 each access)

    res = SimulationResult() # store stats

    for ref in reference: 
        time += 1
        res.total_accesses += 1

        p = page_table.get(ref)
        # If Page is loaded in memory (page hit)
        if p and p.loaded:
            res.hits +=1
            p.last_access = time
            p.access_count += 1
        # If Page is not in memory (page miss)
        else: 
            res.page_faults += 1
            res.misses += 1
            # Crating a new Page if it doesn't exist
            if p is None: 
                p = Page(ref)
                page_table[ref] = p

            # find an empty frame or pick oldest loaded
            if None in frames: 
                fi = frames.index(None)
            else: 
                fi = queue.popleft()
                old_page = frames[fi]
                old_page.loaded = False 
                old_page.frame_index = None
            # load new page into chosen frame
            frames[fi] = p
            p.loaded = True 
            p.frame_index = cast(int, fi)
            p.loaded_at = time
            p.last_access = time
            p.access_count += 1
            # Add this frame index to the queue
            queue.append(fi)
        # Save current frame state to timeline
        res.timeline.append(framesToIds(frames))
    return res