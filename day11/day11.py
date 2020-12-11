
def get_occupied(grid, x, y, use_line_of_sight=False):
    w = len(grid[0])
    h = len(grid)
    count = 0

    for offset in [(-1,-1), (1,1), (-1, 1), (1,-1), (0,1), (0,-1), (-1,0), (1,0)]:
        dx,dy = offset
        nx = x + dx
        ny = y + dy
        while use_line_of_sight and 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == '.':
            nx += dx
            ny += dy

        if 0 <= nx < w and 0 <= ny < h:
            count += (1 if grid[ny][nx] == "#" else 0)
    return count

def deep_copy(l):
    new_l = []
    for x in l:
        new_l.append(x.copy())
    return new_l

def run(prefix, occupancy_threshold, use_line_of_sight = False):
    #with open("test.txt", "rt") as file:
    with open("day11.txt", "rt") as file:
        grid = [list(x) for x in file.read().splitlines()]

        w = len(grid[0])
        h = len(grid)
        did_seating_change = True
        while did_seating_change:
            did_seating_change = False
            test_grid = deep_copy(grid)
            for y in range(h):
                for x in range(w):
                    occupied_count = get_occupied(test_grid, x, y, use_line_of_sight)
                    if grid[y][x] == "L" and occupied_count == 0 :
                        grid[y][x] = "#" 
                        did_seating_change = True
                    elif grid[y][x] == "#" and occupied_count >= occupancy_threshold:
                        grid[y][x] = "L" 
                        did_seating_change = True

            # Uncomment to print steps
            # for y in range(h):
            #     for x in range(w):
            #         print (grid[y][x], end="")
            #     print()
            # print()

        count = 0
        for y in range(h):
            for x in range(w):
                if grid[y][x] == "#":
                    count += 1

        print(prefix, count)

run("Part 1", 4)
run("Part 2", 5, True)

