from collections import deque
x  = [[0, 3],
      [0, 1]]


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


print(solve_3(x))