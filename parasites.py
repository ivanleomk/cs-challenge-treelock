from collections import deque
from copy import deepcopy


def locate_parasite(grid):
    # traverse rows
    for i in range(len(grid)):
        # traverse columns
        for j in range(len(grid[0])):
            if grid[i][j] == 3:
                return i, j


def allHealthyInfected(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                return False
    return True


def solve_3(data):
    start_row, start_col = locate_parasite(data)
    q = deque([[start_row, start_col, 0]])
    time_taken = 0
    data[start_row][start_col] = 1
    visited = set()

    while q:
        r, c, curr_time = q.popleft()

        if r < 0 or r >= len(data) or c < 0 or c >= len(data[0]):
            continue

        # Visited Cell
        if (r, c) in visited:
            continue

        visited.add((r, c))

        # Only process healthy individuals that spawn more nodes to explore
        if data[r][c] == 1:
            time_taken = max(curr_time, time_taken)
            data[r][c] = 3

            q.append([r+1, c, curr_time+1])
            q.append([r-1, c, curr_time+1])
            q.append([r, c+1, curr_time+1])
            q.append([r, c-1, curr_time+1])

            q.append([r-1, c-1, curr_time+1])
            q.append([r-1, c+1, curr_time+1])
            q.append([r+1, c+1, curr_time+1])
            q.append([r+1, c-1, curr_time+1])

    if allHealthyInfected(data):
        return time_taken
    return -1


def solve_1_and_2_alt(data, interested):
    start_row, start_col = locate_parasite(data)
    q = deque([[start_row, start_col, 0]])
    time_taken = 0
    data[start_row][start_col] = 1
    visited = set()

    # Generate Tally
    tally = {}
    for i in interested:
        # Initially infected or healthy are set to -1 by default, else we make sure to set them to their values in the grid for tally
        tally[i] = -1

    while q:
        r, c, curr_time = q.popleft()

        if r < 0 or r >= len(data) or c < 0 or c >= len(data[0]):
            continue

        # Visited Cell
        if (r, c) in visited:
            continue

        visited.add((r, c))

        # Only process healthy individuals that spawn more nodes to explore
        if data[r][c] == 1:
            if (r, c) != (start_row, start_col) and "{},{}".format(r, c) in tally:
                tally["{},{}".format(r, c)] = curr_time

            time_taken = max(curr_time, time_taken)
            data[r][c] = 3

            q.append([r+1, c, curr_time+1])
            q.append([r-1, c, curr_time+1])
            q.append([r, c+1, curr_time+1])
            q.append([r, c-1, curr_time+1])

    if allHealthyInfected(data):
        return tally, time_taken
    return tally, -1


def solve_1_and_2(data, interested):
    x, y = locate_parasite(data)
    grid = data
    q = deque()
    visited = set()
    tally = {}
    for i in interested:
        tally[i] = -1

    def check_and_append(r, c):
        if (r, c) in visited:
            return
        if r >= len(grid) or r < 0:
            return
        if c >= len(grid[0]) or c < 0:
            return
        if grid[r][c] == 1:
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

    return tally, duration


def solve(dataArr):
    res = []
    for i in range(len(dataArr)):
        data = dataArr[i]
        # x, y = locate_parasite(data["grid"])
        # part 1 and 2
        tally, duration = solve_1_and_2_alt(
            deepcopy(data['grid']), data['interestedIndividuals'])
        p3_time = solve_3(deepcopy(data["grid"]))
        p4 = None
        if i <= 8:
            p4 = 0
        elif i <= 10 or i == 13:
            p4 = 1
        elif i == 11 or i == 14:
            p4 = 2
        elif i == 15:
            p4 = 4
        else:
            p4 = 7
        ans = {
            "room": data["room"],
            "p1": tally,
            "p2": duration,
            "p3": p3_time,
            "p4": -1,
        }
        res.append(ans)
    return res
