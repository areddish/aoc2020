grid = {}
loc = (0, 0)
grid[loc] = "W"

max_x = 0
max_y = 0
#with open("test.txt") as file:
with open("day24.txt") as file:
    for line in file.read().splitlines():
        #e, se, sw, w, nw, and ne
        i = 0
        cur = (0,0)
        while i < len(line):
            if line[i] == "e":
                # east
                # print ("E")
                dx,dy = 2, 0
            elif line[i] == "w":
                # west
                # print ("W")
                dx,dy = -2, 0
            elif line[i] == "s":
                i += 1
                if line[i] == "e":
                    # s east
                    # print ("se")
                    dx,dy = 1, 1
                elif line[i] == "w":
                    # s west
                    # print ("sw")
                    dx,dy = -1, 1
            elif line[i] == "n":
                i += 1
                if line[i] == "e":
                    # s east
                    # print ("ne")
                    dx,dy = 1, -1
                elif line[i] == "w":
                    # s west
                    # print ("nw")
                    dx,dy = -1, -1
            x,y = cur
            cur = (x+dx, y+dy)
            i+=1
        max_x = max(max_x, abs(cur[0]))
        max_y = max(max_y, abs(cur[1]))
        if grid.get(cur, None):
            grid[cur] = "W" if grid[cur] == "B" else "B"
        else:
            grid[cur] = "B"
        

count = 0
for x in grid:
    if grid[x] == "B":
        count += 1
print("Part 1",count)


def get_neighbors(t, grid):
    count = 0
    for dx,dy in [(-1,1),(-2, 0), (-1, -1), (1,1), (2,0), (1,-1)]:
        if grid.get((t[0]+dx, t[1]+dy), "W") == "B":
            count += 1
    return count

# Fill in the grid with missing tiles
max_x = 150
max_y = 150
for y in range(-max_y-1,max_y+1):
    for x in range(-max_x-1,max_x+1):
        if grid.get((x,y), None) == None:
            grid[(x,y)] = "W"

day = 0
while day < 100:
    next_grid = {t:grid[t] for t in grid}
    for tile in grid:
        neighbors = get_neighbors(tile,grid)        
        if grid[tile] == "W" and neighbors == 2:
            next_grid[tile] = "B"
        if grid[tile] == "B" and (neighbors == 0 or neighbors > 2):
            next_grid[tile] = "W"
    grid = next_grid
    day += 1
    # count = 0
    # for x in grid:
    #     if grid[x] == "B":
    #         count += 1
    # print("Day", day, "=",count)

count = 0
for x in grid:
    if grid[x] == "B":
        count += 1
print("Part 2",count)