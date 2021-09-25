

def generate_grid(entry_point,target_point):
    return [[0 for i in range(target_point[1]+1)] for j in range(target_point[0]+1)]

def calculate_minimum_cost(grid):
    
    dp = [[0 for i in range(len(grid[0]))] for i in range(len(grid))]

    for r in range(1,len(grid)):
        dp[r][0] = dp[r-1][0] + grid[r-1][0]
    
    for c in range(1,len(grid[0])):
        dp[0][c] = dp[0][c-1] + grid[0][c-1]
    
    for r in range(1,len(grid)):
        for c in range(1,len(grid[0])):
            dp[r][c] = min(dp[r-1][c]+grid[r-1][c],dp[r][c-1]+grid[r][c-1])

    return dp[-1][-1]

def assign_value(grid,r,c):
    if grid[r][c] == 3:
        grid[r][c] = 'L'
    elif grid[r][c] == 2:
        grid[r][c] = 'M'
    else:
        grid[r][c] = 'S'

def assign_grid_value(grid,target_point):
    map = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]
    map[0][0] = 'L'
    map[-1][-1] = 'L'
    for r in range(len(map)):
        for c in range(len(map[0])):
            if (r,c) != target_point and (r,c) != (0,0):
                assign_value(map,r,c)
    
    return map

def solve_instance(data):
    entry_point = int(data["entryPoint"]['first']), int(data["entryPoint"]['second'])
    target_point = int(data["targetPoint"]['first']),int(data["targetPoint"]['second'])
    horizontalStepper = int(data['horizontalStepper'])
    verticalStepper = int(data['verticalStepper'])
    gridDepth = int(data['gridDepth'])
    gridKey = int(data['gridKey'])

    

    grid = generate_grid(entry_point,target_point)


    for x in range(len(grid)):
        for y in range(len(grid[0])):
            #First Populate Risk index
            # Region at (0,0) has a risk index of 0
            # Region at target has risk index of 0
            # if y == 0 then risk is x * horizontal stepper
            # if x == 0 then risk is y * verticalStepper
            # else risk is grid[x-1][y] * grid[x][y-1]

            if (x,y) == (0,0):
                grid[x][y] =0
            elif (x,y) == target_point:
                grid[x][y] = 0
            elif y == 0:
                grid[x][y] = x * horizontalStepper
            elif x== 0:
                grid[x][y] = y * verticalStepper
            else:
                grid[x][y] = grid[x-1][y] * grid[x][y-1]
            grid[x][y] = ((grid[x][y]+gridDepth) % gridKey) % 3

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:
                grid[x][y] = 3
            elif grid[x][y] == 1:
                grid[x][y] = 2
            else:
                grid[x][y] = 1

    map = assign_grid_value(grid,target_point)
    dp = calculate_minimum_cost(grid)
    
    return {
        'gridMap':map,
        'minimumCost': 0
    }

def solve(data):
    res = [solve_instance(grd) for grd in data]
    return res


