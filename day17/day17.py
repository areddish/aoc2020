def find_active_neighbors(grid, x, y, z, w):
    count = 0
    for dw in range(1, -2, -1):
        for dz in range(1, -2, -1):
            for dy in range(1, -2, -1):
                    for dx in range(1, -2, -1):
                        if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                            continue
                        if grid.get((x+dx,y+dy,z+dz,w+dw), False):
                            count += 1

    return count

def run_cycles(grid, dim, cycle_count = 6, consider_w=False):
    cycle = 1
    min_dim = -1
    max_dim = dim + 1
    while cycle < cycle_count + 1:
        new_grid = {x:True if grid[x] else False for x in grid }            
        for w in range(-cycle, cycle + 1) if consider_w else range(1):
            for z in range(-cycle, cycle + 1):
                for y in range(min_dim, max_dim + 1):
                    for x in range(min_dim, max_dim + 1):
                        active = grid.get((x,y,z,w), False)
                        active_n = find_active_neighbors(grid, x, y, z, w)
                        if active:
                            if active_n == 3 or active_n == 2:
                                new_grid[(x,y,z,w)] = True
                            else:
                                del new_grid[(x,y,z,w)]
                        else:
                            if active_n == 3:
                                new_grid[(x,y,z,w)] = True
                            else:
                                if (x,y,z) in new_grid:
                                    del new_grid[(x,y,z,w)]

        grid = new_grid
        cycle += 1
        min_dim -= 1
        max_dim += 1
    return len(grid)

#with open("test.txt") as file:
with open("day17.txt") as file:
    dim = 0
    grid = {}
    y = 0
    z = 0
    w = 0
    for line in file.read().splitlines():
        dim = len(line)
        for x,ch in enumerate(line):
            if ch == "#": 
                grid[(x,y,z,w)] = True
        y += 1

    print("Part 1", run_cycles(grid, dim))
    print("Part 2", run_cycles(grid, dim, consider_w=True))