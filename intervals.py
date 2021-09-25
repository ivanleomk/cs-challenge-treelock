# x = [[0,2],[3,6],[2,5],[2,12]]

x = [{'from': 717649920, 'to': 900723920}], [{'from': 323563706, 'to': 836556107}], [{'from': 96021970, 'to': 98042557}], [{'from': 180425524, 'to': 513015509}]

def find_overlap(interval_1,interval_2):
    start_1,end_1 = interval_1
    start_2,end_2 = interval_2

    return max(start_1,start_2),min(end_1,end_2)

def generate_intervals(raw_data):
    return [
        [x[0]['from'],x[0]['to']] for x in raw_data
    ]

def find_overlapping_interval(intervals):
    #Sort by the front
    intervals.sort(key=lambda x: x[0])
    res = [[1,intervals[0]]]
    
    for index,item in enumerate(intervals):
        if index == 0: continue

        start,end = item
        _,prev_end = res[-1][1]
        ctr = res[-1][0]

        if start <= prev_end:
            res[-1] = [ctr+1,find_overlap(item,res[-1][1])]
            
        else:
            res.append([1,item])

    return res

print(find_overlapping_interval(generate_intervals(x)))