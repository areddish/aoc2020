EAST = (1, 0)
WEST = (-1, 0)
SOUTH = (0, -1)
NORTH = (0, 1)

mapping = {
    "N": NORTH,
    "E": EAST,
    "S": SOUTH,
    "W": WEST
}

import math

def deg_to_rad(deg):
    return deg * math.pi / 180.0

def rotate_waypoint(deg, loc, ref):
    x,y = loc
    x -= ref[0]
    y -= ref[1]
    ctheta = math.cos(deg_to_rad(deg))
    stheta = math.sin(deg_to_rad(deg))
    nx = x*ctheta-y*stheta
    ny = y*ctheta+x*stheta

    return (nx + ref[0], ny + ref[1])

def turn_right(dir,times):
    for x in range(times):
        if dir == NORTH:
            dir = EAST
        elif dir == EAST:
            dir = SOUTH
        elif dir == SOUTH:
            dir = WEST
        elif dir == WEST:
            dir = NORTH
    return dir

def turn_left(dir, times):
    for x in range(times):
        if dir == NORTH:
            dir = WEST
        elif dir == WEST:
            dir = SOUTH
        elif dir == SOUTH:
            dir = EAST
        elif dir == EAST:
            dir = NORTH
    return dir

#with open("test.txt", "rt") as file:
with open("day12.txt", "rt") as file:
    data = [(x[0], int(x[1:])) for x in file.read().splitlines()]
    
    #print (data)
    dir = EAST
    start = (0,0)
    
    for x in data:
        d, v = x
        if d == "R":
            assert v in [90, 180, 270]
            dir = turn_right(dir, v//90)
        elif d == "L":
            assert v in [90, 180, 270]
            dir = turn_left(dir, v//90)
        elif d == "F":
            dx,dy = dir
            dx *= v
            dy *= v
            start = (start[0] + dx, start[1] + dy)
        else:
            dx,dy = mapping[d]
            dx *= v
            dy *= v
            start = (start[0] + dx, start[1] + dy)
        #print(start)

    print ("Part 1", abs(start[0]) + abs(start[1]))


    dir = EAST
    waypoint = (10,1)
    start = (0,0)
    for x in data:
        d, v = x
        if d == "R":
            waypoint = rotate_waypoint(-v, waypoint, start)
        elif d == "L":
            waypoint = rotate_waypoint(v, waypoint, start)
        elif d == "F":
            dx = waypoint[0] - start[0]
            dy = waypoint[1] - start[1]
            dx *= v
            dy *= v
            start = (start[0] + dx, start[1] + dy)
            waypoint = (waypoint[0]+dx, waypoint[1]+dy)
        else:
            dx,dy = mapping[d]
            dx *= v
            dy *= v
            waypoint = (waypoint[0] + dx, waypoint[1] + dy)
        #print(start)

    print ("Part 2", abs(start[0]) + abs(start[1]))