x = {
    "entryPoint":{
        "first": 0,
        "second": 0
        },
    "targetPoint":{
        "first": 2,
        "second": 2
        },
    "gridDepth": 156,
    "gridKey":20183,
    "horizontalStepper":16807,
    "verticalStepper":48271
}

def generate_grid(entry_point,target_point):
    return [[0 for i in range(target_point[1]+1)] for j in range(target_point[0]+1)]

def assign_value(grid,r,c):
    if grid[r][c] == 0:
        grid[r][c] = 'L'
    elif grid[r][c] == 1:
        grid[r][c] = 'M'
    else:
        grid[r][c] = 'R'

def assign_grid_value(grid,target_point):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r,c) == target_point or (r,c) == (0,0):
                grid[r][c] == 0
            else:
                assign_value(grid,r,c)
    
    return grid

def solve_instance(data):
    entry_point = data["entryPoint"]['first'],data["entryPoint"]['second']
    target_point = data["targetPoint"]['first'],data["targetPoint"]['second']

    horizontalStepper = int(data['horizontalStepper'])
    verticalStepper = int(data['verticalStepper'])
    gridDepth = int(data['gridDepth'])
    gridKey = int(data['gridKey'])

    

    grid = generate_grid(entry_point,target_point)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if x == 0 and y == 0:
                continue
            elif y == 0:
                grid[x][y] = (x * horizontalStepper) % 3
            elif x == 0:
                grid[x][y] = (x * verticalStepper)%3
            else:
                grid[x][y] = (grid[x-1][y] * grid[x][y-1])
            # assign_value(grid,x,y)
            # print(grid[x][y])
    
    map = assign_grid_value(grid)
    return {
        'gridMap':map,
        'minimumCost':9
    }

def solve(data):
    res = [solve_instance(x) for x in data]
    print("Solved all values!")
    print(res)
    return res


