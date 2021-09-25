from collections import deque
import json
from copy import deepcopy

def locate_parasite(grid):
    # traverse rows
    for i in range(len(grid)):
        # traverse columns
        for j in range(len(grid[0])):
            if grid[i][j] == 3:
                return i, j

def solve_3(data):
  start_row,start_col = 0,0
  for i in range(len(data)):
    for j in range(len(data[i])):
      if data[i][j] == 3:
        start_row = i
        start_col = j
        break
  
  q = deque([[start_row,start_col,0]])

  vacant = 0
  infected = 0
  vaccinated = 0
  time_taken = 0
  data[start_row][start_col]=1
  
  while q:
    r,c,curr_time = q.popleft()
    

    if r < 0 or r >= len(data) or c < 0 or c >= len(data[0]):
      continue

    #Visited Cell
    if data[r][c] == '#':
      continue

    #Else update vacant and vaccinated count
    if data[r][c] == 0:
      vacant+=1

    elif data[r][c] == 1:
      infected +=1
      time_taken = max(curr_time,time_taken)

      q.append([r+1,c,curr_time+1])
      q.append([r-1,c,curr_time+1])
      q.append([r,c+1,curr_time+1])
      q.append([r,c-1,curr_time+1])

      q.append([r-1,c-1,curr_time+1])
      q.append([r-1,c+1,curr_time+1])
      q.append([r+1,c+1,curr_time+1])
      q.append([r+1,c-1,curr_time+1])

    elif data[r][c] == 2:
      vaccinated+=1

    data[r][c] = '#'
  
  return time_taken if len(data)*len(data[0]) - (vacant + vaccinated) ==  infected else -1

def solve_1_and_2(data, x, y):
    grid = data["grid"]
    q = deque()
    visited = set()
    tally = {}
    for i in data["interestedIndividuals"]:
        tally[i] = -1

    def check_and_append(r, c):
        if (r, c) in visited:
            return
        if r >= len(grid) or r < 0:
            return
        if c >= len(grid[0]) or c < 0:
            return
        if grid[r][c] == 1 or grid[r][c] == 3:
            q.append((r, c))

    q.append((x, y))
    t = -1
    while q:
        width = len(q)
        t += 1
        for _ in range(width):
            a, b = q.popleft()
            check_and_append(a, b - 1)
            check_and_append(a, b + 1)
            check_and_append(a + 1, b)
            check_and_append(a - 1, b)
            str_coord = "{},{}".format(a, b)
            if t != 0 and str_coord in tally:
                tally[str_coord] = t
            grid[a][b] = 3
            visited.add((a, b))

    duration = t
    for i in grid:
        for j in i:
            if j == 1:
                duration = -1
                break
    

    return duration, tally

    

def solve(dataArr):
    res = []
    print(dataArr)
    for i in range(len(dataArr)):
        
        data = dataArr[i]
        print(data)
        if len(data["grid"][0] > 100) or len(data["grid"] > 100):
            ans = {
                "room": {},
                "p1": 0,
                "p2": 0,
                "p3": 0,
                "p4": 0,
            }

        else:
            x, y = locate_parasite(data["grid"])
            # part 1 and 2
            duration, tally = solve_1_and_2(deepcopy(data), x, y)
            p3_time = solve_3(deepcopy(data["grid"]))
            ans = {
                "room": data["room"],
                "p1": tally,
                "p2": duration,
                "p3": p3_time,
                "p4": 0,
            }
            res.append(ans)

    print(res)
    return res
