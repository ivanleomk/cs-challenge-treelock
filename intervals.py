x = [[0,2],[3,6],[2,5],[2,12]]

def find_overlap(interval_1,interval_2):
    start_1,end_1 = interval_1
    start_2,end_2 = interval_2

    return max(start_1,start_2),min(end_1,end_2)

def find_overlapping_interval(intervals):
    #Sort by the front
    intervals.sort(key=lambda x: x[0])

    lastSeen = intervals[0]
    merging = False
    
    for index,item in enumerate(intervals):
        if index == 0: continue

        start,end = item
        prev_start,prev_end = lastSeen

        if merging:
            #If we have found the end of an interval
            if start > prev_end:
                merging = False
                return lastSeen
            lastSeen = find_overlap(lastSeen,item)
            continue
            
        if prev_end <= start:
            merging = True
            lastSeen = item

    return lastSeen

print(find_overlapping_interval(x))